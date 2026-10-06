import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from autoeval.core import corpus, make_prompt, score_response, validate_corpus, value_matches, write_json
from autoeval.providers import Ollama, regex_baseline
from autoeval.report import aggregate, export
from autoeval.runner import run

ROOT = Path(__file__).resolve().parents[1]


class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.docs, cls.cases = corpus(ROOT)

    def case(self, suffix="extract", source="19V627"):
        return next(c for c in self.cases if c["id"] == source+"-"+suffix)

    def response(self, case):
        return {"answers": {key:{k:v for k,v in ref.items() if k in {"value","page","quote"}}
                            for key,ref in case["expected"].items()}}

    def test_real_corpus_hashes_quotes_and_splits(self):
        self.assertEqual(validate_corpus(ROOT)["cases"],9)

    def test_changed_source_hash_is_rejected(self):
        manifest,docs,cases=corpus(ROOT)
        manifest["sources"][0]["sha256"]="0"*64
        with patch("autoeval.core.corpus",return_value=(manifest,docs,cases)):
            with self.assertRaisesRegex(ValueError,"PDF hash mismatch"):
                validate_corpus(ROOT)

    def test_reference_quote_and_campaign_leakage_are_rejected(self):
        manifest,docs,cases=corpus(ROOT)
        cases[0]["expected"]["population"]["quote"]="A reference that is not in this report"
        with patch("autoeval.core.corpus",return_value=(manifest,docs,cases)):
            with self.assertRaisesRegex(ValueError,"Reference quote not found"):
                validate_corpus(ROOT)
        manifest,docs,cases=corpus(ROOT)
        cases[1]["split"]="pilot"
        with patch("autoeval.core.corpus",return_value=(manifest,docs,cases)):
            with self.assertRaisesRegex(ValueError,"Campaign leakage"):
                validate_corpus(ROOT)

    def test_expected_answers_never_in_prompt(self):
        case = dict(self.case())
        case["expected"] = {"SECRET_GOLD_MARKER":{}}
        messages = make_prompt(case,self.docs["19V627"])
        self.assertNotIn("SECRET_GOLD_MARKER",json.dumps(messages))

    def test_perfect_fields_and_quotes(self):
        for case in self.cases:
            if "expected" not in case:
                continue
            score=score_response(json.dumps(self.response(case)),case,self.docs[case["source_id"]])
            self.assertTrue(score["automatic_acceptance"],case["id"])
            self.assertTrue(score["human_review_required"])

    def test_null_is_not_zero_and_bool_is_not_integer(self):
        self.assertFalse(value_matches(0,None))
        self.assertFalse(value_matches(True,1))
        self.assertFalse(value_matches("229,460",229460))
        self.assertTrue(value_matches(None,None))

    def test_wrong_missing_information_is_critical(self):
        case=self.case();response=self.response(case)
        response["answers"]["defect_percent"]["value"]=0
        result=score_response(json.dumps(response),case,self.docs["19V627"])
        self.assertIn("defect_percent",result["critical_errors"])
        self.assertEqual(result["field_accuracy"],.8)

    def test_missing_null_field_does_not_count_as_correct(self):
        case=self.case();response=self.response(case)
        del response["answers"]["defect_percent"]
        result=score_response(json.dumps(response),case,self.docs["19V627"])
        self.assertFalse(result["schema_valid"])
        self.assertEqual(result["field_accuracy"],.8)

    def test_invalid_json_arrays_nan_and_fences(self):
        case=self.case()
        for raw in ['[]','```json\n{}\n```','{"answers":NaN}','bad']:
            result=score_response(raw,case,self.docs["19V627"])
            self.assertFalse(result["schema_valid"])

    def test_wrong_page_or_invented_quote_not_accepted(self):
        case=self.case();response=self.response(case)
        response["answers"]["population"]["page"]=99
        response["answers"]["supplier"]["quote"]="This is a fabricated reference."
        result=score_response(json.dumps(response),case,self.docs["19V627"])
        self.assertEqual(result["field_accuracy"],1)
        self.assertEqual(result["quote_validity"],.6)
        self.assertFalse(result["automatic_acceptance"])

    def test_extra_fields_break_schema(self):
        case=self.case();response=self.response(case)
        response["answers"]["extra"]={"value":"invented","page":1,"quote":"invented"}
        self.assertFalse(score_response(json.dumps(response),case,self.docs["19V627"])["schema_valid"])

    def test_summary_has_no_fake_semantic_score(self):
        case=self.case("summary")
        result=score_response(json.dumps({"summary":"Texte inexact mais bien structuré.","citations":[{"page":1,"quote":"NHTSA Recall No. : 19V-627"}]}),case,self.docs["19V627"])
        self.assertTrue(result["schema_valid"])
        self.assertEqual(result["quote_validity"],1)
        self.assertIsNone(result["quality_score"])
        self.assertFalse(result["length_respected"])

    def test_baseline_cannot_consult_answers(self):
        case=self.case();changed={**case,"expected":{}}
        result=json.loads(regex_baseline(changed,self.docs["19V627"]))
        self.assertEqual(result["answers"]["population"]["value"],229460)
        self.assertIsNone(result["answers"]["defect_percent"]["value"])
        self.assertIsNone(result["answers"]["supplier"]["value"])

    def test_network_is_loopback_only(self):
        for endpoint in ['https://api.example.com','http://127.0.0.1.evil.com','http://name:secret@localhost','http://localhost/api']:
            with self.assertRaises(ValueError):
                Ollama(endpoint)

    def test_streaming_counts_content_not_empty_packets(self):
        client=Ollama()
        events=[{"message":{"content":""}}, {"message":{"content":"{\"ok\":"}},
                {"message":{"content":"true}"}}, {"done":True,"done_reason":"stop","eval_count":10,
                 "eval_duration":2_000_000_000,"prompt_eval_count":42}]
        stream=io.BytesIO(b"\n".join(json.dumps(e).encode() for e in events))
        with patch.object(client.opener,"open",return_value=stream):
            result=client.generate("test",[],41)
        self.assertEqual(result["raw_response"],'{"ok":true}')
        self.assertEqual(result["metrics"]["generation_tokens_per_s"],5)
        self.assertEqual(result["metrics"]["input_tokens"],42)
        self.assertIsNotNone(result["metrics"]["first_content_chunk_s"])

    def test_unfinished_stream_is_failure(self):
        client=Ollama()
        with patch.object(client.opener,"open",return_value=io.BytesIO(b'{"message":{"content":"partial"}}\n')):
            with self.assertRaises(RuntimeError):
                client.generate("test",[],41)

    def test_provider_error_is_not_silently_scored(self):
        client=Ollama()
        with patch.object(client.opener,"open",return_value=io.BytesIO(b'{"error":"out of memory"}\n')):
            with self.assertRaisesRegex(RuntimeError,"out of memory"):
                client.generate("test",[],41)

    def test_aggregation_keeps_failures_and_repetition_units(self):
        rows=[{"model":"a","task":"extraction","case_id":"c","status":"ok",
               "score":{"field_accuracy":1,"schema_valid":True},"metrics":{"latency_s":1}},
              {"model":"a","task":"extraction","case_id":"c","status":"error","metrics":{"latency_s":3}}]
        result=aggregate(rows)[0]
        self.assertEqual(result["field_accuracy"],.5)
        self.assertEqual(result["error_rate"],.5)
        self.assertEqual(result["distinct_cases"],1)
        self.assertEqual(result["mean_repeat_range"],1)

    def test_full_baseline_run_and_safe_static_export(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            shutil.copytree(ROOT/"data/raw",root/"data/raw")
            shutil.copytree(ROOT/"data/processed",root/"data/processed")
            for name in ['cases.json','manifest.json']:
                shutil.copy2(ROOT/"data"/name,root/"data"/name)
            shutil.copytree(ROOT/"web",root/"web")
            with contextlib.redirect_stdout(io.StringIO()):
                run_dir=run(root,[],"pilot",1,baseline=True)
                result_file=run_dir/"results.jsonl"
                rows=[json.loads(x) for x in result_file.read_text().splitlines()]
                self.assertEqual(len(rows),2)
                rows[0]["raw_response"]='</script><script>alert(1)</script>'
                result_file.write_text("\n".join(json.dumps(r) for r in rows))
                export(root,[run_dir],root/"site")
            rendered=(root/"site/index.html").read_text()
            self.assertNotIn('</script><script>alert(1)',rendered)
            self.assertIn('\\u003c/script>',rendered)
            self.assertFalse((root/"site/sources").exists())


if __name__=="__main__":
    unittest.main()

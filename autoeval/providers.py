"""Loopback-only streaming Ollama client. No cloud provider or automatic retry."""
import json
import time
import urllib.request
from urllib.parse import urlparse


class Ollama:
    def __init__(self, base_url="http://127.0.0.1:11434", timeout=180):
        parsed = urlparse(base_url)
        if (parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
                or parsed.username or parsed.password or parsed.path not in {"", "/"}
                or parsed.query or parsed.fragment):
            raise ValueError("Only local Ollama HTTP endpoints are allowed")
        self.base_url, self.timeout = base_url.rstrip("/"), timeout
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def request(self, path, payload=None):
        body = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(self.base_url + path, data=body, headers={"Content-Type": "application/json"})
        with self.opener.open(req, timeout=self.timeout) as response:
            return json.load(response)

    def identity(self, model):
        tags = self.request("/api/tags")["models"]
        item = next((m for m in tags if m["name"] == model), None)
        if item is None:
            raise ValueError(f"Local model not installed: {model}. Run: ollama pull {model}")
        info = self.request("/api/show", {"model": model})
        return {"name": model, "digest": item["digest"], "details": item.get("details"),
                "capabilities": info.get("capabilities", []), "ollama_version": self.request("/api/version")["version"]}

    def generate(self, model, messages, seed, thinking_supported=False, max_tokens=1400):
        options = {"temperature": 0.2, "seed": seed, "num_ctx": 16384, "num_predict": max_tokens}
        payload = {"model": model, "messages": messages, "stream": True, "format": "json",
                   "keep_alive": "5m", "options": options}
        if thinking_supported:
            payload["think"] = False
        req = urllib.request.Request(self.base_url + "/api/chat", data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        started, first, chunks, terminal = time.perf_counter(), None, [], None
        with self.opener.open(req, timeout=self.timeout) as response:
            for line in response:
                if time.perf_counter() - started > self.timeout:
                    raise TimeoutError("Overall generation deadline exceeded")
                if not line.strip():
                    continue
                event = json.loads(line)
                if event.get("error"):
                    raise RuntimeError(event["error"])
                content = event.get("message", {}).get("content", "")
                if content:
                    first = first if first is not None else time.perf_counter() - started
                    chunks.append(content)
                if event.get("done"):
                    terminal = event
        if terminal is None:
            raise RuntimeError("Stream ended without completion marker")
        seconds = time.perf_counter() - started
        generation_ns = terminal.get("eval_duration", 0)
        return {"raw_response": "".join(chunks), "parameters": options,
                "metrics": {"latency_s": seconds, "first_content_chunk_s": first,
                    "input_tokens": terminal.get("prompt_eval_count"),
                    "output_tokens": terminal.get("eval_count"),
                    "generation_tokens_per_s": terminal.get("eval_count", 0) / (generation_ns / 1e9) if generation_ns else None,
                    "load_s": terminal.get("load_duration", 0) / 1e9,
                    "api_cost_eur": 0.0, "energy_cost_eur": None},
                "done_reason": terminal.get("done_reason"),
                "provider_terminal": {k: v for k, v in terminal.items() if k != "message"}}


def regex_baseline(case, doc):
    """Explicit labels only; does not consult expected answers or semantic rubrics."""
    import re
    patterns = {"campaign": r"NHTSA Recall No\.\s*:\s*([^\n]+)",
                "manufacturer": r"Manufacturer Name\s*:\s*([^\n]+)",
                "population": r"Number of potentially involved\s*:\s*([\d,]+)",
                "defect_percent": r"Estimated percentage with defect\s*:\s*(NR|[\d.]+)"}
    answers = {}
    for field in case["fields"]:
        match, page = None, None
        if field in patterns:
            for p in doc["pages"]:
                match = re.search(patterns[field], p["text"])
                if match:
                    page = p["page"]
                    break
        if match:
            value = match[1].strip()
            value = None if value == "NR" else value
            if field in {"population", "defect_percent"} and value is not None:
                value = float(value.replace(",", ""))
                value = int(value) if value.is_integer() else value
            answers[field] = {"value": value, "page": page, "quote": match[0]}
        else:
            answers[field] = {"value": None, "page": None, "quote": None}
    return json.dumps({"answers": answers}, ensure_ascii=False)

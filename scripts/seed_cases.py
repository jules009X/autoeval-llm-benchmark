"""Curated annotations from downloaded reports. Never generates source facts."""
import hashlib
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from autoeval.core import digest, read_json, write_json

ROOT = Path(__file__).resolve().parents[1]


def ref(value, page, quote, critical=False):
    return dict(value=value, page=page, quote=quote, critical=critical)


def create():
    records = [
        ("24V720", "24V-720", "2024-09-27", "Batteries haute tension — Jeep", "https://static.nhtsa.gov/odi/rcl/2024/RCLRPT-24V720-8602.PDF", "dev"),
        ("24V436", "24V-436", "2025-01-30", "Caméras de recul — FCA", "https://static.nhtsa.gov/odi/rcl/2024/RCLRPT-24V436-2012.PDF", "pilot"),
        ("19V627", "19V-627", "2020-06-01", "Airbags passager — Toyota", "https://static.nhtsa.gov/odi/rcl/2019/RCLRPT-19V627-7873.PDF", "pilot")]
    sources = []
    for sid, campaign, date, title, url, split in records:
        sources.append(dict(id=sid, campaign=campaign, document_date=date, title=title, url=url,
            split=split, retrieved_at="2026-10-06", origin="NHTSA / manufacturer submission",
            synthetic=False, sha256=hashlib.sha256((ROOT / f"data/raw/{sid}.pdf").read_bytes()).hexdigest(),
            text_sha256=digest(read_json(ROOT / f"data/processed/{sid}.json")),
            reuse_status="Publicly accessible; third-party submission. No blanket redistribution license asserted."))
    # Pin the extractor actually used; reproducibility is checked before every run.
    import pypdf
    write_json(ROOT / "data/manifest.json", {"version": "0.1.0", "extractor": "pypdf", "extractor_version": pypdf.__version__, "sources": sources})
    extraction = {
      "24V720": {
        "campaign": ref("24V-720",1,"NHTSA Recall No. : 24V-720"),
        "manufacturer": ref("Chrysler (FCA US, LLC)",1,"Manufacturer Name : Chrysler (FCA US, LLC)"),
        "population": ref(154032,1,"Number of potentially involved : 154,032",True),
        "defect_percent": ref(1,1,"Estimated percentage with defect : 1 %",True),
        "supplier": ref("Samsung SDI America INC",3,"Name : Samsung SDI America INC"),
      },
      "24V436": {
        "campaign": ref("24V-436",1,"NHTSA Recall No. : 24V-436"),
        "manufacturer": ref("Chrysler (FCA US, LLC)",1,"Manufacturer Name : Chrysler (FCA US, LLC)"),
        "population": ref(1033433,1,"Number of potentially involved : 1,033,433",True),
        "defect_percent": ref(100,1,"Estimated percentage with defect : 100 %",True),
        "supplier": ref("Harman",7,"Name : Harman"),
      },
      "19V627": {
        "campaign": ref("19V-627",1,"NHTSA Recall No. : 19V-627"),
        "manufacturer": ref("Toyota Motor Engineering & Manufacturing",1,"Manufacturer Name : Toyota Motor Engineering & Manufacturing"),
        "population": ref(229460,1,"Number of potentially involved : 229,460",True),
        "defect_percent": ref(None,1,"Estimated percentage with defect : NR",True),
        "supplier": ref("Joyson Safety Systems Japan K. K.",3,"Name : Joyson Safety Systems Japan K. K."),
      }}
    timelines = {
      "24V720": (
        {"investigation_date":"Date d'ouverture de l'enquête mentionnée dans la chronologie.",
         "decision_date":"Date de décision du rappel volontaire.",
         "planned_dealer_date":"Date prévue de notification aux concessionnaires.",
         "planned_owner_start":"Début de la plage Planned Owner Notification Date.",
         "actual_owner_date":"Date EFFECTIVE d'envoi aux propriétaires, null si non attestée dans ce document."},
        {"investigation_date":ref("2024-06-25",3,"On June 25, 2024, the FCA US LLC",True),
         "decision_date":ref("2024-09-20",3,"On September 20, 2024, FCA US determined",True),
         "planned_dealer_date":ref("2024-10-03",4,"Planned Dealer Notification Date : OCT 03, 2024 - OCT 03, 2024"),
         "planned_owner_start":ref("2024-10-17",4,"Planned Owner Notification Date : OCT 17, 2024 - OCT 29, 2024"),
         "actual_owner_date":ref(None,4,"FCA US will notify dealers on or about 10/3/2024 and begin notifying owners on or about 10/17/2024.",True)}),
      "24V436": (
        {"initial_alert":"Date de notification du problème potentiel à TSRC.",
         "decision_date":"Date de décision du rappel volontaire.",
         "actual_durango_date":"Date effective d'envoi des lettres finales aux propriétaires de Dodge Durango 2021-2022.",
         "latest_pacifica_plan":"Date prévue la plus récente pour les lettres aux propriétaires de Chrysler Pacifica 2021, selon la mise à jour du 30 janvier 2025.",
         "actual_pacifica_date":"Date effective des lettres FINALES aux propriétaires de Chrysler Pacifica 2021, null si non attestée."},
        {"initial_alert":ref("2023-10-23",8,"On October 23, 2023, the FCA US LLC"),
         "decision_date":ref("2024-06-06",8,"On June 06, 2024, FCA US determined",True),
         "actual_durango_date":ref("2024-12-12",9,"FCA US began mailing Final letters to owners of 2021-2022 Dodge Durango vehicles on 12/12/2024",True),
         "latest_pacifica_plan":ref("2025-02-20",9,"Pacifica vehicles on or about 02/20/2025",True),
         "actual_pacifica_date":ref(None,9,"Pacifica vehicles on or about 02/20/2025",True)}),
      "19V627": (
        {"submission_date":"Date de soumission de CETTE version du rapport.",
         "actual_dealer_date":"Date effective de notification aux distributeurs/concessionnaires, d'après le récit.",
         "planned_owner_start":"Début de la plage Planned Owner Notification Date.",
         "investigation_date":"Date d'ouverture de l'enquête : null si absente des quatre pages fournies.",
         "production_fix_date":"Date de correction en production, null si non renseignée."},
        {"submission_date":ref("2020-06-01",1,"Submission Date : JUN 01, 2020"),
         "actual_dealer_date":ref("2019-08-28",4,"Notifications to distributors/dealers were sent on August 28, 2019.",True),
         "planned_owner_start":ref("2019-09-25",4,"Planned Owner Notification Date : SEP 25, 2019 - OCT 27, 2019"),
         "investigation_date":ref(None,4,"Please see the attached Part 573 Defect Information Report for the full chronology.",True),
         "production_fix_date":ref(None,4,"Identify How/When Recall Condition was Corrected in Production : NR",True)})}
    rubrics = {
      "24V720": [
        ("Population et véhicules concernés, sans assimiler population et défauts confirmés",1,"Number of potentially involved : 154,032"),
        ("Dégradation du séparateur et risque d'incendie formulés avec prudence",2,"In rare circumstances, a battery pack may contain cells with separator damage."),
        ("Investigation de la cause encore en cours dans cette version",3,"Root cause investigation continues."),
        ("Logiciel puis remplacement de batterie si nécessaire",4,"Remedy is a software flash followed by a HV battery replacement if needed."),
        ("Dates de notification décrites comme prévisionnelles",4,"Planned Owner Notification Date : OCT 17, 2024 - OCT 29, 2024")],
      "24V436": [
        ("Population potentiellement concernée exacte",1,"Number of potentially involved : 1,033,433"),
        ("Défaut d'affichage de caméra attribué au logiciel",7,"Vehicles with suspect radio software may not display the rearview image during a backing event under certain conditions."),
        ("Correction logicielle et deux campagnes constructeur",8,"The vehicle population will be managed between 2 FCA US campaign ID numbers, 66B and 79B."),
        ("OTA ou USB selon capacité",8,"Vehicles will be updated either via firmware Over-The-Air; if capable, or via USB."),
        ("Distinction entre envoi Durango réalisé et échéance Pacifica révisée",9,"Pacifica vehicles on or about 02/20/2025")],
      "19V627": [
        ("Population et incertitude sur le pourcentage défectueux",1,"Toyota is unable to provide an estimate of the percentage of vehicles to actually contain the defect."),
        ("Risque de déploiement incorrect à haute température",3,"There is a possibility that the air bag may not unfold as designed during inflation under high temperature conditions"),
        ("Remplacement du module ou sous-ensemble de l'airbag passager",4,"Dealers will replace the front passenger airbag assembly"),
        ("Chronologie complète absente, renvoi à une pièce jointe",4,"Please see the attached Part 573 Defect Information Report for the full chronology."),
        ("Envoi aux concessionnaires attesté au 28 août 2019",4,"Notifications to distributors/dealers were sent on August 28, 2019.")]}
    cases = []
    for source in sources:
        sid = source["id"]
        common = {"source_id":sid,"split":source["split"],"version":"0.1.0",
                  "annotation_status":"AI-prepared, source-checked; independent human validation pending",
                  "context":"full_report","input_language":"en","output_language":"fr","business_criticality":"high"}
        cases.append({**common,"id":sid+"-extract","task":"extraction","complexity":"medium",
          "title":"Extraire les caractéristiques du rappel",
          "instruction":"Extrais les caractéristiques du rappel. Ne confonds pas la population potentiellement concernée et le nombre de défauts confirmés.",
          "fields":{"campaign":"Identifiant NHTSA exact, avec tiret.","manufacturer":"Nom exact du constructeur dans l'en-tête.",
                    "population":"Nombre total de véhicules potentiellement concernés, entier.","defect_percent":"Pourcentage estimé défectueux, nombre entre 0 et 100, ou null si NR.",
                    "supplier":"Nom exact du fabricant de composant dans Supplier Identification."},"expected":extraction[sid]})
        fields, expected = timelines[sid]
        cases.append({**common,"id":sid+"-timeline","task":"chronology","complexity":"high",
          "title":"Distinguer événements et prévisions",
          "instruction":"Reconstitue les dates demandées en distinguant ce qui était prévu de ce qui est attesté comme réalisé. Les mises à jour ont leur propre date.",
          "fields":fields,"expected":expected})
        cases.append({**common,"id":sid+"-summary","task":"synthesis","complexity":"high",
          "title":"Préparer une synthèse qualité sourcée",
          "instruction":"Prépare une synthèse pour une revue qualité : périmètre, problème rapporté, action corrective, état des notifications et limites documentaires. Ne formule pas de conseil actuel à un propriétaire.",
          "rubric":[{"criterion":c,"page":p,"quote":q,"weight":1} for c,p,q in rubrics[sid]]})
    write_json(ROOT / "data/cases.json", {"version":"0.1.0","cases":cases})


if __name__ == "__main__":
    create()

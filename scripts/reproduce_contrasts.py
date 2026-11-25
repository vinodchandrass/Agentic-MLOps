import csv
import json
from pathlib import Path

def reproduce():
    path = Path(__file__).resolve().parents[1] / "extraction/provisional_contrasts.csv"
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        a,b = float(r["baseline"]),float(r["candidate"])
        kind = r["transformation"]
        if r["denominator"]:
            delta = 100*(int(r["candidate_count"])-int(r["baseline_count"]))/int(r["denominator"])
        elif kind == "relative_percent":
            delta = 100*(b-a)/a
        else:
            delta = b-a
        tolerance = {"pp":0.011,"relative_percent":0.005,"absolute":0.00005}[kind]
        assert abs(delta-float(r["reported_difference"])) <= tolerance, r
        out.append(dict(study=r["study"],metric=r["metric"],comparator=r["comparator"],difference=round(delta,6),unit=kind,provenance=r["provenance"]))
    assert len(out)==15 and len({r["study"] for r in out})==4
    return out

if __name__ == "__main__":
    print(json.dumps(reproduce(),indent=2))

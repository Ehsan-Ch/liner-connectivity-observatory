"""Join frozen WDI series and compare their ranks without filling missing years."""
from collections import Counter
import json
from math import isfinite
from pathlib import Path
from statistics import correlation, StatisticsError

ROOT = Path(__file__).resolve().parent
YEARS = tuple(range(2019, 2025))


def load(name):
    meta, rows = json.loads((ROOT / "source-data" / f"{name}.json").read_text(encoding="utf-8-sig"))
    if int(meta["pages"]) != 1 or int(meta["total"]) != len(rows):
        raise ValueError(f"Incomplete snapshot: {name}")
    return rows


def observations(rows, indicator, codes):
    values = {}
    for row in rows:
        code = row["countryiso3code"]
        year = int(row["date"])
        if row["indicator"]["id"] != indicator or year not in YEARS:
            raise ValueError("Unexpected indicator or year")
        if code not in codes:
            continue
        key = (code, year)
        if key in values:
            raise ValueError(f"Duplicate observation: {key}")
        value = row["value"]
        if value is not None and (not isinstance(value, (int, float)) or
                                  isinstance(value, bool) or not isfinite(value) or value < 0):
            raise ValueError(f"Unexpected value: {key}")
        values[key] = value
    return values


def ranks(values):
    """Return descending ranks using average positions for ties."""
    frequencies = Counter(values)
    positions = {}
    start = 1
    for value in sorted(frequencies, reverse=True):
        count = frequencies[value]
        positions[value] = start + (count-1)/2
        start += count
    return [positions[value] for value in values]


def compare(rows):
    paired = [dict(row) for row in rows if row["teu"] is not None and row["index"] is not None]
    teu = ranks([row["teu"] for row in paired])
    index = ranks([row["index"] for row in paired])
    try:
        rho = round(correlation(teu, index), 6)
    except StatisticsError:
        rho = None
    for row, t, i in zip(paired, teu, index):
        row.update(teu_rank=t, index_rank=i, gap=t-i)
    paired.sort(key=lambda row: (-abs(row["gap"]), row["code"]))
    return {
        "eligible": len(rows),
        "matched": len(paired),
        "traffic_only": sum(r["teu"] is not None and r["index"] is None for r in rows),
        "index_only": sum(r["teu"] is None and r["index"] is not None for r in rows),
        "neither": sum(r["teu"] is None and r["index"] is None for r in rows),
        "rho": rho,
        "rows": paired,
    }


def experiment():
    geographies = {r["id"]: (r["name"], r["region"]["value"].strip()) for r in load("economies")
                   if r["region"]["id"] not in ("", "NA")}
    teu = observations(load("traffic"), "IS.SHP.GOOD.TU", geographies)
    index = observations(load("connectivity"), "IS.SHP.GCNW.XQ", geographies)
    regions = sorted({region for _, region in geographies.values()})
    cohorts = {}
    for year in YEARS:
        rows = [{"code": code, "name": name, "region": region,
                 "teu": teu.get((code, year)), "index": index.get((code, year))}
                for code, (name, region) in sorted(geographies.items())]
        cohorts[year] = {"All regions": compare(rows)}
        for region in regions:
            cohorts[year][region] = compare([row for row in rows if row["region"] == region])
    return {"regions": ["All regions", *regions], "years": YEARS, "cohorts": cohorts}

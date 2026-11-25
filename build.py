import json
from analysis import ROOT, experiment


def render():
    template = (ROOT / "explorer.html").read_text(encoding="utf-8")
    payload = json.dumps(experiment(), separators=(",", ":"), allow_nan=False).replace("<", "\\u003c")
    if template.count("<!-- REPORT -->") != 1:
        raise ValueError("The report placeholder must occur exactly once")
    return template.replace("<!-- REPORT -->", payload)


if __name__ == "__main__":
    (ROOT / "index.html").write_text(render(), encoding="utf-8", newline="\n")

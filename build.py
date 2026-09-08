#!/usr/bin/env python3
"""Samler index.html af skabelon + datasæt + indlejret Montserrat.

    python3 build.py              # henter data fra Supabase, falder tilbage til eu_data.py
    python3 build.py --local      # bruger altid eu_data.py
    python3 build.py --db         # kræver Supabase; fejler frem for at falde tilbage

Output er en enkelt selvbærende fil uden eksterne kald — den kan åbnes direkte
som file://, lægges bag en statisk host eller publiceres som artefakt. Fonten
indlejres som data-URI, fordi siden skal virke uden netværk.

Sandheden ligger i Supabase (se supabase/migrations/). eu_data.py er kilden til
den første indlæsning og fungerer som reserve, når der ikke er credentials —
fx i et frisk klon. De to giver identisk output; det er efterprøvet.
"""
import base64
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = ROOT / "eu-page-template.html"
FONT = ROOT / "fonts" / "Montserrat-VariableFont_wght.ttf"
TITLE = "EU-lovgivning i den digitale sektor"

RESET = """  *,*::before,*::after{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{margin:0}
  img,svg{max-width:100%}
  button,input{font-family:inherit;font-size:inherit}"""


def from_db():
    """Henter kategorier og retsakter via PostgREST med anon-nøglen.

    Udsigten acts_json leverer præcis den form, skabelonen forventer, så der
    er ingen omformning her — og dermed intet sted den kan komme i utakt.
    """
    sys.path.insert(0, str(ROOT))
    from scripts.db import env

    url, key = env("SUPABASE_URL"), env("SUPABASE_ANON_KEY")
    out = subprocess.run(
        ["curl", "-sf", "--max-time", "60", f"{url}/rest/v1/acts_json?select=*",
         "-H", f"apikey: {key}", "-H", f"Authorization: Bearer {key}"],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"kunne ikke læse fra Supabase (curl {out.returncode})")
    data = json.loads(out.stdout)
    if not data:
        raise RuntimeError("acts_json er tom — er seed-scriptet kørt?")
    return data


def _summary(s):
    """Samme nøglerækkefølge som resten — se canonical()."""
    if not s:
        return None
    return {
        "subject": s["subject"],
        "scope": s["scope"],
        "duties": list(s["duties"]),
        "timeline": [
            {"date": t["date"], "label": t["label"], "note": t.get("note")}
            for t in s["timeline"]
        ],
        "supervision": s["supervision"],
        "sanctions": s["sanctions"],
        "note": list(s["note"]),
        "related": list(s["related"]),
        "sources": [{"label": q["label"], "url": q["url"]} for q in s["sources"]],
        "reviewed": str(s["reviewed"]),
    }


def _dk(d):
    """Samme nøglerækkefølge som resten — se canonical()."""
    if not d:
        return None
    return {
        "status": d["status"],
        "instrument": d.get("instrument"),
        "instrumentRef": d.get("instrumentRef"),
        "instrumentUrl": d.get("instrumentUrl"),
        "timeline": [
            {"date": t["date"], "label": t["label"], "note": t.get("note")}
            for t in d.get("timeline", [])
        ],
        "authorities": [
            {"name": au["name"], "url": au.get("url"), "scope": au.get("scope")}
            for au in d.get("authorities", [])
        ],
    }


def canonical(data):
    """Fastlægger nøglerækkefølgen, så begge kilder giver byte-identisk output.

    PostgREST sorterer nøgler alfabetisk, Python bevarer indsættelsesorden. Uden
    dette ville `python3 build.py --db` og `--local` producere to forskellige
    filer med samme indhold, og enhver diff på index.html blev ubrugelig.
    """
    return [
        {
            "key": c["key"],
            "name": c["name"],
            "desc": c["desc"],
            "acts": [
                {
                    "name": a["name"],
                    "slug": a["slug"],
                    "type": a["type"],
                    "status": a["status"],
                    "statusNote": a["statusNote"],
                    "refs": [
                        {"label": r["label"], "celex": r["celex"], "url": r["url"]}
                        for r in a["refs"]
                    ],
                    "proc": a["proc"],
                    "procUrl": a["procUrl"],
                    "appliesFrom": a["appliesFrom"],
                    "appliesNote": a["appliesNote"],
                    "summary": _summary(a.get("summary")),
                    "dk": _dk(a.get("dk")),
                }
                for a in c["acts"]
            ],
        }
        for c in data
    ]


def check(data):
    """Kontrollerer det, en aktside pr. retsakt gør farligt at få forkert.

    Slugs bliver adresser. To retsakter med samme slug ville sende læseren til
    den samme side, uden at noget så galt ud — derfor afbrydes byggeriet.
    Uopklarede related-navne er derimod et legitimt hul: datasættet stopper i
    2024, så et navn kan pege på en retsakt, der ikke er med endnu. De vises som
    ren tekst på siden og rapporteres her, så hullet er synligt frem for stille.
    """
    acts = [a for c in data for a in c["acts"]]

    seen = {}
    for a in acts:
        if a["slug"] in seen:
            raise SystemExit(
                f"slug-kollision: {a['slug']!r} bruges af både "
                f"{seen[a['slug']]!r} og {a['name']!r} — omdøb den ene"
            )
        seen[a["slug"]] = a["name"]

    names = {a["name"] for a in acts}
    unresolved = sorted({
        r for a in acts if a["summary"]
        for r in a["summary"]["related"] if r not in names
    })
    if unresolved:
        print(f"related uden retsakt i datasættet ({len(unresolved)}): "
              + ", ".join(unresolved))
    return len(acts)


def load(mode: str):
    if mode != "local":
        try:
            data = from_db()
            print(f"data hentet fra Supabase — {len(data)} kategorier")
            return data
        except (RuntimeError, SystemExit, json.JSONDecodeError) as err:
            if mode == "db":
                raise SystemExit(f"afbrudt: {err}")
            print(f"Supabase ikke tilgængelig ({err}) — bruger eu_data.py")

    sys.path.insert(0, str(ROOT))
    from eu_data import build as local_build

    return local_build()


def main():
    args = sys.argv[1:]
    mode = "db" if "--db" in args else "local" if "--local" in args else "auto"
    data = canonical(load(mode))
    n_acts = check(data)

    body = TEMPLATE.read_text(encoding="utf-8")
    body = body.replace(f"<title>{TITLE}</title>\n", "", 1)
    body = body.replace("__FONT__", base64.b64encode(FONT.read_bytes()).decode())
    body = body.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    if "__FONT__" in body or "__DATA__" in body:
        raise SystemExit("skabelonen har uudfyldte pladsholdere")

    (ROOT / "eu_digital_acts.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (ROOT / "index.html").write_text(
        f"""<!doctype html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<style>
{RESET}
</style>
</head>
<body>
{body}
</body>
</html>
""",
        encoding="utf-8",
    )

    print(f"index.html bygget — {len(data)} kategorier, {n_acts} retsakter, "
          f"{n_acts} aktsider")


if __name__ == "__main__":
    main()

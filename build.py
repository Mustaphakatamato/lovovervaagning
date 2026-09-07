#!/usr/bin/env python3
"""Samler index.html af skabelon + datasæt + indlejret Montserrat.

    python3 build.py

Output er en enkelt selvbærende fil uden eksterne kald — den kan åbnes
direkte som file://, lægges bag en statisk host eller publiceres som artefakt.
Fonten indlejres som data-URI, fordi siden skal virke uden netværk.
"""
import base64
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
TEMPLATE = ROOT / "eu-page-template.html"
FONT = ROOT / "fonts" / "Montserrat-VariableFont_wght.ttf"
TITLE = "EU-lovgivning i den digitale sektor"

RESET = """  *,*::before,*::after{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{margin:0}
  img,svg{max-width:100%}
  button,input{font-family:inherit;font-size:inherit}"""


def main():
    from eu_data import build

    data = build()
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

    acts = sum(len(c["acts"]) for c in data)
    print(f"index.html bygget — {len(data)} kategorier, {acts} retsakter")


if __name__ == "__main__":
    main()

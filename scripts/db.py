#!/usr/bin/env python3
"""Kører SQL mod Supabase gennem Management API'ets query-endpoint.

    python3 scripts/db.py supabase/migrations/0001_schema.sql
    python3 scripts/db.py -c "select count(*) from acts"

Der er hverken psql eller supabase CLI på maskinen, og service-nøglen kan ikke
køre DDL — derfor Management API'et. Bemærk at urllib bliver afvist af
Cloudflare (403, code 1010); curl går igennem, så det er det, der bruges.
"""
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENDPOINT = "https://api.supabase.com/v1/projects/{ref}/database/query"


def env(name: str) -> str:
    """Læser fra miljøet, ellers fra .env i repo-roden."""
    if os.environ.get(name):
        return os.environ[name]
    envfile = ROOT / ".env"
    if envfile.exists():
        for line in envfile.read_text(encoding="utf-8").splitlines():
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip("\"'")
    raise SystemExit(f"{name} mangler — sæt den i miljøet eller i .env")


def run(sql: str):
    ref = env("SUPABASE_PROJECT_REF")
    token = env("SUPABASE_ACCESS_TOKEN")
    out = subprocess.run(
        ["curl", "-s", "--max-time", "120", "-X", "POST", ENDPOINT.format(ref=ref),
         "-H", f"Authorization: Bearer {token}",
         "-H", "Content-Type: application/json",
         "--data-binary", "@-"],
        input=json.dumps({"query": sql}), capture_output=True, text=True,
    ).stdout
    try:
        result = json.loads(out)
    except json.JSONDecodeError:
        raise SystemExit(f"uventet svar fra Supabase:\n{out[:400]}")
    if isinstance(result, dict) and result.get("message"):
        raise SystemExit(f"SQL-fejl: {result['message']}")
    return result


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    sql = args[1] if args[0] == "-c" else pathlib.Path(args[0]).read_text(encoding="utf-8")
    result = run(sql)
    print(json.dumps(result, ensure_ascii=False, indent=1) if result else "ok — ingen rækker returneret")


if __name__ == "__main__":
    main()

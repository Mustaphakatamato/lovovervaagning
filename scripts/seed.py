#!/usr/bin/env python3
"""Lægger datasættet fra eu_data.py ind i Supabase.

    python3 scripts/seed.py

Idempotent: kan køres igen uden at duplikere. Rækker opdateres på (kategori,
navn) og referencer på (retsakt, rækkefølge) — der slettes ikke, så en retsakt
der får FÆRRE numre end før, efterlader den overskydende reference. Ret den i
SQL-editoren, hvis det sker.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from eu_data import ACTS, CATS  # noqa: E402
from eu_summaries import REVIEWED, SUMMARIES  # noqa: E402
from scripts.db import run  # noqa: E402


def lit(v):
    """SQL-literal. Enkeltanførselstegn i titler fordobles."""
    if v is None:
        return "null"
    return "'" + str(v).replace("'", "''") + "'"


def arr(values):
    """text[]-literal. Bygges som array[...] frem for '{...}', så teksten ikke
    skal escapes to gange."""
    if not values:
        return "null"
    return "array[" + ", ".join(lit(v) for v in values) + "]::text[]"


def js(value):
    """jsonb-literal."""
    if value is None:
        return "null"
    return lit(json.dumps(value, ensure_ascii=False)) + "::jsonb"


def main():
    stmts = []

    for order, (key, name, desc) in enumerate(CATS, start=1):
        stmts.append(
            f"insert into categories (key, name, description, sort_order) "
            f"values ({lit(key)}, {lit(name)}, {lit(desc)}, {order}) "
            f"on conflict (key) do update set "
            f"name = excluded.name, description = excluded.description, "
            f"sort_order = excluded.sort_order;"
        )

    n_acts = n_refs = 0
    for key, _, _ in CATS:
        for order, a in enumerate(ACTS[key], start=1):
            n_acts += 1
            stmts.append(
                f"insert into acts (category_key, name, act_type, status, procedure_ref, sort_order) "
                f"values ({lit(key)}, {lit(a['n'])}, {lit(a['t'])}, {lit(a['s'])}, "
                f"{lit(a.get('proc'))}, {order}) "
                f"on conflict (category_key, name) do update set "
                f"act_type = excluded.act_type, status = excluded.status, "
                f"procedure_ref = excluded.procedure_ref, sort_order = excluded.sort_order;"
            )
            for i, (year, num) in enumerate(a.get("ref", [])):
                n_refs += 1
                stmts.append(
                    f"insert into act_references (act_id, ord, year, number) "
                    f"select id, {i}, {year}, {num} from acts "
                    f"where category_key = {lit(key)} and name = {lit(a['n'])} "
                    f"on conflict (act_id, ord) do update set "
                    f"year = excluded.year, number = excluded.number;"
                )

    n_sum = 0
    for (key, name), su in SUMMARIES.items():
        n_sum += 1
        stmts.append(
            f"update acts set "
            f"subject = {lit(su['subject'])}, "
            f"scope = {lit(su['scope'])}, "
            f"duties = {arr(su['duties'])}, "
            f"timeline = {js(su['timeline'])}, "
            f"supervision_dk = {lit(su['supervision_dk'])}, "
            f"sanctions = {lit(su['sanctions'])}, "
            f"consultant_note = {arr(su['consultant_note'])}, "
            f"related = {arr(su['related'])}, "
            f"sources = {js(su['sources'])}, "
            f"summary_reviewed = {lit(REVIEWED)}::date "
            f"where category_key = {lit(key)} and name = {lit(name)};"
        )

    run("\n".join(stmts))
    print(f"indlæst: {len(CATS)} kategorier, {n_acts} retsakter, "
          f"{n_refs} referencer, {n_sum} opsummeringer")


if __name__ == "__main__":
    main()

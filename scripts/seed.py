#!/usr/bin/env python3
"""Lægger datasættet fra eu_data.py ind i Supabase.

    python3 scripts/seed.py

Idempotent: kan køres igen uden at duplikere. Rækker opdateres på (kategori,
navn) og referencer på (retsakt, rækkefølge) — der slettes ikke, så en retsakt
der får FÆRRE numre end før, efterlader den overskydende reference. Ret den i
SQL-editoren, hvis det sker.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from eu_data import ACTS, CATS  # noqa: E402
from scripts.db import run  # noqa: E402


def lit(v):
    """SQL-literal. Enkeltanførselstegn i titler fordobles."""
    if v is None:
        return "null"
    return "'" + str(v).replace("'", "''") + "'"


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

    run("\n".join(stmts))
    print(f"indlæst: {len(CATS)} kategorier, {n_acts} retsakter, {n_refs} referencer")


if __name__ == "__main__":
    main()

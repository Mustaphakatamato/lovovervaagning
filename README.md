# EU-lovgivning i den digitale sektor

En selvbærende oversigtsside over de EU-retsakter, der regulerer teknologi,
inddelt i tolv kategorier. Klik en kategori for at se hver forordning, hvert
direktiv og hver afgørelse med direkte link til teksten i EUR-Lex.

**104 retsakter** — 67 gældende, 28 i forhandling, 9 planlagte initiativer.

## Kom i gang

```sh
cp .env.example .env      # udfyld SUPABASE_ACCESS_TOKEN og SUPABASE_ANON_KEY
python3 build.py          # henter data fra Supabase og samler index.html
open index.html           # ingen server nødvendig
```

Uden `.env` falder byggeriet tilbage til `eu_data.py`, så et frisk klon kan bygge
siden uden adgang til databasen. De to kilder giver byte-identisk output.

`index.html` er én fil uden eksterne kald: fonten er indlejret som data-URI, og
datasættet ligger inline. Den kan derfor lægges bag en vilkårlig statisk host,
åbnes som `file://` eller sendes videre som en enkelt fil.

## Filer

| Fil | Rolle |
|---|---|
| `eu_data.py` | Datasættet — retsakter pr. kategori, plus CELEX- og URL-generatorerne |
| `eu_summaries.py` | Konsulentopsummeringerne. Redaktionelt indhold, versionsstyret så det kan reviewes |
| `eu-page-template.html` | Skabelonen med `__FONT__`- og `__DATA__`-pladsholdere |
| `build.py` | Samler skabelon + data + font til `index.html` og `eu_digital_acts.json` |
| `eu_digital_acts.json` | Genereret data alene — til import i en database |
| `index.html` | Bygget output. Genereret, men committed så siden kan hostes direkte |
| `fonts/` | Montserrat variable (SIL Open Font License 1.1) |
| `supabase/migrations/` | Skema, afledte funktioner, `acts_json`-udsigten og RLS |
| `scripts/db.py` | Kører SQL mod Supabase via Management API'et |
| `scripts/seed.py` | Lægger `eu_data.py` ind i databasen. Idempotent |

## Opsummeringer

En retsakt kan have en opsummering, som vises bag en **Opsummering**-knap på kortet.
Retsakter med en opsummering får badget *Uddybet*; resten er rene referencer, og
begge er gyldige tilstande — siden skal ikke se halvfærdig ud, fordi 100 retsakter
ikke er skrevet.

Indholdet forfattes i `eu_summaries.py` og lægges i databasen af `scripts/seed.py`.
Koden er forfatterformatet, databasen er den kopi siden læses fra. Det er valgt
fordi juridisk indhold skal kunne reviewes i en pull request, ikke rettes direkte
i en tabel.

Ni felter pr. opsummering:

| Felt | Indhold |
|---|---|
| `subject` | Lovens genstand, 1–2 sætninger |
| `scope` | Anvendelsesområde: hvem er omfattet, personelt og territorialt |
| `duties` | Kernekrav med artikelhenvisning |
| `timeline` | Vedtagelse, ikrafttræden og anvendelsesdatoer. Fremtidige datoer markeres på siden |
| `supervision_dk` | Dansk tilsynsmyndighed |
| `sanctions` | Bødeniveau |
| `consultant_note` | Hvad det betyder for et tech-hus: leverancer, faldgruber, rolleskift |
| `related` | Andre retsakter i datasættet. Bliver klikbare opslag |
| `sources` | Links til de kilder, indholdet er kontrolleret mod |

`summary_reviewed` sættes af `REVIEWED` i `eu_summaries.py` og vises som
*Kontrolleret <dato>* nederst i panelet. Feltet er ikke pynt: AI-forordningens
anvendelsesdatoer blev flyttet i juli 2026, og uden en kontroldato kan læseren
ikke vurdere, om teksten stadig holder. Ret datoen, når indholdet er gennemgået.

Skrevet indtil videre: GDPR og AI-forordningen.

## Database

Data ligger i Supabase-projektet **Lovovervågning** (`iuniokifmwxehrcrxrtn`).

```sh
python3 scripts/db.py supabase/migrations/0001_schema.sql   # opret/opdater skema
python3 scripts/seed.py                                     # indlæs datasættet
python3 scripts/db.py -c "select count(*) from acts"        # ad hoc-forespørgsel
```

Databasen holder kun rådata: årstal, nummer og type. CELEX-numre, referencelabels
og URL'er dannes af `celex()`, `act_label()` og `eurlex_url()` i SQL, så de ikke
kan komme i utakt med tallene. Udsigten `acts_json` leverer præcis den form,
skabelonen forventer — `build.py` omformer intet.

Der er hverken `psql`, `docker` eller Supabase CLI i brug: service-nøglen kan
ikke køre DDL, så migrationer går gennem Management API'ets query-endpoint.
`urllib` afvises af Cloudflare, derfor `curl`.

**Adgang.** RLS er slået til på alle tre tabeller med kun en læsepolicy for
`anon` og `authenticated` — offentlig EU-information læses af alle. Der findes
ingen skrivepolicy, så indlæsning kræver access-tokenet. `anon`-nøglen kan
udelukkende læse.

## Sådan tilføjes en retsakt

Ret i `eu_data.py` og kør `python3 build.py`. Et opslag ser sådan ud:

```python
dict(n="Cyber Resilience Act", t="R", s="neg", proc="2022/0272(COD)"),
dict(n="NIS 2 Directive",      t="L", s="law", ref=[(2022, 2555)]),
```

- `t` — retsakt-type til CELEX-opslaget: `R` forordning, `L` direktiv, `D` afgørelse
- `s` — status: `law` gældende ret, `neg` i forhandling, `plan` planlagt initiativ
- `ref` — `[(år, nummer)]` for vedtagne retsakter; giver et EUR-Lex-link
- `proc` — procedurenummer; giver et link til Europa-Parlamentets Legislative Observatory

CELEX-nummeret dannes som sektor `3` + år + typebogstav + firecifret nummer, fx
`32022L2555`. Referencelabels får korrekt traktatsuffiks (EEC / EC / EU) ud fra året.

## Datagrundlag og forbehold

Kategoriinddelingen og udvalget af retsakter følger Bruegel og kaizenner.eu,
*Overview of EU Legislation in the Digital Sector*. Den er valgt frem for EU's
egne taksonomier, fordi hverken EuroVoc (21 domæner) eller Europa-Parlamentets
emneklassifikation (9 kapitler) har et digitalt niveau — digitalt er et tværsnit
af traktatens politikområder og kan derfor ikke hentes som én kategori.

Tre forbehold, der bør stå ved en ekstern brug af siden:

1. **Links er genereret, ikke verificeret.** CELEX-numrene konstrueres ud fra
   nummer og type. EUR-Lex afviser automatiserede kald, så de er ikke efterprøvet
   maskinelt. Kontrollér et link, før det citeres — særligt de ældste retsakter.
2. **Datasættet stopper i 2024.** Kildetabellen er et snapshot. Retsakter vedtaget
   efter 2024 mangler, herunder simplificerings- og omnibus-sagerne fra 2025–26.
3. **Kategorien er redaktionel.** En retsakt kan sagligt høre i flere kategorier.
   Hver er placeret ét sted, som i kildetabellen.

## Design

Devoteams designsystem: Montserrat i alle størrelser, Red Poppy `#f8485e` alene
som accent, Dark Grey `#3c3c3a` til al tekst — aldrig sort. Status vises på
brandets Red Poppy-intensitetsskala frem for flere kulører. Siden har både lys og
mørk tilstand og følger systemets tema.

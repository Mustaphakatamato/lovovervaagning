# EU-lovgivning i den digitale sektor

En selvbærende oversigtsside over de EU-retsakter, der regulerer teknologi,
inddelt i tolv kategorier. Klik en kategori for at se hver forordning, hvert
direktiv og hver afgørelse — og klik en retsakt for at få dens egen side med
anvendelsesdato, dansk implementering, tilsyn og link til teksten i EUR-Lex.

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
| `supabase/migrations/` | Skema, afledte funktioner (`celex`, `slug`, …), `acts_json`-udsigten og RLS |
| `scripts/db.py` | Kører SQL mod Supabase via Management API'et |
| `scripts/seed.py` | Lægger `eu_data.py` ind i databasen. Idempotent |

## Aktsider og adresser

Hver retsakt har sin egen side på `#akt/<slug>` — fx `index.html#akt/gdpr`.
Sluggen afledes af navnet: slutter navnet på en forkortelse i parentes, bruges
den (`(GDPR)` → `gdpr`), ellers kebab-case af hele navnet
(`Cyber Resilience Act` → `cyber-resilience-act`). `slug()` findes både i SQL og
i `eu_data.py`, som `celex()` og `eurlex_url()` gør.

CELEX virker som alias, så `#akt/32016R0679` fører til samme side. Det er ikke
pynt: en slug afledt af navnet dør, hvis navnet rettes, og så dør de delte
links. CELEX-nummeret ændrer sig aldrig. `build.py` afbryder ved slug-kollision,
fordi to retsakter på samme adresse ville sende læseren til den forkerte side,
uden at noget så galt ud.

Sidens rækkefølge er dens indhold: identitet, dernæst faktalaget — *Gælder fra i
EU* og *Dansk implementering* — og først derefter det redaktionelle. Et felt, der
mangler, skriver *Ikke registreret* eller *Ikke kortlagt endnu*: en tom kasse
læses som en fejl på siden. Retsakter uden opsummering skriver det selv frem for
at se halvfærdige ud.

Siden er stadig én fil. Routingen er hash-baseret, så deep links, tilbage-knappen
og `file://` virker uden hosting — og fonten skal ikke ud i en delt fil, som 104
selvstændige HTML-filer ville kræve (688 KB TTF, 918 KB base64, pr. side).

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
| `related` | Andre retsakter. Bliver links til deres egne sider; navne uden for datasættet vises som ren tekst |
| `sources` | Links til de kilder, indholdet er kontrolleret mod |

`summary_reviewed` sættes af `REVIEWED` i `eu_summaries.py` og vises som
*Kontrolleret <dato>* nederst i panelet. Feltet er ikke pynt: AI-forordningens
anvendelsesdatoer blev flyttet i juli 2026, og uden en kontroldato kan læseren
ikke vurdere, om teksten stadig holder. Ret datoen, når indholdet er gennemgået.

Skrevet indtil videre: GDPR og AI-forordningen.

## Dansk implementering

En retsakt kan derudover have en dansk implementeringsstatus: er den direkte
gældende, gennemført ved en dansk lov, eller afventer den stadig dansk
gennemførelse — og hvilken/hvilke danske myndigheder fører tilsyn. Feltet er
uafhængigt af opsummeringen ovenfor: en forordning kan vise dansk status uden
nogensinde at få en fuld konsulentopsummering.

| Felt | Indhold |
|---|---|
| `dk_status` | `direct` (direkte gældende), `transposed` (gennemført), `pending` (afventer), eller `unmapped` (ikke undersøgt — default) |
| `dk_instrument` | Navnet på den danske lov/bekendtgørelse, hvis der findes én. Tomt for rene forordninger |
| `dk_instrument_ref` | Den officielle betegnelse, fx "Lov nr. 502 af 23. maj 2018" |
| `dk_instrument_url` | Link til retsinformation.dk |
| `dk_timeline` | Danske milepæle, samme form som `timeline`: `[{date, label, note}]` |
| `dk_authorities` | Liste af `{name, url, scope}` — flere myndigheder pr. retsakt understøttes, hver med sit afgrænsede ansvarsområde |

Skrives i `eu_summaries.py` sammen med resten af opsummeringen og lægges i
databasen af `scripts/seed.py`, som også holder tabellerne `authorities` og
`act_authorities` ajour. `unmapped` er default for alle retsakter, der endnu
ikke er research'et — status vises hverken som badge eller i panelet, før den
er sat til noget andet.

Skrevet indtil videre: GDPR og AI-forordningen.

## Database

Data ligger i Supabase-projektet **Lovovervågning** (`iuniokifmwxehrcrxrtn`).

```sh
for m in supabase/migrations/*.sql; do python3 scripts/db.py "$m"; done
python3 scripts/seed.py                                     # indlæs datasættet
python3 scripts/db.py -c "select count(*) from acts"        # ad hoc-forespørgsel
```

Databasen holder kun rådata: årstal, nummer og type. CELEX-numre, referencelabels,
URL'er og slugs dannes af `celex()`, `act_label()`, `eurlex_url()` og `slug()` i
SQL, så de ikke kan komme i utakt med det, de bygger på. Udsigten `acts_json`
leverer præcis den form, skabelonen forventer — `build.py` omformer intet.

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
- `app` / `appn` — EU-anvendelsesdato som `ÅÅÅÅ-MM-DD`, og et forbehold når
  datoerne er trappede, som AI-forordningens fem. Ikke det samme som
  `dk_timeline`: `app` er hvornår retsakten gælder i EU, `dk_timeline` er hvad
  Danmark har gjort ved den

CELEX-nummeret dannes som sektor `3` + år + typebogstav + firecifret nummer, fx
`32022L2555`. Referencelabels får korrekt traktatsuffiks (EEC / EC / EU) ud fra året.

## Datagrundlag og forbehold

Kategoriinddelingen og udvalget af retsakter følger Bruegel og kaizenner.eu,
*Overview of EU Legislation in the Digital Sector*. Den er valgt frem for EU's
egne taksonomier, fordi hverken EuroVoc (21 domæner) eller Europa-Parlamentets
emneklassifikation (9 kapitler) har et digitalt niveau — digitalt er et tværsnit
af traktatens politikområder og kan derfor ikke hentes som én kategori.

Fire forbehold, der bør stå ved en ekstern brug af siden:

1. **Links er genereret, ikke verificeret.** CELEX-numrene konstrueres ud fra
   nummer og type. EUR-Lex afviser automatiserede kald, så de er ikke efterprøvet
   maskinelt. Kontrollér et link, før det citeres — særligt de ældste retsakter.
2. **Datasættet stopper i 2024.** Kildetabellen er et snapshot. Retsakter vedtaget
   efter 2024 mangler, herunder simplificerings- og omnibus-sagerne fra 2025–26.
3. **Kategorien er redaktionel.** En retsakt kan sagligt høre i flere kategorier.
   Hver er placeret ét sted, som i kildetabellen.
4. **Aktsidernes faktalag er næsten tomt.** Anvendelsesdato og dansk
   implementering er indtil videre kun udfyldt for GDPR og AI-forordningen, hvor
   de er kontrolleret mod kilderne. De øvrige 102 sider skriver *Ikke
   registreret* og *Ikke kortlagt endnu* — det betyder "ikke slået op", ikke
   "findes ikke". Udfyldningen kræver et opslag pr. retsakt.

## Design

Devoteams designsystem: Montserrat i alle størrelser, Red Poppy `#f8485e` alene
som accent, Dark Grey `#3c3c3a` til al tekst — aldrig sort. Status vises på
brandets Red Poppy-intensitetsskala frem for flere kulører. Siden har både lys og
mørk tilstand og følger systemets tema.

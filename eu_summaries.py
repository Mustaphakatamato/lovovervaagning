# Konsulentopsummeringer pr. retsakt.
#
# Indholdet ligger som kode og ikke kun i databasen, fordi det er redaktionelt
# arbejde, der skal kunne reviewes i en pull request. scripts/seed.py lægger det
# ind i Supabase, som er den kopi siden læses fra.
#
# Nøglen er (kategori, navn) og skal matche eu_data.py præcist.
#
# REVIEWED er datoen, indholdet sidst blev holdt op mod kilderne. Den vises på
# siden. Retsakter ældes — AI-forordningens datoer flyttede sig i juli 2026 — og
# uden datoen kan læseren ikke vurdere, om teksten stadig holder.

REVIEWED = "2026-09-07"

SUMMARIES = {

("data", "General Data Protection Regulation (GDPR)"): dict(
    subject=(
        "Regulerer al behandling af personoplysninger — hele livscyklussen fra "
        "indsamling til sletning. Det er ikke en it-sikkerhedslov, men en lov om, "
        "hvornår det overhovedet er lovligt at behandle oplysninger om en "
        "identificerbar fysisk person, og hvilke rettigheder personen har imens."
    ),
    scope=(
        "Helt eller delvist automatiseret behandling samt manuelle registre. "
        "Omfatter dataansvarlige og databehandlere etableret i EU, og virksomheder "
        "uden for EU når de udbyder varer eller tjenester til, eller overvåger "
        "adfærden hos, personer i EU (art. 3). Undtaget: rent private aktiviteter, "
        "og politiets og anklagemyndighedens behandling, som er dækket af "
        "retshåndhævelsesdirektivet."
    ),
    duties=[
        "Behandlingsgrundlag for hver enkelt behandling (art. 6). Følsomme oplysninger kræver derudover en undtagelse i art. 9",
        "Principperne i art. 5 skal kunne dokumenteres: formålsbegrænsning, dataminimering, opbevaringsbegrænsning, ansvarlighed",
        "Den registreredes rettigheder besvares inden for én måned (art. 12–22): indsigt, sletning, dataportabilitet, indsigelse",
        "Fortegnelse over behandlingsaktiviteter (art. 30) og databehandleraftale med hver leverandør (art. 28)",
        "Konsekvensanalyse (DPIA) før behandling med høj risiko (art. 35). Databeskyttelsesrådgiver er obligatorisk for offentlige myndigheder (art. 37)",
        "Sikkerhedsforanstaltninger efter risiko (art. 32) og anmeldelse af brud til Datatilsynet inden 72 timer (art. 33)",
        "Overførsel til tredjeland kræver et overførselsgrundlag i kap. V — tilstrækkelighedsafgørelse eller standardkontrakter med tilhørende overførselsvurdering",
        "Databeskyttelse gennem design og standardindstillinger (art. 25) — et krav til systemarkitekturen, ikke kun til politikker",
    ],
    timeline=[
        {"date": "2016-04-27", "label": "Vedtaget"},
        {"date": "2016-05-24", "label": "I kraft"},
        {"date": "2018-05-25", "label": "Anvendes", "note": "Ophævede samtidig databeskyttelsesdirektivet 95/46/EF"},
        {"date": "—", "label": "Under ændring",
         "note": "Digital Omnibus (2025/0360(COD)) er i udvalgsbehandling og vil ændre dele af forordningen. Ikke vedtaget."},
    ],
    supervision_dk=(
        "Datatilsynet. Suppleret af databeskyttelsesloven (lov nr. 502 af 23. maj 2018), "
        "som udnytter forordningens nationale råderum. Vigtigt for forventningsafstemning: "
        "Datatilsynet kan ikke selv udstede bøder — tilsynet indgiver politianmeldelse, og "
        "bøden fastsættes af domstolene. Dansk håndhævelse er derfor langsommere og "
        "sjældnere end i lande med administrative bøder."
    ),
    sanctions=(
        "Op til 20 mio. EUR eller 4 % af den samlede globale årsomsætning, hvad der er "
        "højest (art. 83, stk. 5). Lavere niveau: 10 mio. EUR eller 2 %. I Danmark går "
        "bøder gennem straffesag, og de udmålte beløb har hidtil ligget langt under loftet."
    ),
    consultant_note=[
        "Udløser konkrete leverancer: DPIA'er, fortegnelser, databehandleraftaler, sletteregler i systemer, klassifikation af datatyper og overførselsvurderinger ved cloud",
        "Art. 25 gør databeskyttelse til et arkitekturkrav. Det er her et tech-hus adskiller sig fra en advokat — kravet skal omsættes til datamodeller, adgangsstyring og opbevaringspolitikker i selve løsningen",
        "Hyppigste faldgrube hos offentlige kunder: cloudleverandøren behandler data til egne formål og bliver dermed selvstændig dataansvarlig, uden at det er afdækket i aftalen",
        "Ved brug af amerikanske hyperscalere er overførselsvurderingen næsten altid det svage led i dokumentationen, også efter tilstrækkelighedsafgørelsen for EU-US Data Privacy Framework",
        "Datatilsynets sag om Chromebooks i Helsingør Kommune er referencesagen for kommunal cloudbrug og bør kendes, før man rådgiver en kommune",
    ],
    related=[
        "Law Enforcement Directive",
        "ePrivacy Regulation",
        "Data Governance Act (DGA)",
        "European Health Data Space",
        "Digital Omnibus (Omnibus VII)",
        "AI Act",
    ],
    sources=[
        {"label": "Datatilsynet", "url": "https://www.datatilsynet.dk"},
        {"label": "Databeskyttelsesloven på retsinformation.dk",
         "url": "https://www.retsinformation.dk/eli/lta/2018/502"},
    ],
),

("trust", "AI Act"): dict(
    subject=(
        "Harmoniserede regler for udvikling, markedsføring og brug af AI-systemer i EU. "
        "Opbygget som produktsikkerhedslovgivning, ikke som databeskyttelse: kravene "
        "følger systemets risikoklasse og anvendelse, ikke teknologien i sig selv. "
        "Samme model som CE-mærkning af maskiner."
    ),
    scope=(
        "Gælder udbydere, ibrugtagere, importører og distributører — og også aktører uden "
        "for EU, når systemets output anvendes i EU. Fire risikoniveauer: uacceptabel "
        "risiko er forbudt (art. 5), høj risiko udløser det fulde kravsæt (art. 6 med "
        "bilag I og III), begrænset risiko udløser alene transparenspligter (art. 50), og "
        "minimal risiko er ureguleret. AI-modeller til almen brug har deres eget regime "
        "(kap. V) med skærpede krav, når modellen har systemisk risiko."
    ),
    duties=[
        "Højrisiko, udbyder: risikostyringssystem (art. 9), datastyring og datakvalitet (art. 10), teknisk dokumentation (art. 11 og bilag IV), automatisk logning (art. 12)",
        "Højrisiko, udbyder: gennemsigtighed over for ibrugtager (art. 13), menneskeligt tilsyn (art. 14), nøjagtighed, robusthed og cybersikkerhed (art. 15)",
        "Højrisiko, udbyder: kvalitetsstyringssystem (art. 17), overensstemmelsesvurdering (art. 43), CE-mærkning og registrering i EU-databasen (art. 49)",
        "Højrisiko, ibrugtager: brug efter brugsanvisningen, menneskeligt tilsyn, logopbevaring og underretning ved hændelser (art. 26)",
        "Offentlige myndigheder som ibrugtager: konsekvensanalyse for grundlæggende rettigheder, FRIA, før første brug af et højrisikosystem (art. 27)",
        "Alle risikoniveauer: AI-kompetencer hos personale, der bruger systemerne (art. 4)",
        "Begrænset risiko: oplysning om interaktion med AI og mærkning af syntetisk indhold (art. 50)",
    ],
    timeline=[
        {"date": "2024-07-12", "label": "Offentliggjort i EU-Tidende"},
        {"date": "2024-08-01", "label": "I kraft"},
        {"date": "2025-02-02", "label": "Anvendes: forbud", "note": "Forbudt praksis (art. 5) og AI-kompetencer (art. 4)"},
        {"date": "2025-08-02", "label": "Anvendes: modeller til almen brug",
         "note": "Kap. V, governance-strukturen og medlemsstaternes sanktionsbestemmelser"},
        {"date": "2026-08-02", "label": "Anvendes: transparens",
         "note": "Art. 50. Gælder nu — blev IKKE udskudt af Digital Omnibus"},
        {"date": "2027-12-02", "label": "Anvendes: høj risiko efter bilag III",
         "note": "Udskudt fra 2. august 2026 ved forordning (EU) 2026/1744"},
        {"date": "2028-08-02", "label": "Anvendes: høj risiko i regulerede produkter",
         "note": "Bilag I. Udskudt fra 2. august 2027 ved samme ændringsforordning"},
    ],
    supervision_dk=(
        "Splittet og endnu ikke færdigt. Digitaliseringsstyrelsen er bemyndigende myndighed, "
        "centralt kontaktpunkt og markedsovervågningsmyndighed for forbudt praksis efter "
        "art. 5, stk. 1, litra a–c og e–f. Datatilsynet fører tilsyn med litra d og g. "
        "Domstolsstyrelsen dækker domstolenes egen administrative brug. "
        "Hvem der fører tilsyn med højrisikosystemer og transparenspligterne var pr. "
        "september 2026 stadig uafklaret ifølge Digitaliseringsstyrelsens egen FAQ. "
        "AI-modeller til almen brug overvåges af Kommissionens AI-kontor, ikke nationalt."
    ),
    sanctions=(
        "Op til 35 mio. EUR eller 7 % af den globale årsomsætning for forbudt praksis. "
        "15 mio. EUR eller 3 % for de fleste øvrige pligter, herunder højrisikokravene. "
        "7,5 mio. EUR eller 1 % for urigtige oplysninger til myndighederne. For små og "
        "mellemstore virksomheder gælder det laveste af de to beløb, ikke det højeste."
    ),
    consultant_note=[
        "De fleste danske kunder er ibrugtagere, ikke udbydere. Pligterne er færre, men reelle: art. 26, og for offentlige myndigheder art. 27 FRIA, som ingen har rutine i endnu",
        "Man bliver selv udbyder, hvis man sætter sit eget navn på et system eller ændrer et højrisikosystem væsentligt (art. 25). Det er det hyppigste utilsigtede rolleskift — finetuning af en model til en kunde kan flytte hele kravsættet over på leverandøren",
        "Udskydelsen til december 2027 fjerner hastværket på højrisiko-compliance, men ikke på art. 50-transparens og art. 4 AI-kompetence, som gælder nu. Kunder, der læser overskrifterne om udskydelsen, tror ofte at alt er udskudt",
        "Udløser konkrete leverancer: AI-inventar, risikoklassifikation pr. system, FRIA'er, dokumentationspakker efter bilag IV, menneskeligt tilsyn indbygget i procesdesign, og kravformuleringer til leverandører i udbudsmateriale",
        "Overlapper GDPR, men falder ikke sammen med den: et system kan være lovligt efter AI-forordningen og ulovligt efter GDPR. To vurderinger, ikke én",
    ],
    related=[
        "General Data Protection Regulation (GDPR)",
        "Cyber Resilience Act",
        "Product Liability Directive (PLD)",
        "Machinery Regulation",
        "Cloud and AI Development Act",
        "AI Liability Directive",
    ],
    sources=[
        {"label": "Procedurefil i OEIL",
         "url": "https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2021/0106(COD)"},
        {"label": "Digitaliseringsstyrelsens tilsynsside",
         "url": "https://digst.dk/tilsyn/ai-forordningen/faq-om-ai-forordningen/"},
        {"label": "Datatilsynet om AI-forordningen", "url": "https://www.datatilsynet.dk"},
        {"label": "Ændringsforordning (EU) 2026/1744",
         "url": "https://eur-lex.europa.eu/legal-content/DA/TXT/?uri=CELEX:32026R1744"},
    ],
),

}

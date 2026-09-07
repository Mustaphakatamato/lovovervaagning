# Datasæt: EU-lovgivning i den digitale sektor.
# Kilde: Bruegel / kaizenner.eu "Overview of EU Legislation in the Digital Sector".
# t = retsakt-type til CELEX-opslag: R=forordning, L=direktiv, D=afgørelse
# s = status: law (gældende) | neg (i forhandling) | plan (planlagt initiativ)
# ref = [(år, nummer)] for vedtagne retsakter | proc = procedurenummer

CATS = [
 ("research", "Research & Innovation", "Programmer og instrumenter der finansierer digital forskning og udvikling."),
 ("industrial", "Industrial Policy", "Industriel kapacitet: halvledere, HPC, råstoffer, digitale mål."),
 ("connectivity", "Connectivity", "Frekvenser, bredbånd, elektronisk kommunikation, roaming, domæner."),
 ("data", "Data & Privacy", "Persondata, ikke-personhenførbare data, dataadgang og interoperabilitet."),
 ("ipr", "IPR", "Ophavsret til databaser, design, patenter og forretningshemmeligheder."),
 ("cyber", "Cybersecurity", "Netværkssikkerhed, produktsikkerhed i software, beredskab."),
 ("law", "Law Enforcement", "Retshåndhævelse, e-bevis, ulovligt indhold, betalingssvindel."),
 ("trust", "Trust & Safety", "AI, produktansvar, produktsikkerhed, eID og digital tillid."),
 ("ecom", "E-commerce & Consumer Protection", "Onlinehandel, forbrugerrettigheder, platformsansvar, markedsføring."),
 ("comp", "Competition", "Konkurrenceregler, gatekeepers, markedsovervågning, platformsarbejde."),
 ("media", "Media", "Ophavsret, audiovisuelle tjenester, mediefrihed, portabilitet."),
 ("finance", "Finance", "Betalinger, kryptoaktiver, operationel modstandskraft, digital euro, moms."),
]

ACTS = {
"research": [
 dict(n="Digital Europe Programme Regulation", t="R", s="law", ref=[(2021,694)]),
 dict(n="Horizon Europe Regulation", t="R", s="law", ref=[(2021,695),(2021,764)]),
 dict(n="Regulation on a pilot regime for distributed ledger technology market infrastructures", t="R", s="law", ref=[(2022,858)]),
],
"industrial": [
 dict(n="Recovery and Resilience Facility Regulation", t="R", s="law", ref=[(2021,241)]),
 dict(n="InvestEU Programme Regulation", t="R", s="law", ref=[(2021,523)]),
 dict(n="Connecting Europe Facility Regulation", t="R", s="law", ref=[(2021,1153)]),
 dict(n="Regulation on the High Performance Computing Joint Undertaking", t="R", s="law", ref=[(2021,1173)]),
 dict(n="Regulation on Joint Undertakings under Horizon Europe", t="R", s="law", ref=[(2021,2085)], proc="2022/0033(NLE)"),
 dict(n="Decision on a path to the Digital Decade", t="D", s="law", ref=[(2022,2481)]),
 dict(n="European Chips Act", t="R", s="neg", proc="2022/0032(COD)"),
 dict(n="European Critical Raw Materials Act", t="R", s="neg", proc="2023/0079(COD)"),
 dict(n="Strategic Technologies for Europe Platform (STEP)", t="R", s="neg", proc="2023/0199(COD)"),
],
"connectivity": [
 dict(n="Frequency Bands Directive", t="L", s="law", ref=[(1987,372)]),
 dict(n="Radio Spectrum Decision", t="D", s="law", ref=[(2002,676)]),
 dict(n="Broadband Cost Reduction Directive", t="L", s="law", ref=[(2014,61)], proc="2023/0046(COD)"),
 dict(n="Open Internet Access Regulation", t="R", s="law", ref=[(2015,2120)]),
 dict(n="European Electronic Communications Code Directive (EECC)", t="L", s="law", ref=[(2018,1972)]),
 dict(n="Roaming Regulation", t="R", s="law", ref=[(2022,612)]),
 dict(n="Regulation on the Union Secure Connectivity Programme", t="R", s="law", ref=[(2023,588)]),
 dict(n=".eu top-level domain Regulation", t="R", s="law", ref=[(2019,517)]),
 dict(n="New radio spectrum policy programme (RSPP 2.0)", t="R", s="plan"),
 dict(n="Telecoms Act / Fair Share initiative", t="R", s="plan"),
],
"data": [
 dict(n="General Data Protection Regulation (GDPR)", t="R", s="law", ref=[(2016,679)]),
 dict(n="Regulation on the protection of personal data processed by EU institutions, bodies, offices and agencies", t="R", s="law", ref=[(2018,1725)]),
 dict(n="Regulation on the free flow of non-personal data", t="R", s="law", ref=[(2018,1807)]),
 dict(n="Open Data Directive (PSI)", t="L", s="law", ref=[(2019,1024)]),
 dict(n="Data Governance Act (DGA)", t="R", s="law", ref=[(2022,868)]),
 dict(n="ePrivacy Regulation", t="R", s="neg", proc="2017/0003(COD)"),
 dict(n="European Data Act", t="R", s="neg", proc="2022/0047(COD)"),
 dict(n="European Health Data Space", t="R", s="neg", proc="2022/0140(COD)"),
 dict(n="Regulation on data collection and sharing for short-term rental", t="R", s="neg", proc="2022/0358(COD)"),
 dict(n="Harmonisation of GDPR enforcement", t="R", s="neg", proc="2023/0202(COD)"),
 dict(n="Interoperable Europe Act", t="R", s="neg", proc="2022/0379(COD)"),
 dict(n="Access to vehicle data, functions and resources", t="R", s="plan"),
 dict(n="GreenData4All", t="R", s="plan"),
],
"ipr": [
 dict(n="Database Directive", t="L", s="law", ref=[(1996,9)]),
 dict(n="Community Design Regulation", t="R", s="law", ref=[(2002,6)], proc="2022/0391(COD)"),
 dict(n="Enforcement Directive (IPR)", t="L", s="law", ref=[(2004,48)]),
 dict(n="Directive on the protection of trade secrets", t="L", s="law", ref=[(2016,943)]),
 dict(n="Standard essential patents", t="R", s="neg", proc="2023/0133(COD)"),
 dict(n="Design Directive", t="L", s="neg", proc="2022/0392(COD)"),
 dict(n="Compulsory licensing of patents", t="R", s="neg", proc="2023/0129(COD)"),
],
"cyber": [
 dict(n="Cybersecurity Act", t="R", s="law", ref=[(2019,881)]),
 dict(n="Regulation establishing the European Cybersecurity Competence Centre", t="R", s="law", ref=[(2021,887)]),
 dict(n="NIS 2 Directive", t="L", s="law", ref=[(2022,2555)]),
 dict(n="Information Security Regulation", t="R", s="neg", proc="2022/0084(COD)"),
 dict(n="Cybersecurity Regulation", t="R", s="neg", proc="2022/0085(COD)"),
 dict(n="Cyber Resilience Act", t="R", s="neg", proc="2022/0272(COD)"),
 dict(n="Cyber Solidarity Act", t="R", s="neg", proc="2023/0109(COD)"),
],
"law": [
 dict(n="Law Enforcement Directive", t="L", s="law", ref=[(2016,680)]),
 dict(n="Directive on combating fraud and counterfeiting of non-cash means of payment", t="L", s="law", ref=[(2019,713)]),
 dict(n="Regulation on addressing the dissemination of terrorist content online", t="R", s="law", ref=[(2021,784)]),
 dict(n="Temporary CSAM Regulation", t="R", s="law", ref=[(2021,1232)], proc="2022/0155(COD)"),
 dict(n="E-evidence Regulation", t="R", s="neg", proc="2018/0108(COD)"),
 dict(n="Digitalisation of travel documents", t="R", s="plan"),
],
"trust": [
 dict(n="Product Liability Directive (PLD)", t="L", s="law", ref=[(1985,374)], proc="2022/0302(COD)"),
 dict(n="European Standardisation Regulation", t="R", s="law", ref=[(2012,1025)]),
 dict(n="Radio Equipment Directive (RED)", t="L", s="law", ref=[(2014,53)]),
 dict(n="eIDAS Regulation", t="R", s="law", ref=[(2014,910)], proc="2021/0136(COD)"),
 dict(n="Regulation establishing a Single Digital Gateway", t="R", s="law", ref=[(2018,1724)]),
 dict(n="General Product Safety Regulation", t="R", s="law", ref=[(2023,988)]),
 dict(n="Machinery Regulation", t="R", s="law", ref=[(2023,1230)]),
 dict(n="AI Act", t="R", s="neg", proc="2021/0106(COD)"),
 dict(n="Eco-design Regulation", t="R", s="neg", proc="2022/0095(COD)"),
 dict(n="AI Liability Directive", t="L", s="neg", proc="2022/0303(COD)"),
],
"ecom": [
 dict(n="Unfair Contract Terms Directive (UCTD)", t="L", s="law", ref=[(1993,13)]),
 dict(n="E-commerce Directive", t="L", s="law", ref=[(2000,31)]),
 dict(n="Unfair Commercial Practices Directive (UCPD)", t="L", s="law", ref=[(2005,29)]),
 dict(n="Consumer Rights Directive (CRD)", t="L", s="law", ref=[(2011,83)]),
 dict(n="e-Invoicing Directive", t="L", s="law", ref=[(2014,55)]),
 dict(n="Geo-blocking Regulation", t="R", s="law", ref=[(2018,302)]),
 dict(n="Digital Content Directive", t="L", s="law", ref=[(2019,770)]),
 dict(n="Directive on certain aspects concerning contracts for the sale of goods", t="L", s="law", ref=[(2019,771)]),
 dict(n="Digital Services Act (DSA)", t="R", s="law", ref=[(2022,2065)]),
 dict(n="Political Advertising Regulation", t="R", s="neg", proc="2021/0381(COD)"),
 dict(n="Right to Repair Directive", t="L", s="neg", proc="2023/0083(COD)"),
 dict(n="Multimodal digital mobility services (MDMS)", t="R", s="plan"),
 dict(n="Consumer protection: strengthened enforcement cooperation", t="R", s="plan"),
 dict(n="Consumer rights: adapting ADR to digital markets", t="L", s="plan"),
],
"comp": [
 dict(n="Technology Transfer Block Exemption Regulation", t="R", s="law", ref=[(2014,316)]),
 dict(n="Company Law Directive", t="L", s="law", ref=[(2017,1132)], proc="2023/0089(COD)"),
 dict(n="Market Surveillance Regulation", t="R", s="law", ref=[(2019,1020)]),
 dict(n="Platform-to-Business Regulation (P2B)", t="R", s="law", ref=[(2019,1150)]),
 dict(n="Vertical Block Exemption Regulation (VBER)", t="R", s="law", ref=[(2022,720)]),
 dict(n="Digital Markets Act (DMA)", t="R", s="law", ref=[(2022,1925)]),
 dict(n="Regulation on foreign subsidies distorting the internal market", t="R", s="law", ref=[(2022,2560)]),
 dict(n="Horizontal Block Exemption Regulations (HBER)", t="R", s="law", ref=[(2023,1066),(2023,1067)]),
 dict(n="Platform Work Directive", t="L", s="neg", proc="2021/0414(COD)"),
 dict(n="Single Market Emergency Instrument (SMEI)", t="R", s="neg", proc="2022/0278(COD)"),
],
"media": [
 dict(n="Satellite and Cable I Directive", t="L", s="law", ref=[(1993,83)]),
 dict(n="Information Society Directive (InfoSoc)", t="L", s="law", ref=[(2001,29)]),
 dict(n="Audiovisual Media Services Directive (AVMSD)", t="L", s="law", ref=[(2010,13)]),
 dict(n="Portability Regulation", t="R", s="law", ref=[(2017,1128)]),
 dict(n="Satellite and Cable II Directive", t="L", s="law", ref=[(2019,789)]),
 dict(n="Copyright Directive (DSM)", t="L", s="law", ref=[(2019,790)]),
 dict(n="European Media Freedom Act", t="R", s="neg", proc="2022/0277(COD)"),
],
"finance": [
 dict(n="Common VAT system Directive", t="L", s="law", ref=[(2006,112)], proc="2022/0407(CNS)"),
 dict(n="Payment Services Directive 2 (PSD2)", t="L", s="law", ref=[(2015,2366)], proc="2023/0209(COD)"),
 dict(n="Digital Operational Resilience Act (DORA)", t="R", s="law", ref=[(2022,2554)]),
 dict(n="Markets in Crypto-Assets Regulation (MiCA)", t="R", s="law", ref=[(2023,1114)]),
 dict(n="Financial Data Access Regulation (FiDA)", t="R", s="neg", proc="2023/0205(COD)"),
 dict(n="Digital euro Regulation", t="R", s="neg", proc="2023/0212(COD)"),
 dict(n="Payment Services Regulation", t="R", s="neg", proc="2023/0210(COD)"),
 dict(n="Revision of the Late Payments Directive", t="L", s="plan"),
],
}

def celex(t, year, num):
    """CELEX-nummer: sektor 3 + år + type-bogstav + 4-cifret nummer."""
    return f"3{year}{t}{num:04d}"

def eurlex_url(t, year, num):
    return f"https://eur-lex.europa.eu/legal-content/DA/TXT/?uri=CELEX:{celex(t, year, num)}"

def oeil_url(proc):
    return f"https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference={proc}"

def label(t, year, num):
    """Reference som den officielt skrives, med korrekt traktat-suffiks."""
    suffix = "EEC" if year <= 1993 else "EC" if year < 2010 else "EU"
    word = {"R": "Regulation", "L": "Directive", "D": "Decision"}[t]
    if t == "L":
        core = f"{str(year)[2:]}/{num}" if year < 2000 else f"{year}/{num}"
        return f"{word} {core}/{suffix}" if year < 2015 else f"{word} ({suffix}) {year}/{num}"
    # forordninger og afgørelser nummereres nummer-før-år indtil 2015
    if year < 2015:
        return f"{word} ({suffix}) No {num}/{year}"
    return f"{word} ({suffix}) {year}/{num}"

def build():
    out = []
    for key, name, desc in CATS:
        items = []
        for a in ACTS[key]:
            refs = [
                {"label": label(a["t"], y, n), "celex": celex(a["t"], y, n), "url": eurlex_url(a["t"], y, n)}
                for y, n in a.get("ref", [])
            ]
            items.append({
                "name": a["n"], "type": a["t"], "status": a["s"], "refs": refs,
                "proc": a.get("proc"), "procUrl": oeil_url(a["proc"]) if a.get("proc") else None,
            })
        out.append({"key": key, "name": name, "desc": desc, "acts": items})
    return out

if __name__ == "__main__":
    import json, collections
    data = build()
    c = collections.Counter(a["status"] for cat in data for a in cat["acts"])
    print("kategorier:", len(data), "retsakter:", sum(len(x["acts"]) for x in data), dict(c))
    for cat in data:
        print(f"  {cat['name']:36} {len(cat['acts']):2}")
    json.dump(data, open("eu_digital_acts.json", "w"), ensure_ascii=False, indent=1)

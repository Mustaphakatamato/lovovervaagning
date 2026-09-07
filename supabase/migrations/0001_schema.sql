-- Lovovervågning — skema for EU-retsakter i den digitale sektor.
--
-- Databasen holder kun rådata: årstal, nummer og type. CELEX-numre,
-- referencelabels og URL'er er afledt og dannes af funktionerne nedenfor, så
-- de aldrig kan komme i utakt med de tal, de bygger på.

create table if not exists categories (
  key         text     primary key,
  name        text     not null,
  description text     not null default '',
  sort_order  smallint not null
);

comment on table categories is
  'De tolv kategorier. Følger Bruegel/kaizenner.eu, Overview of EU Legislation in the Digital Sector.';

do $$ begin
  create type act_type   as enum ('R', 'L', 'D');           -- forordning, direktiv, afgørelse
exception when duplicate_object then null; end $$;

do $$ begin
  create type act_status as enum ('law', 'neg', 'plan');    -- gældende, i forhandling, planlagt
exception when duplicate_object then null; end $$;

do $$ begin
  create type act_direction as enum ('new', 'relief', 'neutral');
exception when duplicate_object then null; end $$;

create table if not exists acts (
  id            bigint generated always as identity primary key,
  category_key  text        not null references categories (key) on update cascade,
  name          text        not null,
  act_type      act_type    not null,
  status        act_status  not null,
  procedure_ref text,                    -- fx '2022/0272(COD)', hvis sagen er i proces
  direction     act_direction,           -- redaktionel vurdering: nyt krav, lettelse, neutral
  note          text,                    -- konsekvenssætning: hvem rammes, hvordan
  sort_order    smallint    not null default 0,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  constraint acts_navn_unik unique (category_key, name),
  -- en planlagt retsakt har hverken nummer eller procedure endnu; alt andet
  -- skal kunne spores til en kilde
  constraint acts_proces_har_reference check (status <> 'neg' or procedure_ref is not null)
);

create index if not exists acts_kategori_idx on acts (category_key, sort_order);
create index if not exists acts_status_idx    on acts (status);

create table if not exists act_references (
  act_id bigint   not null references acts (id) on delete cascade,
  ord    smallint not null default 0,
  year   smallint not null check (year between 1952 and 2100),
  number integer  not null check (number > 0),
  primary key (act_id, ord)
);

comment on table act_references is
  'Nummerering af en vedtaget retsakt. Flere rækker, når én retsakt har flere numre.';

-- ── afledte værdier ────────────────────────────────────────────────────────

create or replace function celex(t act_type, y smallint, n integer)
returns text language sql immutable strict as $$
  select '3' || y::text || t::text || lpad(n::text, 4, '0');
$$;

comment on function celex is
  'CELEX: sektor 3 (sekundær ret) + år + typebogstav + firecifret nummer.';

create or replace function act_label(t act_type, y smallint, n integer)
returns text language sql immutable strict as $$
  select case
    -- traktatsuffikset skifter med årstallet: EØF indtil og med 1993, EF til
    -- og med 2009, EU derefter
    when t = 'L' and y < 2015 then
      'Directive ' || case when y < 2000 then right(y::text, 2) else y::text end
        || '/' || n::text || '/' || suffix
    when t = 'L' then 'Directive (' || suffix || ') ' || y || '/' || n
    -- forordninger og afgørelser blev nummereret nummer-før-år indtil 2015
    when y < 2015 then
      case t when 'R' then 'Regulation' else 'Decision' end
        || ' (' || suffix || ') No ' || n || '/' || y
    else
      case t when 'R' then 'Regulation' else 'Decision' end
        || ' (' || suffix || ') ' || y || '/' || n
  end
  from (select case when y <= 1993 then 'EEC' when y < 2010 then 'EC' else 'EU' end) as s (suffix);
$$;

create or replace function eurlex_url(t act_type, y smallint, n integer)
returns text language sql immutable strict as $$
  select 'https://eur-lex.europa.eu/legal-content/DA/TXT/?uri=CELEX:' || celex(t, y, n);
$$;

create or replace function oeil_url(proc text)
returns text language sql immutable strict as $$
  select 'https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=' || proc;
$$;

-- ── udsigt der leverer præcis den form, siden bygges af ────────────────────

create or replace view acts_json as
select
  c.key,
  c.name,
  c.description                         as desc,
  coalesce(jsonb_agg(
    jsonb_build_object(
      'name',    a.name,
      'type',    a.act_type,
      'status',  a.status,
      'refs',    coalesce(r.refs, '[]'::jsonb),
      'proc',    a.procedure_ref,
      'procUrl', case when a.procedure_ref is not null then oeil_url(a.procedure_ref) end
    )
    order by a.sort_order, a.id
  ) filter (where a.id is not null), '[]'::jsonb) as acts
from categories c
left join acts a on a.category_key = c.key
left join lateral (
  select jsonb_agg(
           jsonb_build_object(
             'label', act_label(a.act_type, ar.year, ar.number),
             'celex', celex(a.act_type, ar.year, ar.number),
             'url',   eurlex_url(a.act_type, ar.year, ar.number)
           ) order by ar.ord
         ) as refs
  from act_references ar
  where ar.act_id = a.id
) r on true
group by c.key, c.name, c.description, c.sort_order
order by c.sort_order;

comment on view acts_json is
  'Én række pr. kategori med retsakterne som JSON. build.py læser denne udsigt direkte.';

-- ── holder updated_at ajour ────────────────────────────────────────────────

create or replace function touch_updated_at() returns trigger
language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end $$;

drop trigger if exists acts_touch on acts;
create trigger acts_touch before update on acts
for each row execute function touch_updated_at();

-- ── adgang: offentlig EU-information, læses af alle, skrives af ingen ──────

alter table categories     enable row level security;
alter table acts           enable row level security;
alter table act_references enable row level security;

drop policy if exists categories_laes on categories;
create policy categories_laes on categories for select to anon, authenticated using (true);

drop policy if exists acts_laes on acts;
create policy acts_laes on acts for select to anon, authenticated using (true);

drop policy if exists act_references_laes on act_references;
create policy act_references_laes on act_references for select to anon, authenticated using (true);

-- Ingen insert/update/delete-policy: skrivning kræver service-nøglen, som kun
-- bruges af seed- og synk-scripts. anon-nøglen kan udelukkende læse.
grant select on categories, acts, act_references, acts_json to anon, authenticated;

-- Dansk implementering: hvornår er en retsakt trådt i kraft/anvendes i
-- Danmark, og hvilken/hvilke danske myndigheder fører tilsyn.
--
-- Adskilt fra opsummeringen (0002): en forordning kan være direkte gældende
-- uden nogensinde at få en konsulentopsummering, og skal stadig kunne vise
-- dansk status. dk_status er derfor et felt på selve retsakten, ikke en del
-- af summary — 'unmapped' er default, så alle eksisterende retsakter forbliver
-- uændrede, indtil de research'es.
--
-- Tilsyn modelleres som en egen tabel frem for endnu et fritekstfelt, fordi
-- retsakter som AI-forordningen har flere myndigheder med hver sit
-- artikelafgrænsede ansvar — det kan et enkelt tekstfelt ikke vise som badges.

do $$ begin
  create type dk_status as enum ('direct', 'transposed', 'pending', 'unmapped');
  -- direct     = forordning, direkte gældende, ingen dansk gennemførelse
  -- transposed = direktiv gennemført, eller forordning suppleret af dansk lov
  -- pending    = vedtaget på EU-plan, dansk gennemførelse afventer
  -- unmapped   = ikke undersøgt endnu
exception when duplicate_object then null; end $$;

alter table acts
  add column if not exists dk_status         dk_status not null default 'unmapped',
  add column if not exists dk_instrument     text,   -- fx 'Databeskyttelsesloven'
  add column if not exists dk_instrument_ref text,   -- fx 'Lov nr. 502 af 23. maj 2018'
  add column if not exists dk_instrument_url text,   -- retsinformation.dk (ELI)
  add column if not exists dk_timeline       jsonb;  -- [{date, label, note}], samme form som acts.timeline

comment on column acts.dk_status is
  'Dansk transponeringsstatus. unmapped = default, ikke research''et endnu.';

create table if not exists authorities (
  id           bigint generated always as identity primary key,
  name         text not null unique,      -- 'Datatilsynet'
  homepage_url text
);

comment on table authorities is 'Danske tilsynsmyndigheder, genbrugt på tværs af retsakter.';

create table if not exists act_authorities (
  act_id       bigint   not null references acts (id) on delete cascade,
  authority_id bigint   not null references authorities (id) on delete cascade,
  scope_note   text,                       -- fx 'art. 5, stk. 1, litra a–c og e–f'
  sort_order   smallint not null default 0,
  primary key (act_id, authority_id)
);

comment on table act_authorities is
  'Mange-til-mange: en retsakt kan have flere myndigheder, hver med sit afgrænsede ansvar.';

-- ── udsigt: samme mønster som 0002 — hele view'et gendefineres, dk ligger
-- ved siden af summary, ikke inde i det ──────────────────────────────────

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
      'procUrl', case when a.procedure_ref is not null then oeil_url(a.procedure_ref) end,
      'summary', case when a.summary_reviewed is not null then jsonb_build_object(
        'subject',    a.subject,
        'scope',      a.scope,
        'duties',     coalesce(to_jsonb(a.duties), '[]'::jsonb),
        'timeline',   coalesce(a.timeline, '[]'::jsonb),
        'supervision', a.supervision_dk,
        'sanctions',  a.sanctions,
        'note',       coalesce(to_jsonb(a.consultant_note), '[]'::jsonb),
        'related',    coalesce(to_jsonb(a.related), '[]'::jsonb),
        'sources',    coalesce(a.sources, '[]'::jsonb),
        'reviewed',   a.summary_reviewed
      ) end,
      -- dk er null, når retsakten ikke er kortlagt endnu — uafhængigt af
      -- summary, så en direkte gældende forordning kan vise dansk status
      -- uden nogensinde at få en konsulentopsummering.
      'dk', case when a.dk_status <> 'unmapped' then jsonb_build_object(
        'status',        a.dk_status,
        'instrument',    a.dk_instrument,
        'instrumentRef', a.dk_instrument_ref,
        'instrumentUrl', a.dk_instrument_url,
        'timeline',      coalesce(a.dk_timeline, '[]'::jsonb),
        'authorities',   coalesce(au.authorities, '[]'::jsonb)
      ) end
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
left join lateral (
  select jsonb_agg(
           jsonb_build_object(
             'name',  auth.name,
             'url',   auth.homepage_url,
             'scope', aa.scope_note
           ) order by aa.sort_order, auth.name
         ) as authorities
  from act_authorities aa
  join authorities auth on auth.id = aa.authority_id
  where aa.act_id = a.id
) au on true
group by c.key, c.name, c.description, c.sort_order
order by c.sort_order;

grant select on acts_json to anon, authenticated;

-- ── adgang: samme mønster som de øvrige tabeller — offentlig data, læses af
-- alle, skrives kun via service-nøglen ────────────────────────────────────

alter table authorities     enable row level security;
alter table act_authorities enable row level security;

drop policy if exists authorities_laes on authorities;
create policy authorities_laes on authorities for select to anon, authenticated using (true);

drop policy if exists act_authorities_laes on act_authorities;
create policy act_authorities_laes on act_authorities for select to anon, authenticated using (true);

grant select on authorities, act_authorities to anon, authenticated;

-- En fjerde status: trukket tilbage.
--
-- Tre af datasættets forslag er ikke i forhandling og bliver aldrig vedtaget —
-- Kommissionen har trukket dem tilbage. Uden en egen status ville de stå som
-- 'neg', og siden ville få læseren til at forberede sig på lovgivning, der
-- ikke kommer. Det er en værre fejl end et hul, fordi det er en påstand.
--
-- 'plan' kunne ikke bruges: et planlagt initiativ er noget, der måske kommer,
-- et tilbagetrukket forslag er noget, der ikke gør. Modsat retning.

-- Enum-værdier kan ikke tilføjes inde i en transaktion i ældre Postgres; her
-- køres sætningen for sig gennem Management API'ets query-endpoint.
alter type act_status add value if not exists 'withdrawn';

alter table acts
  -- Hvornår og hvorfor. For standard-essentielle patenter også forbeholdet:
  -- Europa-Parlamentet har indbragt tilbagetrækningen for EU-Domstolen, så
  -- sagen er ikke afsluttet på samme måde som de to andre.
  add column if not exists status_note text;

comment on column acts.status_note is
  'Forbehold til statussen — fx dato for tilbagetrækning. Null for de fleste retsakter.';

-- Betingelsen fra 0001 kræver kun en procedurereference for 'neg'. Et
-- tilbagetrukket forslag HAR en procedure — det er netop den, der blev
-- afbrudt — så kravet udvides frem for at blive lempet.
--
-- Skrevet som en positivliste over de statusser, der IKKE kræver en
-- reference, frem for at nævne 'withdrawn'. Dels fordi en ny enum-værdi ikke
-- kan bruges i samme migration som den tilføjes, dels fordi standarden så
-- bliver den rigtige: en status, nogen tilføjer senere, kræver en kilde,
-- indtil andet er besluttet.
alter table acts drop constraint if exists acts_proces_har_reference;
alter table acts add constraint acts_proces_har_reference
  check (status in ('law', 'plan') or procedure_ref is not null);

-- ── udsigt: 0004 med statusNote ────────────────────────────────────────────

create or replace view acts_json as
select
  c.key,
  c.name,
  c.description                         as desc,
  coalesce(jsonb_agg(
    jsonb_build_object(
      'name',    a.name,
      'slug',    slug(a.name),
      'type',    a.act_type,
      'status',  a.status,
      'statusNote', a.status_note,
      'refs',    coalesce(r.refs, '[]'::jsonb),
      'proc',    a.procedure_ref,
      'procUrl', case when a.procedure_ref is not null then oeil_url(a.procedure_ref) end,
      'appliesFrom', a.applies_from,
      'appliesNote', a.applies_note,
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

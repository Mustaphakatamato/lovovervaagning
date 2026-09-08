-- Adresser pr. retsakt, og EU's anvendelsesdato.
--
-- Hver retsakt får sin egen side på #akt/<slug>. Sluggen afledes af navnet, som
-- CELEX-numre og URL'er gør i 0001 — den lagres ikke, så den ikke kan komme i
-- utakt med det navn, den bygger på.
--
-- applies_from er EU-retsaktens anvendelsesdato og ikke det samme som
-- dk_timeline fra 0003, som er den danske gennemførelse. En forordning kan
-- være anvendelig i hele EU længe før eller uden at Danmark gør noget, og en
-- læser, der spørger "gælder det for mig", skal have det EU-retlige svar først.
-- Det er også et andet felt end summary.timeline, som kun findes for de
-- retsakter, der har fået en konsulentopsummering.

alter table acts
  add column if not exists applies_from date,
  -- Datoerne er ofte trappede — AI-forordningen har fem. Hovedtallet står i
  -- applies_from, forbeholdet her.
  add column if not exists applies_note text;

comment on column acts.applies_from is
  'EU-anvendelsesdato, ikke vedtagelsesdato. Null = ikke vedtaget, eller ikke slået op endnu.';

-- ── slug: den stabile adresse pr. retsakt ──────────────────────────────────

create or replace function slug(name text)
returns text language sql immutable strict as $$
  -- Slutter navnet på en parentes, er indholdet en forkortelse, og den er den
  -- adresse et menneske ville skrive: (GDPR) -> gdpr, (RSPP 2.0) -> rspp-2-0.
  -- Ellers kebab-case af hele navnet.
  select trim(both '-' from regexp_replace(lower(base), '[^a-z0-9]+', '-', 'g'))
  from (select coalesce(substring(name from '\(([^()]+)\)\s*$'), name)) as b (base);
$$;

comment on function slug is
  'Afledt adresse til #akt/<slug>. CELEX virker som alias, fordi en slug dør, hvis navnet rettes.';

-- ── udsigt: 0003 med slug og anvendelsesdato ved siden af ──────────────────

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

-- Konsulentopsummering pr. retsakt.
--
-- Felterne er delt op frem for at være ét fritekstfelt, fordi de bruges
-- forskelligt: datoerne skal kunne sorteres og sammenlignes, pligterne skal
-- kunne vises som liste, og tilsynsfeltet er det, der oftest skal rettes.
--
-- summary_reviewed er ikke pynt. Indholdet ældes — AI-forordningens datoer
-- flyttede sig i juli 2026 — og uden en kontroldato kan læseren ikke vide, om
-- teksten er ajour.

alter table acts
  add column if not exists subject          text,      -- lovens genstand, 1-2 sætninger
  add column if not exists scope            text,      -- anvendelsesområde: hvem og hvad
  add column if not exists duties           text[],    -- kernekrav
  add column if not exists timeline         jsonb,     -- [{date, label, note}]
  add column if not exists supervision_dk   text,      -- dansk tilsynsmyndighed
  add column if not exists sanctions        text,
  add column if not exists consultant_note  text[],    -- hvad det betyder for et tech-hus
  add column if not exists related          text[],    -- andre retsakter, ved navn
  add column if not exists sources          jsonb,     -- [{label, url}]
  add column if not exists summary_reviewed date;

comment on column acts.summary_reviewed is
  'Hvornår opsummeringen sidst er kontrolleret mod kilderne. Null = ingen opsummering.';

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
      -- summary er null, når retsakten ikke er uddybet. Siden bruger netop det
      -- til at afgøre, om opsummeringsknappen skal vises.
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
group by c.key, c.name, c.description, c.sort_order
order by c.sort_order;

grant select on acts_json to anon, authenticated;

INSERT INTO "public"."approval_stage" (
    "id",
    "policy_id",
    "stage_order",
    "name",
    "mode",
    "mode_value",
    "sla_hours",
    "parallel_group",
    "skip_if",
    "on_empty",
    "on_breach",
    "escalation_rules_json",
    "created_at",
    "updated_at"
)
SELECT v."id", v."policy_id", v."stage_order"::int, v."name", v."mode",
       v."mode_value"::int, v."sla_hours"::int, v."parallel_group"::int,
       v."skip_if"::json, v."on_empty", v."on_breach",
       v."escalation_rules_json"::json, v."created_at"::timestamptz, v."updated_at"::timestamptz
FROM (VALUES
    ('c3200000-0000-4000-8000-000000000101', 'c3100000-0000-4000-8000-000000000001', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('c3200000-0000-4000-8000-000000000201', 'c3100000-0000-4000-8000-000000000002', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('c3200000-0000-4000-8000-000000000301', 'c3100000-0000-4000-8000-000000000003', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('c3200000-0000-4000-8000-000000000111', 'c3100000-0000-4000-8000-000000000011', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('c3200000-0000-4000-8000-000000000121', 'c3100000-0000-4000-8000-000000000012', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('c3200000-0000-4000-8000-000000000131', 'c3100000-0000-4000-8000-000000000013', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW())
) AS v("id","policy_id","stage_order","name","mode","mode_value","sla_hours",
        "parallel_group","skip_if","on_empty","on_breach","escalation_rules_json",
        "created_at","updated_at")
-- Skip stages whose policy is absent. A policy row can legitimately be skipped
-- above (the platform already owns that policy_key), and without this filter the
-- orphan's FK violation aborts the whole statement, taking the valid stages with it.
WHERE EXISTS (SELECT 1 FROM "public"."approval_policy" p WHERE p.id = v."policy_id")
ON CONFLICT DO NOTHING;

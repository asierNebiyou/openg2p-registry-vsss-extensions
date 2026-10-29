-- One approval stage per VSSS policy.
--
-- Id columns are cast explicitly because literals in a VALUES subquery resolve
-- to `text`: without the casts this statement fails on a uuid-typed AWE schema
-- ("column id is of type uuid but expression is of type text") and the EXISTS
-- guard fails too ("operator does not exist: uuid = text"). `::uuid` on the
-- inserted ids and `::text` on the guard are accepted by BOTH a uuid-typed and
-- a varchar-typed schema, so this seed is portable across either.
--
-- INSERT ... SELECT FROM (VALUES ...) so the WHERE EXISTS filter can skip stages
-- whose policy was legitimately skipped above (the platform already owns that
-- policy_key). Without the filter the orphan's FK violation aborts the whole
-- statement and takes the valid stages with it.
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
SELECT v."id"::uuid, v."policy_id"::uuid, v."stage_order"::int, v."name", v."mode",
       v."mode_value"::int, v."sla_hours"::int, v."parallel_group"::int,
       v."skip_if"::json, v."on_empty", v."on_breach",
       v."escalation_rules_json"::json, v."created_at"::timestamptz, v."updated_at"::timestamptz
FROM (VALUES
    ('a1b2c3d4-0001-4000-8000-000000000001', '1c0a7f42-6d31-4f88-9b2e-0a4d7c51e9b3', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('a1b2c3d4-0002-4000-8000-000000000002', '2d1b8053-7e42-4a99-8c3f-1b5e8d62fac4', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('a1b2c3d4-0003-4000-8000-000000000003', '3e2c9164-8f53-4baa-9d40-2c6f9e73ab05', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('a1b2c3d4-0004-4000-8000-000000000004', '4f3da275-9064-4cbb-ae51-3d70af84bc16', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('a1b2c3d4-0005-4000-8000-000000000005', '5a4eb386-a175-4dcc-bf62-4e81b095cd27', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('a1b2c3d4-0006-4000-8000-000000000006', '6b5fc497-b286-4edd-c073-5f92c1a6de38', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW())
) AS v("id","policy_id","stage_order","name","mode","mode_value","sla_hours",
        "parallel_group","skip_if","on_empty","on_breach","escalation_rules_json",
        "created_at","updated_at")
WHERE EXISTS (SELECT 1 FROM "public"."approval_policy" p WHERE p.id::text = v."policy_id")
ON CONFLICT DO NOTHING;

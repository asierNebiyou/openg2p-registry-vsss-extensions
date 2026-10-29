-- Approver rules for each VSSS stage.
--
-- `user_id` is rewritten to the local Keycloak dev user by the developer stack's
-- apply_seed_sql.py (KEYCLOAK_DEV_USER); in a real deployment replace these with
-- the operating ministry's approver accounts, groups or roles.
--
-- Ids are cast for the same reason as in 20_approval_stage.sql: `::uuid` on the
-- inserted ids, `::text` on the EXISTS guard, so either schema type works.
--
-- Same WHERE EXISTS reason as the stage filter: a rule whose stage was skipped
-- must not abort the statement and take the valid rules with it.
INSERT INTO "public"."approver_rule" (
    "id",
    "stage_id",
    "rule_type",
    "rule_value",
    "kind",
    "required",
    "created_at",
    "updated_at"
)
SELECT v."id"::uuid, v."stage_id"::uuid, v."rule_type", v."rule_value"::json, v."kind",
       v."required"::boolean, v."created_at"::timestamptz, v."updated_at"::timestamptz
FROM (VALUES
    ('b2c3d4e5-0001-4000-8000-000000000001', 'a1b2c3d4-0001-4000-8000-000000000001', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('b2c3d4e5-0002-4000-8000-000000000002', 'a1b2c3d4-0002-4000-8000-000000000002', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('b2c3d4e5-0003-4000-8000-000000000003', 'a1b2c3d4-0003-4000-8000-000000000003', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('b2c3d4e5-0004-4000-8000-000000000004', 'a1b2c3d4-0004-4000-8000-000000000004', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('b2c3d4e5-0005-4000-8000-000000000005', 'a1b2c3d4-0005-4000-8000-000000000005', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('b2c3d4e5-0006-4000-8000-000000000006', 'a1b2c3d4-0006-4000-8000-000000000006', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW())
) AS v("id","stage_id","rule_type","rule_value","kind","required","created_at","updated_at")
WHERE EXISTS (SELECT 1 FROM "public"."approval_stage" s WHERE s.id::text = v."stage_id")
ON CONFLICT DO NOTHING;

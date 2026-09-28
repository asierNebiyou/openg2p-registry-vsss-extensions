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
SELECT v."id", v."stage_id", v."rule_type", v."rule_value"::json, v."kind",
       v."required"::boolean, v."created_at"::timestamptz, v."updated_at"::timestamptz
FROM (VALUES
    ('c3300000-0000-4000-8000-000000000101', 'c3200000-0000-4000-8000-000000000101', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('c3300000-0000-4000-8000-000000000201', 'c3200000-0000-4000-8000-000000000201', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('c3300000-0000-4000-8000-000000000301', 'c3200000-0000-4000-8000-000000000301', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('c3300000-0000-4000-8000-000000000111', 'c3200000-0000-4000-8000-000000000111', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('c3300000-0000-4000-8000-000000000121', 'c3200000-0000-4000-8000-000000000121', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('c3300000-0000-4000-8000-000000000131', 'c3200000-0000-4000-8000-000000000131', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW())
) AS v("id","stage_id","rule_type","rule_value","kind","required","created_at","updated_at")
-- Same reason as the stage filter: a rule whose stage was skipped must not abort
-- the statement and take the valid rules with it.
WHERE EXISTS (SELECT 1 FROM "public"."approval_stage" s WHERE s.id = v."stage_id")
ON CONFLICT DO NOTHING;

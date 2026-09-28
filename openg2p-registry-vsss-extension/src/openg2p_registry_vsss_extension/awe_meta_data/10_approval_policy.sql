INSERT INTO "public"."approval_policy" (
    "id",
    "policy_key",
    "version",
    "name",
    "description",
    "status",
    "artifact_type",
    "created_by",
    "forbid_self_approval",
    "forbid_repeat_approvers",
    "created_at",
    "updated_at"
) VALUES
    ('c3100000-0000-4000-8000-000000000001', 'registry.change_request.individual', 1, 'Policy for Individual Change Request', NULL, 'draft', 'registry.change_request', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('c3100000-0000-4000-8000-000000000002', 'registry.change_request.household', 1, 'Policy for Household Change Request', NULL, 'draft', 'registry.change_request', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('c3100000-0000-4000-8000-000000000003', 'registry.change_request.village', 1, 'Policy for Village Change Request', NULL, 'draft', 'registry.change_request', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('c3100000-0000-4000-8000-000000000011', 'registry.intake_form.individual', 1, 'Policy for Individual Intake Form', NULL, 'draft', 'registry.intake_form', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('c3100000-0000-4000-8000-000000000012', 'registry.intake_form.household', 1, 'Policy for Household Intake Form', NULL, 'draft', 'registry.intake_form', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('c3100000-0000-4000-8000-000000000013', 'registry.intake_form.village', 1, 'Policy for Village Intake Form', NULL, 'draft', 'registry.intake_form', 'seed', 'FALSE', 'FALSE', NOW(), NOW())
-- Untargeted DO NOTHING, not ON CONFLICT ("id"): `approval_policy` also carries
-- uq_policy_key_version, and the platform seeds `registry.change_request.household`
-- under a DIFFERENT id. Targeting "id" left that natural-key clash unguarded, so
-- the whole multi-row statement aborted and NONE of the policies landed — individual
-- included. Untargeted catches every unique constraint and skips only the
-- offending row.
ON CONFLICT DO NOTHING;

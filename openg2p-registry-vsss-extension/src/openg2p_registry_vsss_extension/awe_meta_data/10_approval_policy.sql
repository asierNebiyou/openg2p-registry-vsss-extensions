-- VSSS approval policies (AWE database).
--
-- One policy per approvable artifact: change requests and intake forms for the
-- Individual, Household and Village registers. The Village register is
-- VSSS-specific (NSR has no equivalent).
--
-- Untargeted DO NOTHING, not ON CONFLICT ("id"): `approval_policy` also carries
-- uq_policy_key_version, and the platform may already seed some policy_key under
-- a DIFFERENT id. Targeting "id" would leave that natural-key clash unguarded and
-- the whole multi-row statement would abort, landing NONE of the policies.
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
    ('1c0a7f42-6d31-4f88-9b2e-0a4d7c51e9b3', 'registry.change_request.individual', 1, 'Policy for Individual Change Request', NULL, 'active', 'registry.change_request', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('2d1b8053-7e42-4a99-8c3f-1b5e8d62fac4', 'registry.change_request.household',  1, 'Policy for Household Change Request',  NULL, 'active', 'registry.change_request', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('3e2c9164-8f53-4baa-9d40-2c6f9e73ab05', 'registry.change_request.village',    1, 'Policy for Village Change Request',    NULL, 'active', 'registry.change_request', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('4f3da275-9064-4cbb-ae51-3d70af84bc16', 'registry.intake_form.individual',    1, 'Policy for Individual Intake Form',    NULL, 'active', 'registry.intake_form',    'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('5a4eb386-a175-4dcc-bf62-4e81b095cd27', 'registry.intake_form.household',     1, 'Policy for Household Intake Form',     NULL, 'active', 'registry.intake_form',    'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('6b5fc497-b286-4edd-c073-5f92c1a6de38', 'registry.intake_form.village',       1, 'Policy for Village Intake Form',       NULL, 'active', 'registry.intake_form',    'seed', 'FALSE', 'FALSE', NOW(), NOW())
ON CONFLICT DO NOTHING;

-- Converge databases seeded before these policies became 'active'.
-- The INSERT above is ON CONFLICT DO NOTHING, so on any DB that already ran an
-- earlier seed the rows keep whatever status they were created with — leaving
-- the policies inert and approvals unrouted, with nothing in the logs to say so.
-- Scoped to this seed's own rows (created_by = 'seed') and only to rows still
-- 'draft', so a policy somebody deliberately drafted or retired is left alone.
UPDATE "public"."approval_policy"
   SET "status" = 'active',
       "updated_at" = NOW()
 WHERE "created_by" = 'seed'
   AND "status" = 'draft'
   AND "policy_key" IN (
     'registry.change_request.individual',
     'registry.change_request.household',
     'registry.change_request.village',
     'registry.intake_form.individual',
     'registry.intake_form.household',
     'registry.intake_form.village'
   );

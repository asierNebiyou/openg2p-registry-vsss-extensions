-- Binds each VSSS register / intake form to the AWE policy that governs it.
-- register_id and intake_form_id values come from
-- register-metadata/g2p_register_definitions.sql and
-- register-metadata/g2p_intake_form_definitions.sql; policy_key values come
-- from awe_meta_data/10_approval_policy.sql.
INSERT INTO "public"."g2p_registry_awe_policy_configurations" (
    "awe_policy_config_id",
    "policy_scope",
    "register_id",
    "intake_form_id",
    "section_id",
    "policy_type",
    "policy_key",
    "context_field_names"
) VALUES
    ('c3d4e5f6-0001-4000-8000-000000000001','REGISTER','a1a4d25a-1cd4-4356-abac-985a0b3c6bcd','','','registry.change_request','registry.change_request.individual','null'),
    ('c3d4e5f6-0002-4000-8000-000000000002','REGISTER','9055ab43-c85d-4833-bd00-ca657bb72644','','','registry.change_request','registry.change_request.household','null'),
    ('c3d4e5f6-0003-4000-8000-000000000003','REGISTER','e7c8f2a1-4b5d-4e6f-9a0b-1c2d3e4f5a6b','','','registry.change_request','registry.change_request.village','null'),
    ('c3d4e5f6-0004-4000-8000-000000000004','INTAKE_FORM','a1a4d25a-1cd4-4356-abac-985a0b3c6bcd','dcf019af-458c-43be-9343-16dfc38a2475','','registry.intake_form','registry.intake_form.individual','null'),
    ('c3d4e5f6-0005-4000-8000-000000000005','INTAKE_FORM','9055ab43-c85d-4833-bd00-ca657bb72644','7a7cbf4b-2b9f-49df-a50e-f10b1b7e6b6d','','registry.intake_form','registry.intake_form.household','null'),
    ('c3d4e5f6-0006-4000-8000-000000000006','INTAKE_FORM','e7c8f2a1-4b5d-4e6f-9a0b-1c2d3e4f5a6b','a9b8c7d6-e5f4-4321-9876-543210fedcba','','registry.intake_form','registry.intake_form.village','null')
ON CONFLICT ("awe_policy_config_id") DO NOTHING;

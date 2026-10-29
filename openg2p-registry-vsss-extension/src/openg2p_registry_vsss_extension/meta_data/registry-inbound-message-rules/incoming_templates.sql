-- Transformation template bound to the generic JSON-L import path.
--
-- The nsr_edrmc_* and nsr_v11_* template bindings that used to sit here were
-- removed with the rest of the NSR-inherited inbound surface.
INSERT INTO
    "public"."incoming_templates" (
        "template_id",
        "register_id",
        "data_model_id",
        "template_document_id",
        "jsonld_expansion_required",
        "created_at",
        "updated_at"
    )
VALUES
    (
        'd8f9a188-fec4-4465-b4f0-59565ff3f092',
        '9055ab43-c85d-4833-bd00-ca657bb72644',
        '3116dd3a-1f81-46c3-b6a8-88f82fe5aae5',
        'd2e7bd22-edd2-446b-82f3-6a6044c7c732',
        'False',
        '2026-05-13 05:50:00.260793',
        NULL
    )
ON CONFLICT DO NOTHING;

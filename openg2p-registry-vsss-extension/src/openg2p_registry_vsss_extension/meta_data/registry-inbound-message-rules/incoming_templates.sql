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
    ),
    (
        'nsr_edrmc_household_template',
        '9055ab43-c85d-4833-bd00-ca657bb72644',
        'nsr_edrmc_data_model',
        'eb3e2450-11af-57da-9b77-1f49d8a1f4c2',
        'False',
        '2026-05-06 11:32:37.662558',
        '2026-05-06 11:49:28.514495'
    ),
    (
        'nsr_edrmc_individual_template',
        'a1a4d25a-1cd4-4356-abac-985a0b3c6bcd',
        'nsr_edrmc_data_model',
        'eb3e2450-11af-57da-9b77-1f49d8a1f4c2',
        'False',
        '2026-05-06 11:32:37.662558',
        '2026-05-06 11:49:28.514495'
    ),
    (
        'nsr_v11_household_template',
        '9055ab43-c85d-4833-bd00-ca657bb72644',
        'nsr_v11_data_model',
        '49cdd4aa-459f-51f3-b50c-cdc3e2559967',
        'False',
        '2026-04-30 09:53:08.47819',
        '2026-04-30 17:47:14.899648'
    ),
    (
        'nsr_v11_individual_template',
        'a1a4d25a-1cd4-4356-abac-985a0b3c6bcd',
        'nsr_v11_data_model',
        '59a8f5f9-7fd0-5631-84a9-f6c2b6113bd5',
        'False',
        '2026-04-30 09:53:08.47819',
        '2026-04-30 17:47:14.899648'
    )
ON CONFLICT DO NOTHING;

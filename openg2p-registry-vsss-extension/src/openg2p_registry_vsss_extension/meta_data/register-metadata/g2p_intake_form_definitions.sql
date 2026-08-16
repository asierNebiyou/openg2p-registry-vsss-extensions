INSERT INTO
    "public"."g2p_intake_form_definitions" (
        "form_id",
        "register_id",
        "form_mnemonic",
        "form_description",
        "number_of_verifications",
        "used_only_in_ingestion_pipeline"
    )
VALUES
    (
        'a9b8c7d6-e5f4-4321-9876-543210fedcba',
        'e7c8f2a1-4b5d-4e6f-9a0b-1c2d3e4f5a6b',
        'Village Intake Form',
        'This form collects essential details of a VSSS village for registration and grant readiness.',
        1,
        'False'
    ),
    (
        '7a7cbf4b-2b9f-49df-a50e-f10b1b7e6b6d',
        '9055ab43-c85d-4833-bd00-ca657bb72644',
        'Household Intake Form',
        'This form collects essential details of household to help create an accurate and complete profile.',
        1,
        'False'
    ),
    (
        'dcf019af-458c-43be-9343-16dfc38a2475',
        'a1a4d25a-1cd4-4356-abac-985a0b3c6bcd',
        'Individual Intake Form',
        'This form collects essential details of individual to help create an accurate and complete profile.',
        1,
        'False'
    );
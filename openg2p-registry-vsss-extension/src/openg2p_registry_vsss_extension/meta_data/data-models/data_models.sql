INSERT INTO
    "public"."data_models" (
        "data_model_id",
        "data_model_mnemonic",
        "pattern_for_data_model",
        "response_template_document_id",
        "is_active"
    )
VALUES
    (
        '3116dd3a-1f81-46c3-b6a8-88f82fe5aae5',
        'Import file (JSON-L)',
        '*',
        NULL,
        'True'
    ),
    (
        '7a7fefc6-588c-4fb1-a26d-a5414d0ceb38',
        'Import-CSV',
        '*',
        NULL,
        'True'
    ),
    (
        'a38d1cbd-88a3-4ffd-9cc9-ccb69148d489',
        'test',
        '$.body.header.message_id=>^$',
        '283c29fe-c762-4e5d-a90d-0124d194cd98',
        'True'
    ),
    (
        'nsr_edrmc_data_model',
        'nsr_registration_edrmc',
        '$.body.header.message_id=>^.+$',
        NULL,
        'True'
    ),
    (
        'nsr_v11_data_model',
        'NSR_REGISTRATION_V11',
        '$.body.header.message_id=>^.+$',
        '56619678-0cad-4eb1-924e-6e74fb20291f',
        'True'
    )
ON CONFLICT DO NOTHING;

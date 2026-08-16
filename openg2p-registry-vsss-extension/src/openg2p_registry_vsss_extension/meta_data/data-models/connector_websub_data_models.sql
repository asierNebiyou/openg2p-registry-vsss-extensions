-- ---------------------------------------------------------------------------
-- Data models for the connector-fed WebSub sources.
--
-- The connector posts to the Partner API with ?data_model=<MNEMONIC>; its
-- HTTP client upper-cases the connector's data_model_mnemonic, and the core
-- ingest service matches data_models.data_model_mnemonic EXACTLY — so these
-- mnemonics MUST be uppercase. pattern_for_data_model is kept sender-pinned
-- as a fallback for envelopes posted without the query parameter.
--
-- The ODK connector reuses the existing NSR_REGISTRATION_V11 data model
-- (data_models.sql) and needs no extra rows here.
-- ---------------------------------------------------------------------------
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
        'edrmc_websub_v1_data_model',
        'EDRMC_WEBSUB_V1',
        '$.body.header.sender_id=>^edrmc-websub$',
        NULL,
        'True'
    ),
    (
        'ud_websub_individual_v1_data_model',
        'UD_WEBSUB_INDIVIDUAL_V1',
        '$.body.header.sender_id=>^ud-sr-websub$',
        NULL,
        'True'
    )
ON CONFLICT (data_model_id) DO UPDATE SET
    data_model_mnemonic    = EXCLUDED.data_model_mnemonic,
    pattern_for_data_model = EXCLUDED.pattern_for_data_model,
    is_active              = EXCLUDED.is_active;

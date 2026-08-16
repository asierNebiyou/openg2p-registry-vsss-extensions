-- ---------------------------------------------------------------------------
-- Inbound message rules for the connector-fed WebSub sources
-- (EDRMC_WEBSUB_V1 and UD_WEBSUB_INDIVIDUAL_V1 data models defined in
-- data-models/connector_websub_data_models.sql).
--
-- Both sources arrive through the connector, which wraps every record in the
-- standard {header, message} envelope, so the key paths mirror nsr_v11.
-- Routing:
--   EDRMC   -> registration_type discriminator (household | individual)
--   UD SR   -> source_system discriminator injected by the connector mapper
-- Register / intake form UUIDs are the NSR extension's fixed IDs
-- (register-metadata/g2p_register_definitions.sql).
-- ---------------------------------------------------------------------------

INSERT INTO
    "public"."incoming_model_key_paths" (
        "key_path_id",
        "data_model_id",
        "key_path_for_message_id",
        "key_path_for_sender",
        "key_path_for_signature",
        "key_path_for_signature_payload",
        "is_list",
        "key_path_for_list_elements"
    )
VALUES
    (
        'edrmc_websub_v1_key_paths',
        'edrmc_websub_v1_data_model',
        '$.body.header.message_id',
        '$.body.header.sender_id',
        '$.body.header.signature',
        '$.body.message',
        'False',
        '$.body.message.payload'
    ),
    (
        'ud_websub_individual_v1_key_paths',
        'ud_websub_individual_v1_data_model',
        '$.body.header.message_id',
        '$.body.header.sender_id',
        '$.body.header.signature',
        '$.body.message',
        'False',
        '$.body.message.payload'
    )
ON CONFLICT (data_model_id) DO UPDATE SET
    key_path_for_message_id        = EXCLUDED.key_path_for_message_id,
    key_path_for_sender            = EXCLUDED.key_path_for_sender,
    key_path_for_signature         = EXCLUDED.key_path_for_signature,
    key_path_for_signature_payload = EXCLUDED.key_path_for_signature_payload,
    is_list                        = EXCLUDED.is_list,
    key_path_for_list_elements     = EXCLUDED.key_path_for_list_elements;

INSERT INTO
    "public"."incoming_model_semantic_patterns" (
        "semantic_pattern_id",
        "data_model_id",
        "register_id",
        "pattern_for_register",
        "key_path_for_business_payload",
        "raw_payload_enricher_class",
        "intake_form_id",
        "pattern_for_intake_form"
    )
VALUES
    (
        'edrmc_websub_v1_household_pattern',
        'edrmc_websub_v1_data_model',
        '9055ab43-c85d-4833-bd00-ca657bb72644',
        '$.body.message.payload.registration_type=>^household$',
        '$.body.message.payload',
        'G2PSpdciHouseholdCreateEnricherService',
        '7a7cbf4b-2b9f-49df-a50e-f10b1b7e6b6d',
        '$.body.message.payload.registration_type=>^household$'
    ),
    (
        'edrmc_websub_v1_individual_pattern',
        'edrmc_websub_v1_data_model',
        'a1a4d25a-1cd4-4356-abac-985a0b3c6bcd',
        '$.body.message.payload.registration_type=>^individual$',
        '$.body.message.payload',
        'G2PSpdciIndividualCreateEnricherService',
        'dcf019af-458c-43be-9343-16dfc38a2475',
        '$.body.message.payload.registration_type=>^individual$'
    ),
    (
        'ud_websub_individual_v1_pattern',
        'ud_websub_individual_v1_data_model',
        'a1a4d25a-1cd4-4356-abac-985a0b3c6bcd',
        '$.body.message.payload.source_system=>^ud_websub_sr$',
        '$.body.message.payload',
        'G2PSpdciIndividualCreateEnricherService',
        'dcf019af-458c-43be-9343-16dfc38a2475',
        '$.body.message.payload.source_system=>^ud_websub_sr$'
    )
ON CONFLICT (semantic_pattern_id) DO UPDATE SET
    data_model_id                 = EXCLUDED.data_model_id,
    register_id                   = EXCLUDED.register_id,
    pattern_for_register          = EXCLUDED.pattern_for_register,
    key_path_for_business_payload = EXCLUDED.key_path_for_business_payload,
    raw_payload_enricher_class    = EXCLUDED.raw_payload_enricher_class,
    intake_form_id                = EXCLUDED.intake_form_id,
    pattern_for_intake_form       = EXCLUDED.pattern_for_intake_form;

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
        'edrmc_websub_v1_household_template',
        '9055ab43-c85d-4833-bd00-ca657bb72644',
        'edrmc_websub_v1_data_model',
        '2e8b6d94-1a5f-5e83-b7c0-9d34a2f61c58',
        'False',
        '2026-05-22 00:00:00',
        NULL
    ),
    (
        'edrmc_websub_v1_individual_template',
        'a1a4d25a-1cd4-4356-abac-985a0b3c6bcd',
        'edrmc_websub_v1_data_model',
        '7c1f3a52-9b0e-5c47-8d21-4f6a8e0b9d13',
        'False',
        '2026-05-22 00:00:00',
        NULL
    ),
    (
        'ud_websub_individual_v1_template',
        'a1a4d25a-1cd4-4356-abac-985a0b3c6bcd',
        'ud_websub_individual_v1_data_model',
        'a4d92f07-6c31-5b68-9e45-0b7d18c3f2a6',
        'False',
        '2026-05-22 00:00:00',
        NULL
    )
ON CONFLICT (template_id) DO UPDATE SET
    register_id               = EXCLUDED.register_id,
    data_model_id             = EXCLUDED.data_model_id,
    template_document_id      = EXCLUDED.template_document_id,
    jsonld_expansion_required = EXCLUDED.jsonld_expansion_required,
    updated_at                = NOW();

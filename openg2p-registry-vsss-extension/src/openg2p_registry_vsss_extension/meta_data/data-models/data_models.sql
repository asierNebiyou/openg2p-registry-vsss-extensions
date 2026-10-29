-- Data models VSSS accepts records under.
--
-- Only the generic import paths remain. The inbound connector surface this
-- extension inherited from the MoWSA NSR lineage has been removed: the
-- edrmc_websub / ud_websub WebSub models pointed at Ethiopian endpoints
-- (websub.hrp.edrmc.gov.et, websub.ud.mowsa.gov.et), and nsr_v11_data_model /
-- nsr_edrmc_data_model carried NSR's Ethiopian payload shape (woreda / zone /
-- kebele). None of it applies to a Uganda VSSS deployment.
--
-- Add a VSSS-specific data model here, with matching key paths, semantic
-- patterns and incoming templates, when a real inbound source exists.
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
    )
ON CONFLICT DO NOTHING;

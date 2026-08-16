-- ---------------------------------------------------------------------------
-- Incoming partners for connector-fed sources (MASTER DATA database).
--
-- The core ingest service resolves $.body.header.sender_id against
-- g2p_partners.partner_mnemonic in the master-data DB and rejects the
-- envelope with PARTNER_NOT_REGISTERED when no row exists. One row per
-- connector g2p_sender_id.
--
-- keymanager_reference_id must be unique but is not exercised today:
-- signature validation is disabled in G2PIngestService (the
-- _validate_signature call is commented out upstream). Replace these
-- placeholders with real Keymanager reference IDs if/when signature
-- verification is enabled.
-- ---------------------------------------------------------------------------
INSERT INTO
    "public"."g2p_partners" (
        "partner_id",
        "partner_mnemonic",
        "keymanager_reference_id",
        "is_active"
    )
VALUES
    (
        'c3f6b7e1-52d4-5a89-b1c2-7e9a3d05f841',
        'edrmc-websub',
        'edrmc-websub-keyref',
        TRUE
    ),
    (
        '5d28a94c-e07b-5f36-a6d1-38c4b21e9f75',
        'ud-sr-websub',
        'ud-sr-websub-keyref',
        TRUE
    ),
    (
        '81b4c2d9-3e65-5a07-9f28-d15e6a4c03b2',
        'odk-nsr',
        'odk-nsr-keyref',
        TRUE
    )
ON CONFLICT DO NOTHING;

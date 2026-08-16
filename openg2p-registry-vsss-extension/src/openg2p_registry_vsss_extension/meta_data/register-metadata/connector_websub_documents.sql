-- ---------------------------------------------------------------------------
-- Document catalog rows for the connector WebSub Jinja templates.
--
-- Object key in MinIO == document_store_id == filename: the db-seed job
-- uploads every *.j2 in the extension's templates/ folder with the filename
-- as the object key (see docker/db-seed/upload_templates.py), and
-- incoming_templates.template_document_id below points at these rows.
-- ---------------------------------------------------------------------------
INSERT INTO
    "public"."g2p_registry_documents" (
        "document_id",
        "document_store_id",
        "bucket",
        "source_filename",
        "created_by",
        "created_at"
    )
VALUES
    (
        '7c1f3a52-9b0e-5c47-8d21-4f6a8e0b9d13',
        'edrmc_websub_individual.j2',
        'templates',
        'edrmc_websub_individual.j2',
        'seeder',
        '2026-05-22 00:00:00'
    ),
    (
        '2e8b6d94-1a5f-5e83-b7c0-9d34a2f61c58',
        'edrmc_websub_household.j2',
        'templates',
        'edrmc_websub_household.j2',
        'seeder',
        '2026-05-22 00:00:00'
    ),
    (
        'a4d92f07-6c31-5b68-9e45-0b7d18c3f2a6',
        'ud_websub_individual.j2',
        'templates',
        'ud_websub_individual.j2',
        'seeder',
        '2026-05-22 00:00:00'
    )
ON CONFLICT DO NOTHING;

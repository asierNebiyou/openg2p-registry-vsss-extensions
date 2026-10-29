-- Document catalog rows for the Jinja templates VSSS ships.
--
-- Object key in MinIO == document_store_id == filename: the db-seed job uploads
-- every *.j2 in the extension's templates/ folder with the filename as the
-- object key (docker/db-seed/upload_templates.py).
--
-- This file previously carried 47 rows captured from an NSR developer database:
-- 30+ `import_file/<hash>_nsr_household_single_data_record.jsonl` uploads plus
-- openg2p_logo.png, zmb.conf, 1.jpeg, "Online Application Receipt (1).pdf",
-- odk.txt and nine duplicate z_sample_import_template_household rows under
-- different store ids. None of it was referenced by VSSS metadata, and the
-- import_file/* objects do not exist in any VSSS MinIO bucket, so the catalog
-- advertised documents that could never be fetched. Only the rows VSSS
-- references remain.
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
    -- referenced by registry-inbound-message-rules/incoming_templates.sql
    (
        'd2e7bd22-edd2-446b-82f3-6a6044c7c732',
        'z_sample_import_template_household.json.j2',
        'templates',
        'z_sample_import_template_household.json.j2',
        'seeder',
        '2026-04-01 00:00:00'
    ),
    -- generic DCI response template (not variant-specific)
    (
        '56619678-0cad-4eb1-924e-6e74fb20291f',
        'dci_commons_response.json.j2',
        'templates',
        'dci_commons_response.json.j2',
        'seeder',
        '2026-04-01 00:00:00'
    )
ON CONFLICT DO NOTHING;

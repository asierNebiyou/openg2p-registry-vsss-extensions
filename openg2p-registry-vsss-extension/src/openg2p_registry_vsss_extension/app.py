# ruff: noqa: E402
import asyncio
import logging

from sqlalchemy import text

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_fastapi_common.context import dbengine
from openg2p_registry_core.app import Initializer as CoreInitializer
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeFormSubmission

from .register_domain.models import (
    G2PRegisterHousehold, G2PRegisterHistoryHousehold, G2PIntakeFormHousehold,
    G2PRegisterHouseholdProgram, G2PRegisterHistoryHouseholdProgram, G2PIntakeFormHouseholdProgram,
    G2PRegisterIndividual, G2PRegisterHistoryIndividual, G2PIntakeFormIndividual,
    G2PRegisterIndividualDisability, G2PRegisterHistoryIndividualDisability, G2PIntakeFormIndividualDisability,
    G2PRegisterIndividualLivestock, G2PRegisterHistoryIndividualLivestock, G2PIntakeFormIndividualLivestock,
    G2PRegisterIndividualProgram, G2PRegisterHistoryIndividualProgram, G2PIntakeFormIndividualProgram,
    G2PRegisterHouseholdShock, G2PRegisterHistoryHouseholdShock, G2PIntakeFormHouseholdShock,
    G2PRegisterVillage, G2PRegisterHistoryVillage, G2PIntakeFormVillage,
)
from .register_domain.factory import G2PRegisterDomainFactory
from .register_domain.listeners import register_intake_submission_listeners
from .register_domain.services import (
    G2PRegisterDomainServiceHousehold,
    G2PRegisterDomainServiceIndividual,
    G2PRegisterDomainServiceHouseholdProgram,
    G2PRegisterDomainServiceIndividualDisability,
    G2PRegisterDomainServiceIndividualLivestock,
    G2PRegisterDomainServiceIndividualProgram,
    G2PRegisterDomainServiceHouseholdShock,
    G2PRegisterDomainServiceVillage,
)

_logger = logging.getLogger(_config.logging_default_logger_name)

# SQLAlchemy create_all does not ADD columns on existing tables. VSSS migrate
# therefore ensures domain + intake columns required by the installed models.
_VSSS_HOUSEHOLD_COLUMNS = (
    ("village_code", "varchar"),
    ("village_name", "varchar"),
    ("region", "varchar"),
    ("district", "varchar"),
    ("subcounty", "varchar"),
    ("parish", "varchar"),
    ("grant_status", "varchar"),
    ("primary_contact_phone", "varchar"),
    ("national_id", "varchar"),
)

_VSSS_HOUSEHOLD_TABLES = (
    "g2p_register_households",
    "g2p_intake_form_households",
    "g2p_register_history_households",
)


async def _ensure_column(conn, table: str, column: str, coltype: str) -> None:
    await conn.execute(
        text(
            f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column} {coltype}"
        )
    )


async def _ensure_vsss_schema(conn) -> None:
    for table in _VSSS_HOUSEHOLD_TABLES:
        for column, coltype in _VSSS_HOUSEHOLD_COLUMNS:
            await _ensure_column(conn, table, column, coltype)

    # Registry config branding fields used by Staff Portal
    await _ensure_column(conn, "g2p_registry_configuration", "registry_favicon", "text")
    await _ensure_column(conn, "g2p_registry_configuration", "registry_theme_id", "varchar")
    await _ensure_column(conn, "g2p_registry_configuration", "registry_language_id", "varchar")

    # Intake list/search requires application_reference on core submissions table
    await _ensure_column(
        conn, "g2p_intake_form_submissions", "application_reference", "varchar"
    )
    await _ensure_column(conn, "g2p_intake_form_submissions", "awe_request_id", "varchar")
    await _ensure_column(
        conn, "g2p_intake_form_submissions", "awe_request_status_summary", "text"
    )
    await conn.execute(
        text(
            """
            UPDATE g2p_intake_form_submissions
            SET application_reference = COALESCE(
                application_reference, 'APP-' || submission_id::text
            )
            WHERE application_reference IS NULL
            """
        )
    )
    await conn.execute(
        text(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
            ix_g2p_intake_form_submissions_application_reference
            ON g2p_intake_form_submissions (application_reference)
            """
        )
    )

    # Gen2 ORM binds submission_id as UUID; older VSSS DBs used varchar.
    await conn.execute(
        text(
            """
            DO $$
            DECLARE r record;
            BEGIN
              FOR r IN
                SELECT c.table_name, c.column_name
                FROM information_schema.columns c
                WHERE c.table_schema = 'public'
                  AND c.column_name = 'submission_id'
                  AND c.data_type = 'character varying'
              LOOP
                EXECUTE format(
                  'ALTER TABLE %I ALTER COLUMN %I TYPE uuid USING %I::uuid',
                  r.table_name, r.column_name, r.column_name
                );
              END LOOP;
            END $$;
            """
        )
    )

    # Legacy VSSS columns remain on submissions; ORM inserts omit them, so they
    # need defaults / nullability or draft create fails with NOT NULL errors.
    await conn.execute(
        text(
            """
            DO $$
            BEGIN
              IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'g2p_intake_form_submissions'
                  AND column_name = 'submission_reference'
              ) THEN
                CREATE SEQUENCE IF NOT EXISTS
                  g2p_intake_form_submissions_submission_reference_seq;
                PERFORM setval(
                  'g2p_intake_form_submissions_submission_reference_seq',
                  GREATEST(
                    COALESCE(
                      (SELECT MAX(submission_reference)
                       FROM g2p_intake_form_submissions),
                      1000
                    ),
                    1000
                  )
                );
                ALTER TABLE g2p_intake_form_submissions
                  ALTER COLUMN submission_reference
                  SET DEFAULT nextval(
                    'g2p_intake_form_submissions_submission_reference_seq'
                  );
              END IF;
            END $$;
            """
        )
    )
    for col, default in (
        ("tab_id", "'village_intake_tab'"),
        ("intake_form_status", "'DRAFT'"),
        ("change_request_submission_status", "'NOT_APPLICABLE'"),
        ("submission_no_of_attempts", "0"),
        ("no_of_verifications_required", "0"),
        ("no_of_verifications_done", "0"),
        ("created_at", "NOW()"),
    ):
        await conn.execute(
            text(
                f"""
                DO $$
                BEGIN
                  IF EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = 'g2p_intake_form_submissions'
                      AND column_name = '{col}'
                  ) THEN
                    ALTER TABLE g2p_intake_form_submissions
                      ALTER COLUMN {col} SET DEFAULT {default};
                  END IF;
                END $$;
                """
            )
        )

    # Lookup tables used by seed SQL. Older registry-platform migrate paths
    # may skip them; create_all also will not add missing tables after a
    # partial first migrate.
    await conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS g2p_attributes (
              attribute_id varchar PRIMARY KEY,
              attribute_code varchar NOT NULL UNIQUE,
              attribute_display varchar NOT NULL,
              is_hierarchical boolean NOT NULL DEFAULT false
            )
            """
        )
    )
    await conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS g2p_attribute_values (
              value_id varchar PRIMARY KEY,
              attribute_id varchar NOT NULL,
              value_code varchar NOT NULL,
              value_display varchar NOT NULL,
              parent_value_id varchar,
              sort_order integer NOT NULL DEFAULT 0
            )
            """
        )
    )

    # Document catalog must match Gen2 G2PRegistryDocument (bucket/source_filename/...)
    await _ensure_column(conn, "g2p_registry_documents", "bucket", "varchar")
    await _ensure_column(conn, "g2p_registry_documents", "source_filename", "varchar")
    await _ensure_column(conn, "g2p_registry_documents", "created_by", "varchar")
    await _ensure_column(
        conn, "g2p_registry_documents", "created_at", "timestamp without time zone"
    )
    await conn.execute(
        text(
            """
            DO $$
            BEGIN
              IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'g2p_registry_documents'
                  AND column_name = 'filename'
              ) THEN
                UPDATE g2p_registry_documents
                SET source_filename = COALESCE(
                  NULLIF(source_filename, ''),
                  NULLIF(filename, ''),
                  document_id
                );
              ELSE
                UPDATE g2p_registry_documents
                SET source_filename = COALESCE(
                  NULLIF(source_filename, ''),
                  document_id
                );
              END IF;
            END $$;
            """
        )
    )
    await conn.execute(
        text(
            """
            UPDATE g2p_registry_documents
            SET
              bucket = COALESCE(NULLIF(bucket, ''), 'default'),
              created_by = COALESCE(NULLIF(created_by, ''), 'system'),
              created_at = COALESCE(created_at, NOW())
            """
        )
    )
    await conn.execute(
        text(
            """
            ALTER TABLE g2p_registry_documents
              ALTER COLUMN bucket SET DEFAULT 'default'
            """
        )
    )

    # Change-request create: legacy NOT NULL columns omitted by Gen2 ORM inserts
    await conn.execute(
        text(
            """
            DO $$
            BEGIN
              IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'g2p_register_change_requests'
                  AND column_name = 'is_primary_section'
              ) THEN
                ALTER TABLE g2p_register_change_requests
                  ALTER COLUMN is_primary_section SET DEFAULT false;
              END IF;
              IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'g2p_register_change_requests'
                  AND column_name = 'edit_action'
              ) THEN
                ALTER TABLE g2p_register_change_requests
                  ALTER COLUMN edit_action SET DEFAULT 'UPDATE';
              END IF;
            END $$;
            """
        )
    )

    # Score definitions: newer ORM queries by register_mnemonic
    await _ensure_column(
        conn, "g2p_register_score_definitions", "register_mnemonic", "varchar"
    )


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()
        CoreInitializer().initialize()

        G2PRegisterDomainServiceHousehold()
        G2PRegisterDomainServiceIndividual()
        G2PRegisterDomainServiceHouseholdProgram()
        G2PRegisterDomainServiceIndividualDisability()
        G2PRegisterDomainServiceIndividualLivestock()
        G2PRegisterDomainServiceIndividualProgram()
        G2PRegisterDomainServiceHouseholdShock()
        G2PRegisterDomainServiceVillage()

        G2PRegisterDomainFactory()
        register_intake_submission_listeners()

    def migrate_database(self, args):
        async def migrate():
            _logger.info("Migrating VSSS extensions database")

            await G2PIntakeFormSubmission.create_migrate()

            await G2PRegisterVillage.create_migrate()
            await G2PRegisterHistoryVillage.create_migrate()
            await G2PIntakeFormVillage.create_migrate()

            await G2PRegisterHousehold.create_migrate()
            await G2PRegisterHistoryHousehold.create_migrate()
            await G2PIntakeFormHousehold.create_migrate()
            await G2PRegisterHouseholdProgram.create_migrate()
            await G2PRegisterHistoryHouseholdProgram.create_migrate()
            await G2PIntakeFormHouseholdProgram.create_migrate()

            await G2PRegisterIndividual.create_migrate()
            await G2PRegisterHistoryIndividual.create_migrate()
            await G2PIntakeFormIndividual.create_migrate()
            await G2PRegisterIndividualDisability.create_migrate()
            await G2PRegisterHistoryIndividualDisability.create_migrate()
            await G2PIntakeFormIndividualDisability.create_migrate()
            await G2PRegisterIndividualLivestock.create_migrate()
            await G2PRegisterHistoryIndividualLivestock.create_migrate()
            await G2PIntakeFormIndividualLivestock.create_migrate()
            await G2PRegisterIndividualProgram.create_migrate()
            await G2PRegisterHistoryIndividualProgram.create_migrate()
            await G2PIntakeFormIndividualProgram.create_migrate()
            await G2PRegisterHouseholdShock.create_migrate()
            await G2PRegisterHistoryHouseholdShock.create_migrate()
            await G2PIntakeFormHouseholdShock.create_migrate()

            engine = dbengine.get()
            async with engine.begin() as conn:
                await _ensure_vsss_schema(conn)

            _logger.info("VSSS extension schema migrate complete")

        asyncio.run(migrate())

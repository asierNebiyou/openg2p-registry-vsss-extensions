#!/usr/bin/env python3
"""Load sample data from openg2p-data JSON files into VSSS Mowsa Postgres.

Reads JSON from /openg2p-data (cloned in Dockerfile), maps to VSSS Mowsa schema,
executes parameterised INSERTs via psycopg2.
"""

import json
import os
import sys
from pathlib import Path

import psycopg2
import psycopg2.extras


SEEDER = "seeder"
CREATED_AT = "2026-04-01 00:00:00"

OPENG2P_DATA_DIR = Path(os.environ.get("OPENG2P_DATA_DIR", "/openg2p-data"))
DEMO_DIR = OPENG2P_DATA_DIR / "demography"
DATA_DIR = OPENG2P_DATA_DIR / "national-social-registry"


def env(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        print(f"[load-sample-data] Missing env var: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def load_json(path: Path):
    if not path.is_file():
        print(f"[load-sample-data] Missing file: {path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text())


def search_text_individual(ind: dict) -> str:
    parts = [
        ind["functional_record_id"],
        ind["full_name"],
        ind["foundational_id"] or "",
        ind["foundational_id_masked"] or "",
        ind["gender"] or "",
        ind["birth_date"] or "",
        str(ind.get("estimated_age") or ""),
        ind.get("marital_status") or "",
    ]
    return " ".join(p for p in parts if p)


def search_text_household(hh: dict) -> str:
    parts = [
        hh["functional_record_id"],
        hh["head_name"],
        hh["headship_type"],
        str(hh["size_total"]),
    ]
    return " ".join(p for p in parts if p)


def insert_individuals(cur, individuals: list[dict]) -> None:
    columns = [
        "internal_record_id",
        "functional_record_id",
        "link_internal_record_id",
        "link_foundational_id",
        "record_name",
        "record_image_storage_id",
        "created_by",
        "created_at",
        "last_approved_at",
        "last_approved_by",
        "search_text",
        "record_status",
        "record_status_reason",
        "foundational_id",
        "first_name",
        "middle_name",
        "last_name",
        "given_name",
        "prefix",
        "suffix",
        "gender",
        "birth_date",
        "phone_numbers",
        "emails",
        "marital_status",
        "occupation",
        "income_level",
        "language_code",
        "education_level",
        "registration_date",
        "latitude",
        "longitude",
        "altitude",
        "plus_code",
        "address_line_1",
        "address_line_2",
        "postal_code",
        "country_code",
        "geo_lowest_level_value_id",
        "geo_code_hierarchy_json",
        "foundational_id_masked",
        "foundational_id_verification_status",
        "full_name",
        "estimated_age",
        "age_method",
    ]
    rows = []
    for ind in individuals:
        rows.append(
            (
                ind["internal_record_id"],
                ind["functional_record_id"],
                None,
                None,
                ind["full_name"],
                None,
                SEEDER,
                CREATED_AT,
                CREATED_AT,
                SEEDER,
                search_text_individual(ind),
                "ACTIVE",
                None,
                ind["foundational_id"],
                ind["first_name"],
                ind.get("middle_name"),
                ind["last_name"],
                ind["given_name"],
                None,
                None,
                ind["gender"],
                ind["birth_date"],
                json.dumps(ind["phone_numbers"]),
                ind.get("emails"),
                ind["marital_status"],
                None,
                None,
                ind.get("language_code"),
                ind.get("education_level"),
                "2026-04-01",
                ind["latitude"],
                ind["longitude"],
                ind["altitude"],
                ind["plus_code"],
                ind["address_line_1"],
                ind["address_line_2"],
                ind["postal_code"],
                ind["country_code"],
                ind["geo_village_id"],
                json.dumps(ind["geo_hierarchy_json"]),
                ind["foundational_id_masked"],
                "VERIFIED",
                ind["full_name"],
                ind["estimated_age"],
                "DOCUMENTED",
            )
        )
    sql = (
        f'INSERT INTO "public"."g2p_register_individuals" ('
        + ", ".join(f'"{c}"' for c in columns)
        + ") VALUES %s"
    )
    psycopg2.extras.execute_values(cur, sql, rows, template=None, page_size=200)
    print(f"[load-sample-data]   -> g2p_register_individuals: {len(rows)}")


def insert_households(cur, households: list[dict]) -> None:
    columns = [
        "internal_record_id",
        "functional_record_id",
        "link_internal_record_id",
        "link_foundational_id",
        "record_name",
        "record_image_storage_id",
        "created_by",
        "created_at",
        "last_approved_at",
        "last_approved_by",
        "search_text",
        "record_status",
        "record_status_reason",
        "latitude",
        "longitude",
        "altitude",
        "plus_code",
        "address_line_1",
        "address_line_2",
        "postal_code",
        "country_code",
        "geo_lowest_level_value_id",
        "geo_code_hierarchy_json",
        "household_head_internal_record_id",
        "household_head_name",
        "headship_type",
        "size_total",
        "size_adults",
        "size_children_u5",
        "size_school_age",
        "size_elderly",
        "number_of_female_members",
        "number_of_male_members",
        "elderly_member_present",
    ]
    rows = []
    for hh in households:
        rows.append(
            (
                hh["internal_record_id"],
                hh["functional_record_id"],
                None,
                None,
                f"{hh['head_name']} {hh['functional_record_id']}",
                None,
                SEEDER,
                CREATED_AT,
                CREATED_AT,
                SEEDER,
                search_text_household(hh),
                "ACTIVE",
                None,
                hh["latitude"],
                hh["longitude"],
                hh["altitude"],
                hh["plus_code"],
                hh["address_line_1"],
                hh["address_line_2"],
                hh["postal_code"],
                hh["country_code"],
                hh["geo_village_id"],
                json.dumps(hh["geo_hierarchy_json"]),
                hh["head_individual_id"],
                hh["head_name"],
                hh["headship_type"],
                hh["size_total"],
                hh["size_adults"],
                hh["size_children_u5"],
                hh["size_school_age"],
                hh["size_elderly"],
                hh["number_of_female_members"],
                hh["number_of_male_members"],
                "TRUE" if hh["size_elderly"] > 0 else "FALSE",
            )
        )
    sql = (
        f'INSERT INTO "public"."g2p_register_households" ('
        + ", ".join(f'"{c}"' for c in columns)
        + ") VALUES %s"
    )
    psycopg2.extras.execute_values(cur, sql, rows, template=None, page_size=200)
    print(f"[load-sample-data]   -> g2p_register_households: {len(rows)}")


# Sub-table mappings: (table_name, json_filename, extra_columns_in_order)
SUB_TABLES = [
    (
        "g2p_register_individual_livelihoods",
        "individual_livelihoods.json",
        ["primary_livelihood", "secondary_livelihood", "employment_status", "coping_strategies_index", "mobile_phone_type"],
    ),
    (
        "g2p_register_individual_livestock",
        "individual_livestock.json",
        ["livestock_species", "livestock_counts"],
    ),
    (
        "g2p_register_individual_land",
        "individual_land.json",
        ["land_access", "land_size", "productive_assets"],
    ),
    (
        "g2p_register_individual_shocks",
        "individual_shocks.json",
        ["shock_type", "shock_date", "shock_period", "coping_strategy"],
    ),
    (
        "g2p_register_individual_disabilities",
        "individual_disabilities.json",
        ["disability_domain", "disability_severity"],
    ),
    (
        "g2p_register_individual_vulnerability",
        "individual_vulnerability.json",
        [
            "disability_status",
            "orphanhood_flag",
            "chronic_illness_flag",
            "displacement_status",
            "pastoralist_classification",
            "high_mobility_indicator",
            "plw_status",
            "plw_status_date",
        ],
    ),
    (
        "g2p_register_individual_programs",
        "individual_programs.json",
        ["program_name", "program_start_date", "program_exit_date"],
    ),
    (
        "g2p_register_household_assets",
        "household_assets.json",
        ["asset_type", "asset_category", "quantity", "size_value", "size_unit", "size_band", "details"],
    ),
    (
        "g2p_register_household_housing_and_services",
        "household_housing_and_services.json",
        [
            "dwelling_type",
            "roof_material",
            "wall_material",
            "floor_material",
            "tenure_status",
            "water_source_type",
            "water_distance_minutes",
            "sanitation_type",
            "lighting_source",
            "cooking_fuel_type",
        ],
    ),
    (
        "g2p_register_household_programs",
        "household_programs.json",
        ["program_name", "program_start_date", "program_exit_date"],
    ),
]

COMMON_COLUMNS = [
    "internal_record_id",
    "functional_record_id",
    "link_internal_record_id",
    "link_foundational_id",
    "record_name",
    "record_image_storage_id",
    "created_by",
    "created_at",
    "last_approved_at",
    "last_approved_by",
    "search_text",
    "record_status",
    "record_status_reason",
]


def insert_sub_table(cur, table: str, rows_json: list[dict], extra_cols: list[str]) -> None:
    if not rows_json:
        print(f"[load-sample-data]   -> {table}: 0 (empty)")
        return
    columns = COMMON_COLUMNS + extra_cols
    rows = []
    for r in rows_json:
        common = [
            r["internal_record_id"],
            r["functional_record_id"],
            r["link_internal_record_id"],
            r.get("link_foundational_id"),
            r["record_name"],
            r.get("record_image_storage_id"),
            r.get("created_by", SEEDER),
            r.get("created_at", CREATED_AT),
            r.get("last_approved_at", CREATED_AT),
            r.get("last_approved_by", SEEDER),
            r["search_text"],
            r.get("record_status", "ACTIVE"),
            r.get("record_status_reason"),
        ]
        extras = [r.get(c) for c in extra_cols]
        rows.append(tuple(common + extras))

    sql = (
        f'INSERT INTO "public"."{table}" ('
        + ", ".join(f'"{c}"' for c in columns)
        + ") VALUES %s"
    )
    psycopg2.extras.execute_values(cur, sql, rows, template=None, page_size=200)
    print(f"[load-sample-data]   -> {table}: {len(rows)}")


def insert_scores(cur, scores: list[dict]) -> None:
    if not scores:
        return
    columns = [
        "internal_record_id",
        "register_id",
        "score_type",
        "score_definition_id",
        "link_internal_record_id",
        "triggered_by_cr_id",
        "triggered_by_submission_id",
        "computed_score",
        "computed_at",
    ]
    rows = [tuple(r.get(c) for c in columns) for r in scores]
    sql = (
        f'INSERT INTO "public"."g2p_register_scores" ('
        + ", ".join(f'"{c}"' for c in columns)
        + ") VALUES %s"
    )
    psycopg2.extras.execute_values(cur, sql, rows, template=None, page_size=200)
    print(f"[load-sample-data]   -> g2p_register_scores: {len(rows)}")


def main() -> None:
    print("[load-sample-data] Starting…")
    print(f"[load-sample-data] OPENG2P_DATA_DIR = {OPENG2P_DATA_DIR}")

    individuals = load_json(DEMO_DIR / "individuals.json")
    households = load_json(DEMO_DIR / "households.json")

    conn = psycopg2.connect(
        host=env("PGHOST"),
        port=os.environ.get("PGPORT", "5432"),
        dbname=env("PGDATABASE"),
        user=env("PGUSER"),
        password=env("PGPASSWORD"),
    )
    conn.autocommit = False
    cur = conn.cursor()

    try:
        insert_individuals(cur, individuals)
        insert_households(cur, households)
        for table, fname, extras in SUB_TABLES:
            rows = load_json(DATA_DIR / fname)
            insert_sub_table(cur, table, rows, extras)
        scores = load_json(DATA_DIR / "scores.json")
        insert_scores(cur, scores)
        conn.commit()
        print("[load-sample-data] Done.")
    except Exception as exc:
        conn.rollback()
        print(f"[load-sample-data] FAILED: {exc}", file=sys.stderr)
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()

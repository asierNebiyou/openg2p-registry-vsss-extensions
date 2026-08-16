from dataclasses import dataclass
from datetime import date

from openg2p_registry_core.models import RecordStatusEnum
from sqlalchemy import select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain_validation_utils import as_int, parse_date

CHILDREN_U5_MAX_AGE = 4
SCHOOL_AGE_MIN = 5
SCHOOL_AGE_MAX = 17
ADULT_MIN = 18
ADULT_MAX = 59
ELDERLY_MIN = 60

ROSTER_AFFECTING_FIELDS = frozenset(
    {
        "link_internal_record_id",
        "record_status",
        "birth_date",
        "estimated_age",
        "residency_status",
    }
)

GEO_HIERARCHY_FIELDS = frozenset(
    {
        "geo_lowest_level_value_id",
        "geo_code_hierarchy_json",
        "address_descriptor",
        "kebele_code",
        "locality_ea_code",
        "gps_latitude",
        "gps_longitude",
        "gps_accuracy",
    }
)


@dataclass(frozen=True)
class HouseholdRosterAggregates:
    size_total: int
    size_adults: int
    size_children_u5: int
    size_school_age: int
    size_elderly: int
    elderly_member_present: bool
    overcrowding_indicator: float | None = None


def normalize_link(value) -> str | None:
    if value is None or value == "":
        return None
    normalized = str(value).strip()
    return normalized or None


def has_roster_affecting_changes(change_payload: dict) -> bool:
    return any(key in change_payload for key in ROSTER_AFFECTING_FIELDS)


def has_geo_affecting_changes(change_payload: dict) -> bool:
    return any(key in change_payload for key in GEO_HIERARCHY_FIELDS)


def member_payload(individual, change_payload: dict) -> dict:
    base = individual.to_dict()
    overlay = {
        key: value
        for key, value in change_payload.items()
        if key in ROSTER_AFFECTING_FIELDS or key == "internal_record_id"
    }
    return {**base, **overlay}


def affected_household_ids(old_link: str | None, new_link: str | None) -> set[str]:
    household_ids: set[str] = set()
    if old_link:
        household_ids.add(old_link)
    if new_link:
        household_ids.add(new_link)
    return household_ids


def calculate_age(birth_date: date, today: date | None = None) -> int | None:
    if not birth_date:
        return None
    today = today or date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def resolve_member_age(member: dict, today: date | None = None) -> int | None:
    birth_date = parse_date(member.get("birth_date"))
    if birth_date is not None:
        return calculate_age(birth_date, today)
    return as_int(member.get("estimated_age"))


def is_active_member(member: dict) -> bool:
    record_status = member.get("record_status") or RecordStatusEnum.ACTIVE.value
    return record_status == RecordStatusEnum.ACTIVE.value


def calculate_overcrowding_indicator(
    size_total: int, rooms_count: int | float | None
) -> float | None:
    if not rooms_count:
        return None
    return size_total / rooms_count


def compute_household_roster_counts(
    members: list[dict],
    today: date | None = None,
    rooms_count: int | float | None = None,
) -> HouseholdRosterAggregates:
    size_total = 0
    size_children_u5 = 0
    size_school_age = 0
    size_adults = 0
    size_elderly = 0

    for member in members:
        if not is_active_member(member):
            continue

        size_total += 1
        age = resolve_member_age(member, today)
        if age is not None:
            if age <= CHILDREN_U5_MAX_AGE:
                size_children_u5 += 1
            elif SCHOOL_AGE_MIN <= age <= SCHOOL_AGE_MAX:
                size_school_age += 1
            elif ADULT_MIN <= age <= ADULT_MAX:
                size_adults += 1
            elif age >= ELDERLY_MIN:
                size_elderly += 1

    return HouseholdRosterAggregates(
        size_total=size_total,
        size_adults=size_adults,
        size_children_u5=size_children_u5,
        size_school_age=size_school_age,
        size_elderly=size_elderly,
        elderly_member_present=size_elderly > 0,
        overcrowding_indicator=calculate_overcrowding_indicator(size_total, rooms_count),
    )


def apply_household_roster_counts(household, aggregates: HouseholdRosterAggregates) -> None:
    household.household_size_total = aggregates.size_total
    household.household_size_adults = aggregates.size_adults
    household.household_size_children_u5 = aggregates.size_children_u5
    household.household_size_school_age = aggregates.size_school_age
    household.household_size_elderly = aggregates.size_elderly
    household.elderly_member_present = aggregates.elderly_member_present
    household.overcrowding_indicator = aggregates.overcrowding_indicator


def household_geo_payload(household) -> dict:
    return {field: getattr(household, field, None) for field in GEO_HIERARCHY_FIELDS}


def apply_geo_hierarchy_to_individual(individual, geo_payload: dict) -> None:
    for field, value in geo_payload.items():
        setattr(individual, field, value)


async def propagate_household_geo_to_members(
    session: AsyncSession,
    household,
    geo_payload: dict | None = None,
) -> None:
    from ...models.individual import G2PRegisterIndividual

    if geo_payload is None:
        geo_payload = household_geo_payload(household)

    await session.execute(
        sa_update(G2PRegisterIndividual)
        .where(G2PRegisterIndividual.link_internal_record_id == household.internal_record_id)
        .values(**geo_payload)
    )


async def recompute_household_roster_for_household(
    session: AsyncSession,
    household_internal_record_id: str,
    *,
    changed_member_id: str | None = None,
    changed_member_payload: dict | None = None,
) -> None:
    from ...models.household import G2PRegisterHousehold
    from ...models.individual import G2PRegisterIndividual

    household = await session.get(G2PRegisterHousehold, household_internal_record_id)
    if not household:
        return

    members_result = await session.execute(
        select(G2PRegisterIndividual).where(
            G2PRegisterIndividual.link_internal_record_id == household_internal_record_id
        )
    )
    members_by_id = {
        member.internal_record_id: member.to_dict()
        for member in members_result.scalars().all()
    }

    if changed_member_id and changed_member_payload is not None:
        effective_link = normalize_link(changed_member_payload.get("link_internal_record_id"))
        if (
            effective_link == household_internal_record_id
            and is_active_member(changed_member_payload)
        ):
            members_by_id[changed_member_id] = changed_member_payload
        elif changed_member_id in members_by_id:
            del members_by_id[changed_member_id]

    aggregates = compute_household_roster_counts(
        list(members_by_id.values()),
        rooms_count=getattr(household, "rooms_count", None),
    )
    apply_household_roster_counts(household, aggregates)
    await propagate_household_geo_to_members(session, household)
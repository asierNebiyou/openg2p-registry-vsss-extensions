from enum import Enum



class HeadshipTypeEnum(str, Enum):
    FEMALE_HEADED = "FEMALE_HEADED"
    CHILD_HEADED = "CHILD_HEADED"
    ELDERLY_HEADED = "ELDERLY_HEADED"
    DISABLED_HEADED = "DISABLED_HEADED"
    MALE_HEADED = "MALE_HEADED"


class ResidencyStatusEnum(str, Enum):
    USUAL_MEMBER = "USUAL_MEMBER"
    TEMPORARY = "TEMPORARY"
    ABSENT = "ABSENT"


class RelationshipToHeadEnum(str, Enum):
    SPOUSE = "SPOUSE"
    CHILD = "CHILD"
    PARENT = "PARENT"
    OTHER = "OTHER"


class PreferredContactMethodEnum(str, Enum):
    CALL = "CALL"
    SMS = "SMS"
    THROUGH_KEBELE = "THROUGH_KEBELE"


class CitizenshipCategoryEnum(str, Enum):
    CITIZEN = "CITIZEN"
    REFUGEE = "REFUGEE"
    IDP = "IDP"
    RETURNEE = "RETURNEE"
    RESIDENT = "RESIDENT"


class DisabilityStatusEnum(str, Enum):
    YES = "YES"
    NO = "NO"
    UNKNOWN = "UNKNOWN"


class DisabilitySeverityEnum(str, Enum):
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"

class DisabilityDomainEnum(str, Enum):
    PHYSICAL = "PHYSICAL"
    SENSORY = "SENSORY"
    INTELLECTUAL = "INTELLECTUAL"
    MENTAL_HEALTH = "MENTAL_HEALTH"
    OTHER = "OTHER"

class DisplacementStatusEnum(str, Enum):
    IDP = "IDP"
    RETURNEE = "RETURNEE"
    REFUGEE = "REFUGEE"
    HOST_COMMUNITY = "HOST_COMMUNITY"


class PastoralistClassificationEnum(str, Enum):
    PASTORALIST = "PASTORALIST"
    SEMI_PASTORALIST = "SEMI_PASTORALIST"
    SETTLED = "SETTLED"


class DwellingTypeEnum(str, Enum):
    PERMANENT = "PERMANENT"
    SEMI = "SEMI"
    TEMPORARY = "TEMPORARY"


class TenureStatusEnum(str, Enum):
    OWNED = "OWNED"
    RENTED = "RENTED"


class EmploymentStatusEnum(str, Enum):
    EMPLOYED = "EMPLOYED"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    UNEMPLOYED = "UNEMPLOYED"
    STUDENT = "STUDENT"
    OTHER = "OTHER"


class ShockTypeEnum(str, Enum):
    DROUGHT = "DROUGHT"
    FLOOD = "FLOOD"
    CONFLICT = "CONFLICT"
    ILLNESS = "ILLNESS"
    OTHER = "OTHER"


class HouseholdAssetsEnum(str, Enum):
    RADIO = "RADIO"
    TV = "TV"
    FRIDGE = "FRIDGE"
    BICYCLE = "BICYCLE"
    MOTORCYCLE = "MOTORCYCLE"


class MobilePhoneTypeEnum(str, Enum):
    BASIC = "BASIC"
    SMARTPHONE = "SMARTPHONE"


class LightingSourceEnum(str, Enum):
    GRID = "GRID"
    SOLAR = "SOLAR"
    KEROSENE = "KEROSENE"


class AgeMethodEnum(str, Enum):
    DOCUMENTED = "DOCUMENTED"
    ESTIMATED = "ESTIMATED"
    CALCULATED = "CALCULATED"


class RidStatusEnum(str, Enum):
    PENDING = "PENDING"
    SUCCESS_PROCESSED = "SUCCESS_PROCESSED"
    FAIL_FAILED = "FAIL_FAILED"
    FAIL_REJECTED = "FAIL_REJECTED"
    FAIL_PROCESSED_NO_DATA = "FAIL_PROCESSED_NO_DATA"


class MaritalStatusEnum(str, Enum):
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DIVORCED = "DIVORCED"
    WIDOWED = "WIDOWED"
    SEPARATED = "SEPARATED"
    UNKNOWN = "UNKNOWN"


class LivestockSpeciesEnum(str, Enum):
    CATTLE = "CATTLE"
    GOATS = "GOATS"
    SHEEP = "SHEEP"
    POULTRY = "POULTRY"
    CAMELS = "CAMELS"
    EQUINES = "EQUINES"
    OTHER = "OTHER"


class LivestockCountBandEnum(str, Enum):
    BAND_1_5 = "BAND_1_5"
    BAND_6_10 = "BAND_6_10"
    BAND_11_20 = "BAND_11_20"
    BAND_21_50 = "BAND_21_50"
    BAND_50_PLUS = "BAND_50_PLUS"


class DataQualityFlagsEnum(str, Enum):
    MISSING_KEY_FIELDS = "MISSING_KEY_FIELDS"
    SUSPECTED_DUPLICATE = "SUSPECTED_DUPLICATE"
    INCONSISTENT = "INCONSISTENT"


class LivelihoodEnum(str, Enum):
    AGRICULTURE = "AGRICULTURE"
    LIVESTOCK = "LIVESTOCK"
    FISHING = "FISHING"
    WAGE_LABOR = "WAGE_LABOR"
    SELF_EMPLOYMENT = "SELF_EMPLOYMENT"
    GOVERNMENT_EMPLOYEE = "GOVERNMENT_EMPLOYEE"
    PRIVATE_SECTOR_EMPLOYEE = "PRIVATE_SECTOR_EMPLOYEE"
    BUSINESS_TRADE = "BUSINESS_TRADE"
    REMITTANCE = "REMITTANCE"
    PENSION = "PENSION"
    UNEMPLOYED = "UNEMPLOYED"
    OTHER = "OTHER"


class RoofMaterialEnum(str, Enum):
    THATCH = "THATCH"
    CORRUGATED_IRON = "CORRUGATED_IRON"
    CONCRETE = "CONCRETE"
    TILE = "TILE"
    PLASTIC_SHEET = "PLASTIC_SHEET"
    OTHER = "OTHER"


class WallMaterialEnum(str, Enum):
    MUD = "MUD"
    WOOD = "WOOD"
    BAMBOO = "BAMBOO"
    STONE = "STONE"
    BRICK = "BRICK"
    CONCRETE = "CONCRETE"
    OTHER = "OTHER"


class FloorMaterialEnum(str, Enum):
    EARTH = "EARTH"
    WOOD = "WOOD"
    CEMENT = "CEMENT"
    TILE = "TILE"
    OTHER = "OTHER"


class CookingFuelTypeEnum(str, Enum):
    FIREWOOD = "FIREWOOD"
    CHARCOAL = "CHARCOAL"
    ELECTRICITY = "ELECTRICITY"
    LPG = "LPG"
    BIOGAS = "BIOGAS"
    KEROSENE = "KEROSENE"
    DUNG = "DUNG"
    OTHER = "OTHER"


class WaterSourceTypeEnum(str, Enum):
    PIPED = "PIPED"
    BOREHOLE = "BOREHOLE"
    PROTECTED_WELL = "PROTECTED_WELL"
    UNPROTECTED_WELL = "UNPROTECTED_WELL"
    SPRING = "SPRING"
    RIVER = "RIVER"
    RAINWATER = "RAINWATER"
    TANKER_TRUCK = "TANKER_TRUCK"
    OTHER = "OTHER"


class SanitationTypeEnum(str, Enum):
    FLUSH_TOILET = "FLUSH_TOILET"
    PIT_LATRINE = "PIT_LATRINE"
    VENTILATED_IMPROVED_PIT = "VENTILATED_IMPROVED_PIT"
    COMPOSTING_TOILET = "COMPOSTING_TOILET"
    OPEN_DEFECATION = "OPEN_DEFECATION"
    OTHER = "OTHER"


class ProductiveAssetEnum(str, Enum):
    PLOUGH = "PLOUGH"
    IRRIGATION_PUMP = "IRRIGATION_PUMP"
    OTHER = "OTHER"

class ProgramEnum(str, Enum):
    UPSNP = "UPSNP"
    RPSNP = "RPSNP"
    
class EducationalStatusEnum(str, Enum):
    NEVER_ATTEND = "NEVER_ATTEND"
    NON_FORMAL = "NON_FORMAL"
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    HIGHER_EDUCATION = "HIGHER_EDUCATION"

class PrefixEnum(str, Enum):
    MR = "Mr"
    MRS = "Mrs"
    MISS = "Miss"

class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHERS = "OTHERS"
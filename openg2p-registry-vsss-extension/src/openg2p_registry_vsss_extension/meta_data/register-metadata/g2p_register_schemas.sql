INSERT INTO
  "public"."g2p_register_schemas" (
    "register_id",
    "deduplicate_schema",
    "search_result_schema",
    "filter_schema"
  )
VALUES
  (
    'e7c8f2a1-4b5d-4e6f-9a0b-1c2d3e4f5a6b',
    '[{"field_name": "village_code", "match_type": "EXACT", "weight": 0.5, "similarity_threshold": 1}, {"field_name": "village_name", "match_type": "EXACT", "weight": 0.5, "similarity_threshold": 1}]',
    '[{"field_name": "village_code", "display_label": "Village Code", "order": 1}, {"field_name": "village_name", "display_label": "Village Name", "order": 2}, {"field_name": "district", "display_label": "District", "order": 3}, {"field_name": "subcounty", "display_label": "Subcounty", "order": 4}, {"field_name": "parish", "display_label": "Parish", "order": 5}, {"field_name": "grant_status", "display_label": "Grant Status", "order": 6}]',
    '[{"field_name": "village_name", "display_label": "Village Name", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]}, {"field_name": "district", "display_label": "District", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]}, {"field_name": "grant_status", "display_label": "Grant Status", "filter_type": "text", "order": 3, "allowed_operators": ["eq", "contains"]}]'
  ),
  (
    '9055ab43-c85d-4833-bd00-ca657bb72644',
    '[]',
    '[{"field_name": "village_name", "display_label": "Village", "order": 1}, {"field_name": "headship_type", "display_label": "Headship", "order": 2}, {"field_name": "household_size_total", "display_label": "Household Size", "order": 3}, {"field_name": "district", "display_label": "District", "order": 4}, {"field_name": "grant_status", "display_label": "Grant Status", "order": 5}, {"field_name": "primary_contact_phone", "display_label": "Phone", "order": 6}]',
    '[{"field_name": "headship_type", "display_label": "Headship Type", "filter_type": "dropdown", "order": 1, "allowed_operators": ["eq", "in"], "options_source": [{"label": "MALE HEADED", "value": "MALE_HEADED"}, {"label": "FEMALE HEADED", "value": "FEMALE_HEADED"}, {"label": "ELDERLY HEADED", "value": "ELDERLY_HEADED"}, {"label": "CHILD HEADED", "value": "CHILD_HEADED"}, {"label": "DISABLED HEADED", "value": "DISABLED_HEADED"}]}, {"field_name": "district", "display_label": "District", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]}, {"field_name": "household_size_total", "display_label": "Household Size", "filter_type": "number_range", "order": 3, "allowed_operators": ["eq", "gt", "lt", "between"]}]'
  ),
  (
    'a1a4d25a-1cd4-4356-abac-985a0b3c6bcd',
    '[{"field_name": "foundational_id", "match_type": "EXACT", "weight": 0.33, "similarity_threshold": 1}, {"field_name": "first_name", "match_type": "EXACT", "weight": 0.33, "similarity_threshold": 1}, {"field_name": "last_name", "match_type": "EXACT", "weight": 0.33, "similarity_threshold": 1}]',
    '[{"field_name": "rid", "display_label": "RID", "order": 1}, {"field_name": "foundational_id", "display_label": "Fayda ID", "order": 2}, {"field_name": "gender", "display_label": "Gender", "order": 3}, {"field_name": "citizenship_category", "display_label": "Citizenship Category", "order": 4}, {"field_name": "primary_phone", "display_label": "Primary Phone", "order": 5}, {"field_name": "employment_status", "display_label": "Employment Status", "order": 6}, {"field_name": "disability_status", "display_label": "Disability Status", "order": 7}]',
    '[{"field_name": "first_name", "display_label": "First Name", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]}, {"field_name": "last_name", "display_label": "Last Name", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]}, {"field_name": "gender", "display_label": "Gender", "filter_type": "dropdown", "order": 3, "allowed_operators": ["eq", "in"], "options_source": [{"value": "MALE", "label": "MALE"}, {"value": "FEMALE", "label": "FEMALE"}, {"value": "OTHERS", "label": "OTHERS"}, {"value": "UNKNOWN", "label": "UNKNOWN"}]}, {"field_name": "birth_date", "display_label": "Birthdate", "filter_type": "date_range", "order": 4, "allowed_operators": ["eq", "gt", "gte", "lt", "lte", "between"]}, {"field_name": "record_status", "display_label": "Record Status", "filter_type": "dropdown", "order": 5, "allowed_operators": ["eq", "in"], "options_source": [{"value": "ACTIVE", "label": "ACTIVE"}, {"value": "INACTIVE", "label": "INACTIVE"}, {"value": "ARCHIVED", "label": "ARCHIVED"}]}]'
  ),
  (
    'c51e60ca-9990-4077-8d62-0b414ea7e66d',
    'null',
    'null',
    'null'
  );
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
    '[{"field_name": "code", "match_type": "EXACT", "weight": 0.5, "similarity_threshold": 1}, {"field_name": "name", "match_type": "EXACT", "weight": 0.5, "similarity_threshold": 1}]',
    '[{"field_name": "code", "display_label": "Code", "order": 1}, {"field_name": "name", "display_label": "Name", "order": 2}, {"field_name": "household_count", "display_label": "Household Count", "order": 3}, {"field_name": "chairperson_name", "display_label": "Chairperson", "order": 4}, {"field_name": "polling_station", "display_label": "Polling Station", "order": 5}]',
    '[{"field_name": "name", "display_label": "Name", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]}, {"field_name": "code", "display_label": "Code", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]}]'
  ),
  (
    '9055ab43-c85d-4833-bd00-ca657bb72644',
    '[{"field_name": "name", "match_type": "EXACT", "weight": 1, "similarity_threshold": 1}]',
    '[{"field_name": "name", "display_label": "Name", "order": 1}, {"field_name": "household_size", "display_label": "Household Size", "order": 2}, {"field_name": "polling_station", "display_label": "Polling Station", "order": 3}, {"field_name": "bank_name", "display_label": "Bank Name", "order": 4}, {"field_name": "grant_status", "display_label": "Grant Status", "order": 5}]',
    '[{"field_name": "name", "display_label": "Name", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]}, {"field_name": "household_size", "display_label": "Household Size", "filter_type": "number_range", "order": 2, "allowed_operators": ["eq", "gt", "lt", "between"]}, {"field_name": "grant_status", "display_label": "Grant Status", "filter_type": "dropdown", "order": 3, "allowed_operators": ["eq", "in"], "options_source": [{"label": "Not Started", "value": "not_started"}, {"label": "Partial", "value": "partial"}, {"label": "Completed", "value": "completed"}, {"label": "Suspended", "value": "suspended"}]}]'
  ),
  (
    'a1a4d25a-1cd4-4356-abac-985a0b3c6bcd',
    '[{"field_name": "first_name", "match_type": "EXACT", "weight": 0.34, "similarity_threshold": 1}, {"field_name": "last_name", "match_type": "EXACT", "weight": 0.33, "similarity_threshold": 1}, {"field_name": "phone", "match_type": "EXACT", "weight": 0.33, "similarity_threshold": 1}]',
    '[{"field_name": "first_name", "display_label": "First Name", "order": 1}, {"field_name": "last_name", "display_label": "Last Name", "order": 2}, {"field_name": "gender", "display_label": "Gender", "order": 3}, {"field_name": "phone", "display_label": "Phone", "order": 4}, {"field_name": "polling_station", "display_label": "Polling Station", "order": 5}]',
    '[{"field_name": "first_name", "display_label": "First Name", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]}, {"field_name": "last_name", "display_label": "Last Name", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]}, {"field_name": "gender", "display_label": "Gender", "filter_type": "dropdown", "order": 3, "allowed_operators": ["eq", "in"], "options_source": [{"value": "MALE", "label": "Male"}, {"value": "FEMALE", "label": "Female"}, {"value": "OTHERS", "label": "Others"}, {"value": "UNKNOWN", "label": "Unknown"}]}, {"field_name": "birth_date", "display_label": "Birthdate", "filter_type": "date_range", "order": 4, "allowed_operators": ["eq", "gt", "gte", "lt", "lte", "between"]}, {"field_name": "phone", "display_label": "Phone", "filter_type": "text", "order": 5, "allowed_operators": ["eq", "contains"]}]'
  ),
  (
    'c51e60ca-9990-4077-8d62-0b414ea7e66d',
    'null',
    'null',
    'null'
  );

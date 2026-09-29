INSERT INTO "public"."g2p_attribute_values" ("value_id","attribute_id","value_code","value_display","parent_value_id","sort_order") VALUES
('GENDER_MALE','GENDER','MALE','Male',NULL,'1'),
('GENDER_FEMALE','GENDER','FEMALE','Female',NULL,'2'),
('GENDER_OTHERS','GENDER','OTHERS','Others',NULL,'3'),
('GENDER_UNKNOWN','GENDER','UNKNOWN','Unknown',NULL,'4'),

('FINANCIAL_MANAGEMENT_GOOD','FINANCIAL_MANAGEMENT','good','Good',NULL,'1'),
('FINANCIAL_MANAGEMENT_FAIR','FINANCIAL_MANAGEMENT','fair','Fair',NULL,'2'),
('FINANCIAL_MANAGEMENT_POOR','FINANCIAL_MANAGEMENT','poor','Poor',NULL,'3'),

('TRAINING_NEEDS_FINANCIAL_LITERACY','TRAINING_NEEDS','financial_literacy','Financial Literacy',NULL,'1'),
('TRAINING_NEEDS_DIGITAL_TOOLS','TRAINING_NEEDS','digital_tools','Digital Tools',NULL,'2'),
('TRAINING_NEEDS_ENTERPRISE_DEVELOPMENT','TRAINING_NEEDS','enterprise_development','Enterprise Development',NULL,'3'),
('TRAINING_NEEDS_RECORD_KEEPING','TRAINING_NEEDS','record_keeping','Record Keeping',NULL,'4'),
('TRAINING_NEEDS_AGRICULTURE','TRAINING_NEEDS','agriculture','Agriculture',NULL,'5'),
('TRAINING_NEEDS_MARKETING','TRAINING_NEEDS','marketing','Marketing',NULL,'6'),
('TRAINING_NEEDS_LEADERSHIP_GOVERNANCE','TRAINING_NEEDS','leadership_governance','Leadership Governance',NULL,'7'),
('TRAINING_NEEDS_NONE','TRAINING_NEEDS','none','None',NULL,'8'),

('LOAN_REQUIREMENT_WORKING_CAPITAL','LOAN_REQUIREMENT','working_capital','Working Capital',NULL,'1'),
('LOAN_REQUIREMENT_ASSET_FINANCING','LOAN_REQUIREMENT','asset_financing','Asset Financing',NULL,'2'),
('LOAN_REQUIREMENT_EMERGENCY_LOAN','LOAN_REQUIREMENT','emergency_loan','Emergency Loan',NULL,'3'),
('LOAN_REQUIREMENT_AGRI_INPUT_LOAN','LOAN_REQUIREMENT','agri_input_loan','Agri Input Loan',NULL,'4'),
('LOAN_REQUIREMENT_BUSINESS_EXPANSION','LOAN_REQUIREMENT','business_expansion','Business Expansion',NULL,'5'),
('LOAN_REQUIREMENT_NOT_REQUIRED','LOAN_REQUIREMENT','not_required','Not Required',NULL,'6'),

('AMOUNT_REQUIRED_IN_ONE_WEEK','AMOUNT_REQUIRED_IN','one_week','One Week',NULL,'1'),
('AMOUNT_REQUIRED_IN_FIFTEEN_DAYS','AMOUNT_REQUIRED_IN','fifteen_days','Fifteen Days',NULL,'2'),
('AMOUNT_REQUIRED_IN_ONE_MONTH','AMOUNT_REQUIRED_IN','one_month','One Month',NULL,'3'),

('GRANT_STATUS_NOT_STARTED','GRANT_STATUS','not_started','Not Started',NULL,'1'),
('GRANT_STATUS_PARTIAL','GRANT_STATUS','partial','Partial',NULL,'2'),
('GRANT_STATUS_COMPLETED','GRANT_STATUS','completed','Completed',NULL,'3'),
('GRANT_STATUS_SUSPENDED','GRANT_STATUS','suspended','Suspended',NULL,'4')
ON CONFLICT (value_id) DO UPDATE
SET attribute_id    = EXCLUDED.attribute_id,
    value_code      = EXCLUDED.value_code,
    value_display   = EXCLUDED.value_display,
    parent_value_id = EXCLUDED.parent_value_id,
    sort_order      = EXCLUDED.sort_order;

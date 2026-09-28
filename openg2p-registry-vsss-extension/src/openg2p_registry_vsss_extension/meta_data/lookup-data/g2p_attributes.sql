INSERT INTO "public"."g2p_attributes" ("attribute_id","attribute_code","attribute_display","is_hierarchical") VALUES
('GENDER','GENDER','Gender','FALSE'),
('FINANCIAL_MANAGEMENT','FINANCIAL_MANAGEMENT','Financial Management','FALSE'),
('TRAINING_NEEDS','TRAINING_NEEDS','Training Needs','FALSE'),
('LOAN_REQUIREMENT','LOAN_REQUIREMENT','Loan Requirement','FALSE'),
('AMOUNT_REQUIRED_IN','AMOUNT_REQUIRED_IN','Amount Required In','FALSE'),
('GRANT_STATUS','GRANT_STATUS','Grant Status','FALSE')
ON CONFLICT (attribute_id) DO UPDATE
SET attribute_code    = EXCLUDED.attribute_code,
    attribute_display = EXCLUDED.attribute_display,
    is_hierarchical   = EXCLUDED.is_hierarchical;

INSERT INTO
    "public"."g2p_intake_form_ui_tabs" ("tab_id", "form_id", "tab_label", "tab_order")
VALUES
    (
        't1',
        '7a7cbf4b-2b9f-49df-a50e-f10b1b7e6b6d',
        'household_intake_form',
        1
    ),
    (
        't2',
        'dcf019af-458c-43be-9343-16dfc38a2475',
        'individual_intake_form',
        1
    ),
    (
        'village_intake_tab',
        'a9b8c7d6-e5f4-4321-9876-543210fedcba',
        'village_intake_form',
        1
    )
ON CONFLICT (tab_id) DO NOTHING;

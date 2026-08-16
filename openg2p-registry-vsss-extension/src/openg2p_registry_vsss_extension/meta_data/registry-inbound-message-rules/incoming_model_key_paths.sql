INSERT INTO
    "public"."incoming_model_key_paths" (
        "key_path_id",
        "data_model_id",
        "key_path_for_message_id",
        "key_path_for_sender",
        "key_path_for_signature",
        "key_path_for_signature_payload",
        "is_list",
        "key_path_for_list_elements"
    )
VALUES
    (
        'nsr_v11_key_path',
        'nsr_v11_data_model',
        '$.body.header.message_id',
        '$.body.header.sender_id',
        '$.body.header.signature',
        '$.body.message',
        'False',
        '$.body.message'
    )
ON CONFLICT (data_model_id) DO UPDATE SET
    key_path_for_message_id = EXCLUDED.key_path_for_message_id,
    key_path_for_sender = EXCLUDED.key_path_for_sender,
    key_path_for_signature = EXCLUDED.key_path_for_signature,
    key_path_for_signature_payload = EXCLUDED.key_path_for_signature_payload,
    is_list = EXCLUDED.is_list,
    key_path_for_list_elements = EXCLUDED.key_path_for_list_elements;

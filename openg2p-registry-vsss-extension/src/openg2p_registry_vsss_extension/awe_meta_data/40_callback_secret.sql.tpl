-- Shared secret AWE uses to authenticate its decision callbacks back into the
-- registry. Rendered by the db-seed entrypoint with envsubst from
-- AWE_CALLBACK_* (the chart mints the HMAC secret and passes it in), so the
-- secret itself is never committed.
INSERT INTO "public"."callback_secret" (
    "id",
    "caller_service",
    "secret_hash",
    "status",
    "rotated_at",
    "created_at",
    "updated_at"
) VALUES (
    '${AWE_CALLBACK_SECRET_ID}',
    '${AWE_CALLBACK_CALLER_SERVICE}',
    '${AWE_CALLBACK_HMAC_SECRET}',
    'active',
    NOW(),
    NOW(),
    NOW()
)
ON CONFLICT ("id") DO UPDATE SET
    "caller_service" = EXCLUDED."caller_service",
    "updated_at" = NOW();

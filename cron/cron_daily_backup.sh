#!/usr/bin/env bash
# Cron job 8 — backup diário 04h
# Schedule: 0 4 * * *  (job: email-cron-8-daily-backup)

SUPABASE_URL="https://zqvqmqpdgsiyvlsewyyq.supabase.co"
SERVICE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxdnFtcXBkZ3NpeXZsc2V3eXlxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzY5NTU0OSwiZXhwIjoyMDkzMjcxNTQ5fQ.-ONTBhUfgXZ8UGta0bfJBdXgtU0moP1v485LEmMgvzE"
TIMESTAMP=2026-05-02 09:04:12

echo "[] Executando email-cron-8-daily-backup..."

curl -s -X POST "/rest/v1/table_cron"   -H "apikey: "   -H "Authorization: Bearer "   -H "Content-Type: application/json"   -H "Prefer: return=minimal"   -d '{"num": 8}' && echo " OK" || echo " ERRO"

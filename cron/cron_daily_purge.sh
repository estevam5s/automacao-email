#!/usr/bin/env bash
# Cron job 7 — purga diária 01h
# Schedule: 0 1 * * *  (job: email-cron-7-daily-purge)

SUPABASE_URL="https://zqvqmqpdgsiyvlsewyyq.supabase.co"
SERVICE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxdnFtcXBkZ3NpeXZsc2V3eXlxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzY5NTU0OSwiZXhwIjoyMDkzMjcxNTQ5fQ.-ONTBhUfgXZ8UGta0bfJBdXgtU0moP1v485LEmMgvzE"
TIMESTAMP=2026-05-02 09:04:12

echo "[] Executando email-cron-7-daily-purge..."

curl -s -X POST "/rest/v1/table_cron"   -H "apikey: "   -H "Authorization: Bearer "   -H "Content-Type: application/json"   -H "Prefer: return=minimal"   -d '{"num": 7}' && echo " OK" || echo " ERRO"

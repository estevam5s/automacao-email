#!/usr/bin/env bash
# Executa todos os cron jobs manualmente (para teste)
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================"
echo "  AUTOMAÇÃO EMAIL — EXECUTAR TODOS CRONS"
echo "========================================"

for script in \
  cron_6h_heartbeat.sh \
  cron_daily_cleanup.sh \
  cron_10min_status.sh \
  cron_hourly_sync.sh \
  cron_weekly_report.sh \
  cron_monthly_close.sh \
  cron_daily_purge.sh \
  cron_daily_backup.sh \
  cron_weekly_reindex.sh \
  cron_batch_process.sh; do
  echo ""
  echo "--- $script ---"
  bash "$DIR/$script"
done

echo ""
echo "========================================"
echo "  Concluído!"
echo "========================================"

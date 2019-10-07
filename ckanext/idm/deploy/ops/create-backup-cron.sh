#!/usr/bin/env bash

OPS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
VOLUMES_SH="$OPS_DIR/volumes.sh"
POSTGRES_SH="$OPS_DIR/postgres.sh"

mkdir -p /etc/cron.hourly
mkdir -p /etc/cron.daily
mkdir -p /etc/cron.weekly

HOURLY_SH=/etc/cron.hourly/ckan-hourly.sh
DAILY_SH=/etc/cron.daily/ckan-daily.sh
WEEKLY_SH=/etc/cron.weekly/ckan-weekly.sh

rm -f "$HOURLY_SH" "$DAILY_SH" "$WEEKLY_SH"

echo "sudo bash $VOLUMES_SH backup hourly" >> "$HOURLY_SH"
echo "sudo bash $VOLUMES_SH backup daily" >> "$DAILY_SH"
echo "sudo bash $VOLUMES_SH backup weekly" >> "$WEEKLY_SH"

echo "sudo bash $POSTGRES_SH backup weekly" >> "$WEEKLY_SH"

chown root "$HOURLY_SH" "$DAILY_SH" "$WEEKLY_SH"
sudo chmod +x "$HOURLY_SH" "$DAILY_SH" "$WEEKLY_SH"


# sudo tail -f /var/log/cron

#!/usr/bin/env bash

OPS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
VOLUMES_SH="$OPS_DIR/volumes.sh"
POSTGRES_SH="$OPS_DIR/postgres.sh"

chown root "$VOLUMES_SH"
chmod +x "$VOLUMES_SH"

chown root "$POSTGRES_SH"
chmod +x "$POSTGRES_SH"

mkdir -p /etc/cron.hourly
mkdir -p /etc/cron.daily
mkdir -p /etc/cron.weekly

HOURLY_SH=/etc/cron.hourly/ckan-hourly.sh
DAILY_SH=/etc/cron.daily/ckan-daily.sh
WEEKLY_SH=/etc/cron.weekly/ckan-weekly.sh

rm -f "$HOURLY_SH" "$DAILY_SH" "$WEEKLY_SH"

echo "#!/bin/bash" > "$HOURLY_SH"
echo "$VOLUMES_SH backup hourly" >> "$HOURLY_SH"

echo "#!/bin/bash" > "$DAILY_SH"
echo "$VOLUMES_SH backup daily" >> "$DAILY_SH"

echo "#!/bin/bash" > "$WEEKLY_SH"
echo "$VOLUMES_SH backup weekly" >> "$WEEKLY_SH"
echo "$POSTGRES_SH backup weekly" >> "$WEEKLY_SH"


chown root "$HOURLY_SH"
sudo chmod +x "$HOURLY_SH"

chown root "$DAILY_SH"
sudo chmod +x "$DAILY_SH"

chown root "$WEEKLY_SH"
sudo chmod +x "$WEEKLY_SH"


# sudo tail -f /var/log/cron

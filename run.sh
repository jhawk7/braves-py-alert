#!/bin/sh

# use crontab in linux to run this script on schedule `crontab -e` to open cron job
# in cron:
# [minute] [hours] [day of month] [month] [day of week] command
# 0 9 * * * bash /home/pi/dev/python/braves-py-alarm/run.sh > /home/pi/cron_errors.log 2>&1

echo "running braves_alarm..."
source /home/pi/dev/python/braves-py-alarm/env.sh
python3 /home/pi/dev/python/braves-py-alarm/braves_alarm.py
echo "cleaning up.."
unset EMAIL
unset PASS
unset PHONE
unset CC_EMAILS
echo "fin"
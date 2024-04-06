#!/bin/sh

echo "running braves_alarm..."
source /home/pi/dev/python/braves-py-alert/env.sh
python3 /home/pi/dev/python/braves-py-alert/braves_alert.py
echo "cleaning up.."
unset EMAIL
unset PASS
unset PHONE
unset CC_EMAILS
echo "fin"

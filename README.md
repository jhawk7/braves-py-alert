# Braves Game Alert Script ![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)

Simple script calls a public API to get daily mlb game data and sends notifications when the Atlanta Braves have a home game so that traffic can be avoided on that day ;)

Runs on daily schedule as a cron job in linux :); 

**UPDATE**: Now runs as a container on a cronjob schedule in my `k3s` (mini kubernetes runtime) cluster. For setting up more generic SMTP alert cronjobs, see **cron smtp script** and **kubernetes pod config** [here](https://github.com/jhawk7/smtp-alert-cron).

## Setup
Script uses these env vars: 
  - `EMAIL=<sender_email>`
  - `PASS=<sender_email_password>`
  - `PHONE=<receipient phone number>`
  - `CC_EMAILS=<comma seprated list of receipient emails>`
  - `MOBILE_PROVIDER=<name of your mobile provider from providers.py>`

Use `pip3 install -r requirements.txt` to setup requirements and run with python, or run with `docker-compose up`

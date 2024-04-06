# braves-py-alert

## Details
* gets daily mlb game data and sends notifications when the Atlanta Braves have a home game so that traffic can be avoided on that day ;)

* ~runs on daily schedule~ run it as a cron job in linux :); UPDATE: This now runs as a container on a cronjob schedule in k3s

* uses env vars `EMAIL=<sender_email>`, `PASS=<sender_email_password>`,`PHONE=<receipient phone number>`, `CC_EMAILS=<comma seprated list of receipient emails>`

* use `pipenv install` then `pipenv run pip freeze > requirements.txt` to setup requirements

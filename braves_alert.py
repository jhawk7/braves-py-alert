import datetime
import json
import urllib3
import os
import smtplib
from providers import PROVIDERS

http = urllib3.PoolManager()

def getGames():
    start_date = end_date = datetime.date.today().strftime("%Y-%m-%d")
    url = f'https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={start_date}&endDate={end_date}'
    #should retry 3x by default
    res = http.request('GET', url)
    if res:
        print("data retrieved!")
    body = res.data.decode("utf-8")
    if res.status != 200:
        print(f"error getting today's game data; status: {res.status}; response: {body}")
        return []
    else:
       return json.loads(body)['dates'][0]['games'] 


def sendMessage(recipients, message):
    print("sending message")
    sender_email = str(os.getenv('EMAIL'))
    email_password = str(os.getenv('PASS'))
    auth = (sender_email, email_password)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(auth[0], auth[1])
    server.sendmail(auth[0], recipients, message)
   

def main():
    games = getGames()
    gametime = None
    
    for game in games:
        if game['venue']['name'] == "Truist Park":
            gametime = game['gameDate']
            break
    
    if not gametime:
        print("no game today")
        return
    
    number = os.getenv('PHONE')
    cc = str(os.getenv('CC_EMAILS')).split(",")
    provider_name = str(os.getenv("MOBILE_PROVIDER"))
    parsed_gametime = gametime.replace('T',' ').replace('Z','')
    utc_gametime = datetime.datetime.strptime(parsed_gametime, "%Y-%m-%d %H:%M:%S")
    edt_gametime = utc_gametime - datetime.timedelta(hours=4)
    try:
        #try sms text with emails
        recipients = [f'{number}@{PROVIDERS.get(provider_name).get("sms")}'] + cc
        message = f'Subject: Warning! Braves Home Game Today\n\nGameTime @ {edt_gametime} EDT -__-'
        sendMessage(recipients, message)
    except Exception as e:
        #fallback to just emails
        print(f"message failed; falling back; {e}")
        cc = str(os.getenv('CC_EMAILS')).split(",")
        recipients = cc
        message = f'Subject: Warning! Braves Home Game Today\n\nGametime @ {edt_gametime} EDT -__-\n\n' + \
        f'Email was sent as fallback due to the error below:\nFailed to send sms; error: {e}'
        sendMessage(recipients, message)


if __name__ == '__main__':
    main()

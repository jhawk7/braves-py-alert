import datetime
import json
import urllib3
import os
import smtplib
import schedule, time
from providers import PROVIDERS

http = urllib3.PoolManager()

def getGames():
    url = 'http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1'
    
    #should retry 3x by default
    res = http.request('GET', url)
    body = res.data.decode("utf-8")
    if res.status != 200:
        print(f"error getting today's game data; status: {res.status}; response: {body}")
        return []
    else:
       return json.loads(body)['dates'][0]['games'] 


def sendMessage(recipients, message):
    sender_email = os.getenv('EMAIL')
    email_password = os.getenv('PASS')
    auth = (sender_email, email_password)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
    server.sendmail(auth[0], recipients, message)


def main():
    games = getGames()
    gametime = None
    
    for game in games:
        if game['venue']['name'] == "Truist Park":
            gametime = game['gameDate']
            break
    
    if gametime:
        number = os.getenv('PHONE')
        parsed_gametime = gametime.replace('T',' ').replace('Z','')
        utc_gametime = datetime.datetime.strptime(parsed_gametime, "%Y-%m-%d %H:%M:%S")
        edt_gametime = utc_gametime - datetime.timedelta(hours=4)
        try:
            #try sms text with emails
            cc = str(os.getenv('CC_EMAILS')).split(",")
            recipients = [f'{number}@{PROVIDERS.get("Google Project Fi").get("sms")}'] + cc
            message = f'Subject: Warning! Braves Home Game Today\n\nGameTime @ {edt_gametime} EDT -__-'
            sendMessage(recipients, message)
        except Exception as e:
            #fallback to just emails
            cc = str(os.getenv('CC_EMAILS')).split(",")
            recipients = cc
            message = f'Subject: Warning! Braves Home Game Today\n\nGametime @ {edt_gametime} EDT -__-\n\n' + \
            f'Email was sent as fallback due to the error below:\nFailed to send sms; error: {e}'
            sendMessage(recipients, message)

#uses local time
schedule.every().day.at("14:00").do(main)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(60) #sleep in secs

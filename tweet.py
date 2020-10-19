from os import environ
from datetime import datetime, timedelta
import gspread
import tweepy
import time
from dotenv import load_dotenv
import logging
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACESS_SECRET)

api = tweepy.API(auth)

gc = gspread.service_account(filename='gsheet_credentials.json')

sh = gc.open_by_key('1NndC9dgkx18RGh6XuS-NHO2jUmJe3yo0Zi1bHrOfPtI')
worksheet = sh.sheet1
INTERVAL = int(environ['INTERVAL'])

def main():
    while True:
        tweet_records = worksheet.get_all_records()
        current_time = datetime.utcnow() - timedelta(hours=4)
        logger.info(
            f'{len(tweet_records)} tweets found at {current_time.time()}')
        for idx, tweet in enumerate(tweet_records, start=2):
            msg = tweet['message']
            time_str = tweet['time']
            done = tweet['done']
            date_time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            if not done:
                now_time_edt = datetime.utcnow() + timedelta(hours=4)
                if date_time_obj < now_time_edt:
                    logger.info('this should be tweeted')
                    try:
                        # if not DEBUG
                        api.update_status(msg)
                        worksheet.update_cell(idx, 3, 1)
                    except Exception as e:
                        logger.warning(f'exception during tweet! {e}')
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()

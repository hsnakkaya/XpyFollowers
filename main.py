import csv
import tweepy
import pandas
from twitter_credentials import *


def processing_loop(start_id, end_id):

    # initialize twitter API

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=30)

    # get twitter handles from excel fle as pandas data frame

    excel_list = pandas.read_excel('list.xlsx', sheet_name='Sheet1')

    # iterate through all the handles

    for index, row in excel_list.iterrows():

        entry_id = row["id"]

        if index == 0:
            continue
        if entry_id < start_id:
            continue
        if entry_id > end_id:
            continue

        # store the @handle and filename for that id

        handle = row["twitter_handle"]
        file_name = 'follower_ids/' + str(entry_id) + '.csv'

        # open new csv

        with open(file_name, mode='w', encoding='utf-8', newline='') as file:

            # scrape followers

            users = tweepy.Cursor(api.followers_ids, screen_name=handle, count=5000).items()

            csv_writer = csv.writer(file)

            while True:
                try:
                    user = next(users)
                except tweepy.TweepError:
                    print("tweepError")
                    user = next(users)
                except StopIteration:
                    print("stopped iteration")
                    file.close()
                    break
                csv_writer.writerow([user])
                print(user)
                file.flush()


processing_loop(8, 9)













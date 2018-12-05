import csv
import pandas
import tweepy
import datetime
from twitter_credentials import *


# Create edges.csv for Gephi from followers_ids

def edges_process(id_var):  # Iterate through all files and find edges, id_var = id number to iterate up to

    report = open('reports/edges_report.txt', 'a+')
    report.write(str(datetime.datetime.now()) + '   -   edges_process started\n')
    count = 0

    # open new csv file

    with open('output/edges.csv', mode='w', encoding='utf-8', newline='') as file:

        # create and write the headers needed for Gephi

        fieldnames = ['Source', 'Target', 'Weight']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()

        csv_writer = csv.writer(file)

        # iterate through all files and find common followers

        for x in range(id_var):

            with open('followers_ids/' + str(x+1) + '.csv', 'r') as f:
                a = set([row[0] for row in csv.reader(f)])
                f.close()

            for y in range(id_var-1):

                if y+2 <= x+1:
                    continue
                with open('followers_ids/' + str(y+2) + '.csv', 'r') as f:
                    b = set([row[0] for row in csv.reader(f)])
                    f.close()

                # Write data to the file

                source = x+1
                target = y+2
                weight = len(a.intersection(b))
                row_to_write = [source, target, weight]
                csv_writer.writerow(row_to_write)
                count = count + 1

        file.close()
    report.write(str(datetime.datetime.now()) + '       ' + str(count) + '    edges found\n')
    report.close()


# Create nodes.csv for Gephi from followers_ids and file_name.xlsx

def nodes_process(id_var, file_name):  # id_var = id number to iterate up to

    report = open('reports/nodes_report.txt', 'a+')
    report.write(str(datetime.datetime.now()) + '   -   nodes_process started\n')
    count = 0

    excel_list = pandas.read_excel(file_name + '.xlsx', sheet_name='Sheet1')

    with open('output/nodes.csv', mode='w', encoding='utf-8', newline='') as file:

        fieldnames = ['Id', 'Label', 'Weight', 'Category', 'Subcategory', 'Twitter_handle', 'Verified']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()

        csv_writer = csv.writer(file)

        for x in range(id_var):

            with open('followers_ids/' + str(x+1) + '.csv', 'r') as f:
                a = set([row[0] for row in csv.reader(f)])

                label = excel_list.loc[x, 'name']
                weight = len(a)
                category = excel_list.loc[x, 'category']
                subcategory = excel_list.loc[x, 'subcategory']
                handle = '@' + excel_list.loc[x, 'twitter_handle']
                verified = excel_list.loc[x, 'verified']

                row_to_write = [x+1, label, weight, category, subcategory, handle, verified]
                count = count + 1
                csv_writer.writerow(row_to_write)
                f.close()
        file.close()
    report.write(str(datetime.datetime.now()) + '       ' + str(count) + '    nodes found\n')
    report.close()


# Scrape all followers from @handles in file_name.xlsx

def scraper(start_id, end_id, file_name):

    total_count = 0

    report = open('reports/scraper_report.txt', 'a+')
    report.write(str(datetime.datetime.now()) + '   -   scraper started\n')
    report.write('\n    start_id: ' + str(start_id) + '    end_id: ' + str(end_id) + '\n\n')

    # initialize twitter API

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=30)

    # get twitter handles from excel fle as pandas data frame

    excel_list = pandas.read_excel(file_name + '.xlsx', sheet_name='Sheet1')

    # iterate through all the handles

    for index, row in excel_list.iterrows():

        entry_id = row["id"]

        if entry_id < start_id:
            continue
        if entry_id > end_id:
            continue

        # store the @handle and filename for that id

        handle = row["twitter_handle"]
        file_name = 'followers_ids/' + str(entry_id) + '.csv'

        # open new csv

        with open(file_name, mode='w', encoding='utf-8', newline='') as file:

            report.write(str(datetime.datetime.now()) +
                         '   -   creating ' +
                         str(entry_id) + '.csv\n')
            print('-   creating ', str(entry_id), '.csv\n')

            count = 0

            # scrape followers

            users = tweepy.Cursor(api.followers_ids, screen_name=handle, count=5000).items()

            csv_writer = csv.writer(file)

            while True:
                try:
                    user = next(users)
                except tweepy.TweepError:
                    print("tweepError")
                    report.write(str(datetime.datetime.now()) + '   -   tweepy Error\n')
                    user = next(users)
                except StopIteration:
                    print("stopped iteration")
                    file.close()
                    report.write(str(datetime.datetime.now()) +
                                 '   -   closing ' + str(entry_id) + '.csv' +
                                 ' with ' + str(count) + ' entries\n')
                    break
                csv_writer.writerow([user])
                print(count, ' user ids scraped from @', str(handle))
                count = count + 1
                total_count = total_count + 1
                file.flush()

    report.write(str(datetime.datetime.now()) + '   -   Scraping Done\n\n')
    report.write('    ' + str(end_id-start_id+1) + ' accounts     ' + str(total_count) + ' entries\n')
    report.close()







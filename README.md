# XpyFollowers
Twitter follower user_id scraper for Gephi

-Grabs Twitter handles from an excel file
-Scrapes user_ids from all those handles and stores in seperate csv files
-Compares those csv files with each other and finds shared follower counts
-Exports nodes.csv and edges.csv files for Gephi (https://gephi.org/)

instructions:

-get you API tokens/keys from https://apps.twitter.com/
-put them in twitter_credentials.py

-fill up your excel table with twitter handles you want to scrape (maintaining formatting)

-use scraper(start_id, end_id, 'twitter_list')

function to scrape that list from twitter

-start_id = the id # you want to begin scraping with    
-end_id = the id # you want to end scraping with    
-twitter_list = name of the xlsx file you want to use, see the example file for formatting

when done with scraping, use;

edges_process(id) and nodes_process(id, 'twitter_list')

functions to cross reference all the profiles and find shared followers and create the nodes.csv and edges.csv files for Gephi 

-id = how many ids you want to check for shared followers
-twitter_list = name of the xlsx file you used before
    

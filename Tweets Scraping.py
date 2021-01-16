import pandas as pd
import numpy as np
from _datetime import datetime
import tweepy
import re
from Credentials import consumer_key, consumer_secret, access_token, access_token_secret
from Dictionaries import politicians_dct, journalists_dct, media_dct, parties_dct
from Functions import tweets_df, df_punct, df_sentiment, df_organizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from google_trans_new import google_translator
import nltk
# nltk.download('vader_lexicon')

# Setting start and end date, to scrape tweets in between. Also, setting week number for data export and import
# datetime function format is: Year, Month, Day, Hour, Minutes, Seconds, Timezone
startDate = datetime(2021, 1, 8)
endDate = datetime(2021, 1, 15)
printDate = str(datetime.now().day) + '-' + str(datetime.now().month) + '-' + str(datetime.now().year)
week = '3'


# Create four dataframes, for the four types of twitter figures - Politicians, Journalists, Media and Parties
Politicians = tweets_df(politicians_dct, startDate, endDate)
Journalists = tweets_df(journalists_dct, startDate, endDate)
Media = tweets_df(media_dct, startDate, endDate)
Parties = tweets_df(parties_dct, startDate, endDate)

# Add job column to all dataframes
Politicians.insert(1, 'job', 'Politician')
Journalists.insert(1, 'job', 'Journalist')
Media.insert(1, 'job', 'Media')
Parties.insert(1, 'job', 'Party')

# Concatenate the dataframes to the Political System (PS) dataframe
PS_raw = pd.concat([Politicians, Journalists, Media, Parties]).reset_index(drop=True)

# Export the raw dataframe to the Weekly Raw folder
PS_raw.to_csv(r'Data\Raw\Weekly\Raw ' + printDate + '.csv', index=False)

# Appending by dfs concatenation the data to the csv file containing data from all dates
# Importing the full dataframe
Raw = pd.read_csv(r'Data\Raw\Raw.csv')

# Verifying the currently scraped dataframe is in the same column order as the final data one
PS_raw = PS_raw[Raw.columns]

# Concatenating and saving
Raw = pd.concat([Raw, PS_raw])
Raw.to_csv(r'Data\Raw\Raw.csv', index=False)

PS_raw = pd.read_csv(r'Data/Raw/Weekly/Raw 8-1-2021.csv')
# Delete punctuation
PS_raw = df_punct(PS_raw)

# Compute sentiment and export
PS_sentiment = df_sentiment(PS_raw)

# Export the sentiment dataframe
PS_sentiment.to_csv(r'Data\Sentiment\Weekly\Sentiment ' + printDate + '.csv', index=False)

# Appending by dfs concatenation the data to the csv file containing data from all dates
# Importing the full dataframe
Sentiment = pd.read_csv(r'Data\Sentiment\Sentiment.csv')

# Verifying the currently scraped dataframe is in the same column order as the final data one
PS_sentiment = PS_sentiment[Sentiment.columns]

# Concatenating and saving
Sentiment = pd.concat([Sentiment, PS_sentiment])
Sentiment.to_csv(r'Data\Sentiment\Sentiment.csv', index=False)

# Organize the dataframe to final analysis and visualization
PS = df_organizer(PS_sentiment)

# Export dataframe
PS.to_csv(r'Data\Organized\Weekly\Organized ' + printDate + '.csv', index=False)

# Appending by dfs concatenation the data to the csv file containing data from all dates
# Importing the full dataframe
Organized = pd.read_csv(r'Data\Organized\Organized.csv')

# Verifying the currently scraped dataframe is in the same column order as the final data one
PS = PS[Organized.columns]

# Concatenating and saving
Organized = pd.concat([Organized, PS])
Organized.to_csv(r'Data\Organized\Organized.csv', index=False)


##########################################              SKETCH          #############################################
# last_week = pd.read_csv(r'Data\Raw\Weekly\Raw 25-12-2020.csv')
# this_week = pd.read_csv(r'Data\Raw\Weekly\Raw 1-1-2021.csv')
#
# PS = pd.concat([last_week, this_week])
#
# PS = df_organizer(df_punct(PS))
#
# PS_raw = pd.read_csv(r'Data\Raw\Weekly\Raw 1-1-2021.csv')

# politicians_dct.update(journalists_dct)
#
# PS = pd.read_csv(r'Data/Sentiment/Sentiment.csv')
#
# PS['name'][(PS['name'] == 'Shemesh')] = 'Shemesh_Lital'
#
# key_lst = PS['name'].unique().tolist()
# val_lst = []
#
# for name in key_lst:
#     user = api.get_user(politicians_dct[name][0])
#     fol = user.followers_count
#     val_lst.append(fol)
#
# fol_dct = dict(zip(key_lst, val_lst))
#
# PS['followers_count'] = PS['name'].map(fol_dct)
#
# PS.to_csv(r'Data/Sentiment/Sentiment.csv', index=False)

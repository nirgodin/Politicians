import pandas as pd
import numpy as np
from _datetime import datetime, timedelta
import tweepy
import re
from Credentials import consumer_key, consumer_secret, access_token, access_token_secret
from Dictionaries import politicians_dct, journalists_dct, media_dct, parties_dct, seats_dct
from Functions import tweets_df, df_punct, df_sentiment, df_organizer, to_datetime
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

PS_raw = pd.read_csv(r'Data/Raw/Weekly/Raw 15-1-2021.csv')
# Delete punctuation
PS_raw = df_punct(PS_raw)

# Compute sentiment and export
PS_sentiment1 = df_sentiment(PS_raw.head(5000))
PS_sentiment2 = df_sentiment(PS_raw.iloc[5000:10000])
PS_sentiment3 = df_sentiment(PS_raw.iloc[10000:15000])
PS_sentiment4 = df_sentiment(PS_raw.iloc[15000:len(PS_raw)])

PS_sentiment = pd.concat([PS_sentiment1,
                          PS_sentiment2,
                          PS_sentiment3,
                          PS_sentiment4])

# Export the sentiment dataframe
PS_sentiment.to_csv(r'Data\Sentiment\Weekly\Sentiment ' + printDate + '.csv', index=False)
# PS_sentiment.to_csv(r'Data\Sentiment\Weekly\Sentiment ' + '8-1-2021' + '.csv', index=False)

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

# key_lst = PS['name'].unique().tolist()
# created_lst = []
#
# # politicians_dct.update(parties_dct)
#
# # Creating the followers lst by iterating through the key lst and returning for each unique name its followers num
# for name in key_lst:
#     userpage = api.get_user(politicians_dct[name][0])
#     created = userpage.created_at
#     created_lst.append(created)
#
# # Zipping the two lists in two one dictionary
# created_dct = dict(zip(key_lst, created_lst))
#
# # Create the followers count column by mapping the name column with the followers dct
# PS['join_date'] = PS['name'].map(created_dct)
#
# PS.to_csv(r'Data/Raw/Raw.csv', index=False)
#
# # PS = PS.drop(columns='ranking')
#
# # RANK
#
# key_lst = PS['name'].unique().tolist()
# val_lst = []
#
# for name in key_lst:
#     try:
#         rank = politicians_dct[name][4]
#     except KeyError:
#         rank = np.nan
#     val_lst.append(rank)
#
# rank_dct = dict(zip(key_lst, val_lst))
#
# PS['ranking'] = PS['name'].map(rank_dct)
#
# abou = datetime.strptime('19/6/1976', '%d/%m/%Y')
# ab = datetime.now() - abou
#
# round(ab.days/365, 0)


# PS = pd.read_csv(r'Data/Sentiment/Weekly/Sentiment 8-1-2021.csv')


# AGE

# dob_lst = []
#
# for name in key_lst:
#     try:
#         dob = datetime.strptime(politicians_dct[name][5], '%d/%m/%Y')
#     except (KeyError, IndexError) as e:
#         dob = np.nan
#     dob_lst.append(dob)
#
# dob_dct = dict(zip(key_lst, dob_lst))
#
# PS['created_at'] = to_datetime(PS['created_at'])
# PS['dob'] = PS['name'].map(dob_dct)
# PS['age'] = PS['created_at'] - PS['dob']
# PS['age'] = PS['age'].apply(lambda x: round((x.days)/365, 0))




# POLITICAL POWER

# from Dictionaries import seats_dct
# # import shap
#
# power_lst = []
# for name in politicians_dct.keys():
#     try:
#         party = politicians_dct[name][1]
#         seats = seats_dct[party]
#         rank = politicians_dct[name][4]
#         power = seats/rank
#     except KeyError:
#         power = np.nan
#     power_lst.append(power)
#
# power_dct = dict(zip(politicians_dct.keys(), power_lst))
#
# PS['power'] = PS['name'].map(power_dct)
#
# PS.to_csv(r'Data/Regression/Regression.csv', index=False)




# Prime minister column
#
# PS['pm'] = [1 if name == 'Netanyahu' else 0 for name in PS['name']]
#
#
#
# # Minister column
# PS['minister'] = [1 if name in minister_lst else 0 for name in PS['name']]

import pandas as pd
import numpy as np
import time
from _datetime import datetime
import _json
import tweepy
import re
from Credentials import consumer_key, consumer_secret, access_token, access_token_secret
from Dictionaries import politicians_dct, journalists_dct, media_dct
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from google_trans_new import google_translator
import nltk
# nltk.download('vader_lexicon')

# Setting start and end date, to scrape tweets in between
# datetime function format is: Year, Month, Day, Hour, Minutes, Seconds, Timezone
startDate = datetime(2020, 12, 8, 00, 00, 00) # tzinfo=timezone('Israel')
endDate = datetime(2020, 12, 15, 00, 00, 00) # tzinfo=timezone('Israel')

# Setting the necessary twitter developer credentials to use the tweepy package and scrape tweets
# These are set as environment variables
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Set Google Translator
translator = google_translator()

# Set Vader's SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# Create a dataframe in which the tweets will be stored

# Iterate through the politicians twitter users and scrape each user tweets
# Code credit to Alexander Psiuk at https://gist.github.com/alexdeloy
# and Martin Beck at https://towardsdatascience.com/how-to-scrape-tweets-from-twitter-59287e20f0f1
def tweets_df(dct):
    Tweets = pd.DataFrame()
    for user in dct.keys():
        username = dct[user][0]
        try:
            tweets = []
            tmpTweets = api.user_timeline(username)
            for tweet in tmpTweets:
                if startDate < tweet.created_at < endDate:
                    tweets.append(tweet)
            while tmpTweets[-1].created_at > startDate:
                print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")
                tmpTweets = api.user_timeline(username, max_id=tmpTweets[-1].id)
                for tweet in tmpTweets:
                    if startDate < tweet.created_at < endDate:
                        tweets.append(tweet)

            # Pulling information from tweets iterable object
            tweets_list = [[user,
                            dct[user][1],
                            dct[user][2],
                            tweet.created_at,
                            tweet.id,
                            # tweet._json['quote_count'],
                            # tweet._json['reply_count'],
                            tweet._json['retweet_count'],
                            tweet._json['favorite_count'],
                            # tweet._json['in_reply_to_screen_name'],
                            # tweet._json['is_quote_status'],
                            # tweet._json['quoted_status'],
                            tweet.text] for tweet in tweets]

            # Creation of dataframe from tweets list
            # Add or remove columns as you remove tweet information
            tweets_df = pd.DataFrame(tweets_list)
            Tweets = pd.concat([Tweets, tweets_df])

        except BaseException as e:
            print('failed on_status,', str(e))
            time.sleep(3)

    # Change Tweets df column names
    Tweets = Tweets.rename(columns={0: 'name',
                                    1: 'organization',
                                    2: 'gender',
                                    3: 'created_at',
                                    4: 'id',
                                    5: 'retweet_count',
                                    6: 'favorite_count',
                                    7: 'text'})
    
    return Tweets


Politicians_raw = tweets_df(politicians_dct)
Journalists_raw = tweets_df(journalists_dct)
Media_raw = tweets_df(media_dct)


# Export the raw dataframes to the Raw folder
# printDate = str(endDate).split()[0].replace('2020-', '')
# Politicians.to_csv(r'Data\Raw\Politicians\Politicians_' + printDate + '.csv')
# Journalists.to_csv(r'Data\Raw\Journalists\Journalists_' + printDate + '.csv')


# Dataframe organizer function
def df_organizer(df):  
    # Reset index
    df = df.reset_index(drop=True)

    # Delete all urls from the strings, which are almost solely used to retweet, and 'rt' which indicates a Retweet
    try:
        df['text'] = [re.sub(r'http\S+', "", txt) for txt in df['text']]
        df['text'] = [re.sub(r'rt', "", txt) for txt in df['text']]
    except TypeError:
        pass

    # Compute Sentiment, using vader and google translate
    # df['sentiment_dct'] = [sid.polarity_scores(translator.translate(txt)) for txt in df['text']]
    # df['negative'] = [df['sentiment_dct'][i]['neg'] for i in df.index.tolist()]
    # df['neutral'] = [df['sentiment_dct'][i]['neu'] for i in df.index.tolist()]
    # df['positive'] = [df['sentiment_dct'][i]['pos'] for i in df.index.tolist()]
    # df['compound'] = [df['sentiment_dct'][i]['compound'] for i in df.index.tolist()]
    # df = df.drop(columns='sentiment_dct')

    # Delete punctuation
    df['text'] = [re.sub(r'[^\w\s]', '', str(txt).lower().strip()) for txt in df['text']]

    # Insert word and character count columns
    df['word_count'] = df['text'].apply(lambda x: len(str(x).split(" ")))
    df['char_count'] = df['text'].apply(lambda x: sum(len(word) for word in str(x).split(" ")))

    # Group by name, and return the concatenated text, the sum of the word and the char count, and the number of tweets
    df = df.groupby(['name'], as_index=False).agg({'organization': ['first'],
                                                   'gender': ['first', 'size'],
                                                   'retweet_count': ['sum', 'mean'],
                                                   'favorite_count': ['sum', 'mean'],
                                                   'word_count': ['sum', 'mean'],
                                                   'char_count': ['sum', 'mean'],
                                                   'text': [' '.join]})
                                                   # 'negative': ['mean'],
                                                   # 'neutral': ['mean'],
                                                   # 'positive': ['mean'],
                                                   # 'compound': ['mean']

    # Replace column names
    df.columns = list(map(''.join, df.columns.values))
    df = df.rename(columns={'organizationfirst': 'organization',
                            'genderfirst': 'gender',
                            'gendersize': 'tweet_count',
                            'retweet_countsum': 'retweet_count',
                            'retweet_countmean': 'avg_retweet_count',
                            'favorite_countsum': 'favorite_count',
                            'favorite_countmean': 'avg_favorite_count',
                            'word_countsum': 'word_count',
                            'word_countmean': 'avg_word_count',
                            'char_countsum': 'char_count',
                            'char_countmean': 'avg_char_count',
                            'textjoin': 'text'})
                            # 'negativemean': 'negative',
                            # 'neutralmean': 'neutral',
                            # 'positivemean': 'positive',
                            # 'compoundmean': 'compound'

    # Compute traffic and average traffic count
    df['traffic_count'] = df['retweet_count'] + df['favorite_count']
    df['avg_traffic_count'] = df['traffic_count'] / df['tweet_count']

    return df

# Organize the Politicians and Journalists dataframes
Politicians = df_organizer(Politicians_raw)
Journalists = df_organizer(Journalists_raw)

# Translate each row in the dataframe, analyze it's sentiment, and assign this to the sentiment column


# Add job column to both dataframes
Politicians.insert(1, 'job', 'Politician')
Journalists.insert(1, 'job', 'Journalist')

# Concatenate both dataframes to the Political System (PS) dataframe
PS = pd.concat([Politicians, Journalists]).reset_index(drop=True)

from Code.Credentials import consumer_key, consumer_secret, access_token, access_token_secret

################################################        FUNCTIONS        ################################################


# Iterate through the politicians twitter users and scrape each user tweets
# Code credit to Alexander Psiuk at https://gist.github.com/alexdeloy
# and Martin Beck at https://towardsdatascience.com/how-to-scrape-tweets-from-twitter-59287e20f0f1
def tweets_df(dct, startDate, endDate):

    # Necessary libraries
    import pandas as pd
    import numpy as np
    import time
    import tweepy

    # Setting the necessary twitter developer credentials to use the tweepy package and scrape tweets
    # These are set as environment variables
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

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
                            dct[user][3],
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
                                    3: 'hebrew_name',
                                    4: 'created_at',
                                    5: 'id',
                                    6: 'retweet_count',
                                    7: 'favorite_count',
                                    8: 'text'})

    # Append followers count column

    # Create two dictionaries with name column as keys: one - with the number of followers as values ;
    # two - with the twitter account join date as values
    key_lst = Tweets['name'].unique().tolist()
    fol_lst = []
    created_lst = []

    # Creating the followers lst join date of each user
    # This is done by iterating through the key lst and returning for each unique name its followers num
    # The try-except clause is used in case one of the users deleted his user from twitter
    for name in key_lst:
        try:
            userpage = api.get_user(dct[name][0])
            fol = userpage.followers_count
            created = userpage.created_at
        except tweepy.error.TweepError:
            fol = np.nan
            created = np.nan
        fol_lst.append(fol)
        created_lst.append(created)

    # Zipping the lists into dictionaries
    fol_dct = dict(zip(key_lst, fol_lst))
    created_dct = dict(zip(key_lst, created_lst))

    # Adding the columns to the Tweets df by mapping the name column with the dcts
    Tweets['followers_count'] = Tweets['name'].map(fol_dct)
    Tweets['join_date'] = Tweets['name'].map(created_dct)

    return Tweets


# Punctuation delete function
def df_punct(df):

    # Import necessary libraries
    import re
    import demoji
    demoji.download_codes()

    # Reset index
    df = df.reset_index(drop=True)

    # Delete all urls from the strings, which are almost solely used to retweet
    df['text'] = [re.sub(r'http\S+', "", txt) for txt in df['text']]

    # Locate retweets and assign a dummy variable to them
    df['rt'] = [1 if 'RT @' in txt else 0 for txt in df['text']]

    # Replace all emojis with word representations
    big_str = ' '.join(df['text'])
    emj_dct = demoji.findall(big_str)
    for emoji in emj_dct:
        df['text'] = df['text'].str.replace(emoji, emj_dct[emoji])

    # Delete from the text strings 'rt' which indicates a Retweet
    df['text'] = [re.sub(r'rt', "", txt) for txt in df['text']]

    # Delete punctuation
    df['text'] = [re.sub(r'[^\w\s]', '', str(txt).lower().strip()) for txt in df['text']]

    return df


# Sentiment function
def df_sentiment(df):

    # Import necessary libraries
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    from google_trans_new import google_translator
    import time
    import numpy as np
    from json.decoder import JSONDecodeError

    # Set Google Translator
    translator = google_translator()

    # Set Vader's SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()

    # Reset index
    df = df.reset_index(drop=True)

    # Compute Sentiment, using vader and google translate

    # Initializing an empty sentiment list to which the sentiment dct for each tweet will be appended
    sentiment_lst = []

    # Filling the column with the sentiment dictionaries
    # This is done with sleeps between each iteration to avoid the 429: Too Many Requests error
    for i in range(0, len(df)):
        en_text = translator.translate(df['text'][i])
        sentiment_lst.append(sid.polarity_scores(en_text))

        if i % 25 == 0:
            time.sleep(2)
        else:
            time.sleep(0.7)

    # Pass the final sentiment lst to a sentiment dct column
    df['sentiment_dct'] = sentiment_lst

    # Creating new columns for each dictionary key and dropping the dictionary itself
    df['negative'] = [df['sentiment_dct'][i]['neg'] for i in df.index.tolist()]
    df['neutral'] = [df['sentiment_dct'][i]['neu'] for i in df.index.tolist()]
    df['positive'] = [df['sentiment_dct'][i]['pos'] for i in df.index.tolist()]
    df['compound'] = [df['sentiment_dct'][i]['compound'] for i in df.index.tolist()]
    df = df.drop(columns='sentiment_dct')

    return df


# Dataframe organizer function
# sentiment argument indicates whether you insert a df with sentiment columns or not
def df_organizer(df, sentiment='on'):

    # Import necessary libraries
    from bidi.algorithm import get_display
    import pandas as pd

    # Insert word and character count columns
    df['word_count'] = df['text'].apply(lambda x: len(str(x).split(" ")))
    df['char_count'] = df['text'].apply(lambda x: sum(len(word) for word in str(x).split(" ")))

    # Drop rows with null text
    # df = df[df['text'] != '']

    # Group by name, and return the concatenated text, the sum of the word and the char count, and the number of tweets
    if sentiment == 'on':
        df = df.groupby(['name'], as_index=False).agg({'job': ['first'],
                                                       'organization': ['first'],
                                                       'gender': ['first', 'size'],
                                                       'hebrew_name': ['first'],
                                                       'followers_count': ['max'],
                                                       'retweet_count': ['sum', 'mean'],
                                                       'favorite_count': ['sum', 'mean'],
                                                       'word_count': ['sum', 'mean'],
                                                       'char_count': ['sum', 'mean'],
                                                       'negative': ['mean'],
                                                       'neutral': ['mean'],
                                                       'positive': ['mean'],
                                                       'compound': ['mean']}) #,
                                                       # 'text': [' '.join]

        # Replace column names
        df.columns = list(map(''.join, df.columns.values))
        df = df.rename(columns={'jobfirst': 'job',
                                'organizationfirst': 'organization',
                                'genderfirst': 'gender',
                                'gendersize': 'tweet_count',
                                'hebrew_namefirst': 'hebrew_name',
                                'followers_countfirst': 'followers_count',
                                'retweet_countsum': 'retweet_count',
                                'retweet_countmean': 'avg_retweet_count',
                                'favorite_countsum': 'favorite_count',
                                'favorite_countmean': 'avg_favorite_count',
                                'word_countsum': 'word_count',
                                'word_countmean': 'avg_word_count',
                                'char_countsum': 'char_count',
                                'char_countmean': 'avg_char_count',
                                'negativemean': 'negative',
                                'neutralmean': 'neutral',
                                'positivemean': 'positive',
                                'compoundmean': 'compound'}) #,
                                # 'textjoin': 'text'
    else:
        df = df.groupby(['name'], as_index=False).agg({'job': ['first'],
                                                       'organization': ['first'],
                                                       'gender': ['first', 'size'],
                                                       'hebrew_name': ['first'],
                                                       'followers_count': ['first'],
                                                       'retweet_count': ['sum', 'mean'],
                                                       'favorite_count': ['sum', 'mean'],
                                                       'word_count': ['sum', 'mean'],
                                                       'char_count': ['sum', 'mean'],
                                                       'text': [' '.join]})

        # Replace column names
        df.columns = list(map(''.join, df.columns.values))
        df = df.rename(columns={'jobfirst': 'job',
                                'organizationfirst': 'organization',
                                'genderfirst': 'gender',
                                'gendersize': 'tweet_count',
                                'hebrew_namefirst': 'hebrew_name',
                                'followers_countfirst': 'followers_count',
                                'retweet_countsum': 'retweet_count',
                                'retweet_countmean': 'avg_retweet_count',
                                'favorite_countsum': 'favorite_count',
                                'favorite_countmean': 'avg_favorite_count',
                                'word_countsum': 'word_count',
                                'word_countmean': 'avg_word_count',
                                'char_countsum': 'char_count',
                                'char_countmean': 'avg_char_count',
                                'textjoin': 'text'})

    # Compute traffic and average traffic count
    df['traffic_count'] = df['retweet_count'] + df['favorite_count']
    df['avg_traffic_count'] = df['traffic_count'] / df['tweet_count']

    # Apply the get_display function on all the hebew names in the dataframe
    df['hebrew_name'] = [get_display(df['hebrew_name'][i]) for i in df.index.tolist()]

    return df


# Defining few functions that will be relevant for the visualizations
# First function takes a sorted dataframe and returns only the head and the tail of it, with the specified num. of rows


def head_and_tail(df, nrow=20):
    df = df.head(nrow).append(df.tail(nrow))
    return df


# Second function takes a str and returns a dataframe with all the unique words in the string
# and the times each word appeared in it


def word_count(str):

    # Import relevant libraries
    import pandas as pd

    counts = dict()
    words = str.split()

    # Count the words in the string
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    # pass the word count to a sorted dataframe
    df = pd.DataFrame({'word': list(counts.keys()),
                       'count': list(counts.values())})
    df = df.sort_values(by='count', ascending=False).reset_index(drop=True)

    return df


def to_datetime(pd_series):


    # Import datetime package
    from datetime import datetime

    # Create empty list to append values to
    date_lst = []

    # Iterate through the pandas series and return the date as a datetime object no matter is original format
    for date in pd_series:
        try:
            d = datetime.strptime(date, '%d/%m/%Y %H:%M')
        except ValueError:
            pass
            try:
                d = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
            except ValueError:
                pass
                try:
                    d = datetime.strptime(date, '%d-%m-%Y %H:%M')
                except ValueError:
                    pass
                    try:
                        d = datetime.strptime(date, '%d-%m-%Y %H:%M:%S')
                    except ValueError:
                        d = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    # Append the datetime object to the list
        date_lst.append(d)

    # Return list of datetimes
    return date_lst

import pandas as pd
import numpy as np
import time
from _datetime import datetime
import _json
import tweepy
import re
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import seaborn as sns
from bidi.algorithm import get_display
from Credentials import consumer_key, consumer_secret, access_token, access_token_secret
from Dictionaries import politicians_dct, journalists_dct, media_dct
from Stopwords import stopwords_lst
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from google_trans_new import google_translator
# nltk.download('vader_lexicon')

# Setting start and end date, to scrape tweets in between
# datetime function format is: Year, Month, Day, Hour, Minutes, Seconds, Timezone
startDate = datetime(2020, 12, 11, 00, 00, 00) # tzinfo=timezone('Israel')
endDate = datetime(2020, 12, 12, 00, 00, 00) # tzinfo=timezone('Israel')

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
    df['sentiment_dct'] = [sid.polarity_scores(translator.translate(txt)) for txt in df['text']]
    df['negative'] = [df['sentiment_dct'][i]['neg'] for i in df.index.tolist()]
    df['neutral'] = [df['sentiment_dct'][i]['neu'] for i in df.index.tolist()]
    df['positive'] = [df['sentiment_dct'][i]['pos'] for i in df.index.tolist()]
    df['compound'] = [df['sentiment_dct'][i]['compound'] for i in df.index.tolist()]
    df = df.drop(columns='sentiment_dct')

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
                                                   'text': [' '.join],
                                                   'negative': ['mean'],
                                                   'neutral': ['mean'],
                                                   'positive': ['mean'],
                                                   'compound': ['mean']})

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
                            'textjoin': 'text',
                            'negativemean': 'negative',
                            'neutralmean': 'neutral',
                            'positivemean': 'positive',
                            'compoundmean': 'compound'})

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

# Visualize the average Favorites, Retweets and Traffic Counts for journalists and politicians

# Traffic
Traffic = sns.catplot(x='name',
                      y='avg_traffic_count',
                      palette='ch:.25',
                      edgecolor='.6',
                      kind='bar',
                      col='job',
                      data=PS.sort_values(by='avg_traffic_count', ascending=False).head(20),
                      order=PS['name'])

Traffic.set_xticklabels(rotation=90)

# Retweets
sns.catplot(x='avg_retweet_count',
            y='name',
            palette='ch:.25',
            edgecolor='.6',
            kind='bar',
            col='job',
            data=PS.sort_values(by='avg_retweet_count', ascending=False).head(50))

# Favorites
sns.catplot(x='avg_favorite_count',
            y='name',
            palette='ch:.25',
            edgecolor='.6',
            kind='bar',
            col='job',
            data=PS.sort_values(by='avg_favorite_count', ascending=False).head(50))

# Now, we'll create several dataframes with the groupby function, each of them grouping the tweets along
# different aspect. This will allow us to create different wordclouds to analyze different aspects
system_str = ' '.join(PS['text'])
male_str = ' '.join(PS['text'][PS['gender'] == 'Male'])
female_str = ' '.join(PS['text'][PS['gender'] == 'Female'])

# Creating the wordclouds

# Remove stopwords from the system string
system_token = system_str.split()
system_token = [word for word in system_token if word not in stopwords_lst]
system_wc = ' '.join(system_token)

bidi_text = get_display(system_wc)
wordcloud = WordCloud(max_font_size=80,
                      max_words=100,
                      background_color='white',
                      font_path=r'FreeSansBold.ttf').generate(bidi_text)

# Present the wordcloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Exporting the wordcloud
wordcloud.to_file(r'Wordlocuds/name.png')

# Word count function


def word_count(str):
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


# Gender analysis
male_count = word_count(male_str)
female_count = word_count(female_str)
male_tweets_num = len(PS[PS['gender'] == 'Male'])
female_tweets_num = len(PS[PS['gender'] == 'Female'])

# Merge
gender_df = pd.merge(male_count,
                     female_count,
                     how='outer',
                     on='word',
                     suffixes=['_male', '_female'])

# Assign nan values the value zero, beacuse they indicates zero use of these words
gender_df = gender_df.fillna(0)

# Drop Stopwords
gender_df = gender_df[~gender_df['word'].isin(stopwords_lst)].reset_index(drop=True)

# Normalize the word count to the number of tweets by male and female
gender_df['count_male'] = gender_df['count_male']/male_tweets_num
gender_df['count_female'] = gender_df['count_female']/female_tweets_num

# Compute the differnce in the count of each word between males and females
# A positive number indicates words that were used more frequently by females than by males.
# A negative number indictaes the opposite
gender_df['difference'] = gender_df['count_female'] - gender_df['count_male']

# Sort dataframe by the difference column and reset index
gender_df = gender_df.sort_values(by='difference', ascending=False).reset_index(drop=True)

# Subset only the head and the tail of the dataframe, i.e, the values with largest difference in absolute values
gender_df_disp = pd.concat([gender_df.head(20), gender_df.tail(20)])

# Reverse hebrew words, for visualization purposes
gender_df_disp['word'] = [get_display(word) for word in gender_df_disp['word']]

# Visualize
sns.catplot(x='difference',
            y='word',
            palette='ch:.25',
            edgecolor='.6',
            kind='bar',
            data=gender_df_disp)

# Organizations Analysis
Organizations = PS.groupby(['organization'], as_index=False).agg({'job': ['first'],
                                                                  'tweet_count': ['sum'],
                                                                  'word_count': ['sum'],
                                                                  'char_count': ['sum'],
                                                                  'text': [' '.join]})

Organizations.columns = list(map(''.join, Organizations.columns.values))
Organizations = Organizations.rename(columns={'jobfirst': 'job',
                                              'tweet_countsum': 'tweet_count',
                                              'word_countsum': 'word_count',
                                              'char_countsum': 'char_count',
                                              'textjoin': 'text'})

# Parties
org_lst = []
for organization in Organizations['organization']:
    string = ' '.join(Organizations['text'][Organizations['organization'] == organization])
    count = word_count(string)
    count = count[~count['word'].isin(stopwords_lst)].reset_index(drop=True)
    count.sort_values(by='count').reset_index(drop=True)
    count = count.head(10)
    count.insert(0, 'organization', organization)
    org_lst.append(count)
    
organizations_df = pd.concat(org_lst)
organizations_df_try = organizations_df[organizations_df['organization'].isin(['Haaretz', 'Makor_Rishon'])]
organizations_df_try['word'] = [get_display(word) for word in organizations_df_try['word']]

sns.catplot(x='count', y='word',
            col='organization', aspect=.7,
            kind='bar', data=organizations_df_try)


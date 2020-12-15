from wordcloud import WordCloud
from matplotlib import pyplot as plt
import seaborn as sns
from bidi.algorithm import get_display
from Stopwords import stopwords_lst

# Visualize the average Favorites, Retweets and Traffic Counts for journalists and politicians

# Traffic
fig, ax = plt.subplots(1, 2)
ax[0] = sns.barplot(x='avg_favorite_count',
                    y='name',
                    palette='ch:.25',
                    edgecolor='.6',
                    ax=ax[0],
                    data=PS[PS['job'] == 'Journalist'].sort_values(by='avg_favorite_count',
                                                                   ascending=False).head(20))

ax[1] = sns.barplot(x='avg_favorite_count',
                    y='name',
                    palette='ch:.25',
                    edgecolor='.6',
                    ax=ax[1],
                    data=PS[PS['job'] == 'Politician'].sort_values(by='avg_favorite_count',
                                                                   ascending=False).head(20))
fig.show(ax)

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

# Sentiment
sns.catplot(x=('compound'),
            y='name',
            palette='ch:.25',
            edgecolor='.6',
            kind='bar',
            data=Journalists.sort_values(by='compound', ascending=False))

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
gender_df['count_male'] = gender_df['count_male'] / male_tweets_num
gender_df['count_female'] = gender_df['count_female'] / female_tweets_num

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


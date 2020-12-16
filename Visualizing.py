import pandas as pd
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import seaborn as sns
from bidi.algorithm import get_display
from Stopwords import stopwords_lst

# Week number
week = '1'

# Import data
PS = pd.read_csv(r'Data\Organized\Week' + week + '.csv')


##################################################     WORDCLOUD     ##################################################


# First, we'll create several dataframes with the groupby function, each of them grouping the tweets along
# different aspect. This will allow us to create different wordclouds to analyze different aspects
system_str = ' '.join(PS['text'])

# Remove stopwords from the system string
system_token = system_str.split()
system_token = [word for word in system_token if word not in stopwords_lst]
system_wc = ' '.join(system_token)

# Reverse the words for correct visualization in hebrew
bidi_text = get_display(system_wc)

# Generate the wordcloud
wordcloud = WordCloud(max_font_size=80,
                      max_words=100,
                      background_color='white',
                      font_path=r'FreeSansBold.ttf').generate(bidi_text)

# Present the wordcloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Exporting the wordcloud
wordcloud.savefig(r'Visualizations\Wordclouds\Wordcloud_' + week + '.png')


##################################################      TRAFFIC      ##################################################


# Visualize the average Favorites, Retweets and Traffic Counts for journalists and politicians

# FAVORITES - Politicians and Journalists plot
# Set plotting area
fav_fig, fav_ax = plt.subplots(1, 2)

# Plot journalist figure
j_fav_fig = sns.barplot(x='avg_favorite_count',
                        y='hebrew_name',
                        palette='ch:.25',
                        edgecolor='.6',
                        ax=fav_ax[0],
                        data=PS[PS['job'] == 'Journalist'].sort_values(by='avg_favorite_count',
                                                                       ascending=False).head(20))

# Set main title to journalist figure
j_fav_fig.set_title(get_display('עיתונאים'), fontsize=14)

p_fav_fig = sns.barplot(x='avg_favorite_count',
                        y='hebrew_name',
                        palette='ch:.25',
                        edgecolor='.6',
                        ax=fav_ax[1],
                        data=PS[PS['job'] == 'Politician'].sort_values(by='avg_favorite_count',
                                                                       ascending=False).head(20))

# Set main title to politicians figure
p_fav_fig.set_title(get_display('פוליטיקאים'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    fav_ax[i].set_xlabel('')
    fav_ax[i].set_ylabel('')

# Show the favorites figure
fav_fig.show(fav_ax)


# RETWEETS - Politicians and Journalists plot
rt_fig, rt_ax = plt.subplots(1, 2)

# Plot journalist figure
j_rt_fig = sns.barplot(x='avg_retweet_count',
                       y='hebrew_name',
                       palette='ch:.25',
                       edgecolor='.6',
                       ax=rt_ax[0],
                       data=PS[PS['job'] == 'Journalist'].sort_values(by='avg_retweet_count',
                                                                      ascending=False).head(20))

# Set main title to journalist figure
j_rt_fig.set_title(get_display('עיתונאים'), fontsize=14)

p_rt_fig = sns.barplot(x='avg_retweet_count',
                       y='hebrew_name',
                       palette='ch:.25',
                       edgecolor='.6',
                       ax=rt_ax[1],
                       data=PS[PS['job'] == 'Politician'].sort_values(by='avg_retweet_count',
                                                                      ascending=False).head(20))

# Set main title to politicians figure
p_rt_fig.set_title(get_display('פוליטיקאים'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    rt_ax[i].set_xlabel('')
    rt_ax[i].set_ylabel('')

# Show the retweets figure
rt_fig.show(rt_ax)

# Save figures
fav_fig.savefig(r'Visualizations\Favorites\Favorites_' + week + '.png')
rt_fig.savefig(r'Visualizations\Retweets\Retweets_' + week + '.png')

# Sentiment
sns.catplot(x=('compound'),
            y='name',
            palette='ch:.25',
            edgecolor='.6',
            kind='bar',
            data=Journalists.sort_values(by='compound', ascending=False))


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


##################################################       GENDER       ##################################################



male_str = ' '.join(PS['text'][PS['gender'] == 'Male'])
female_str = ' '.join(PS['text'][PS['gender'] == 'Female'])
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

gen_fig_traffic, gen_ax_traffic = plt.subplots(1, 2)

# Gender favorites boxplot
sns.boxplot(x='job',
            y='avg_favorite_count',
            palette='Set3',
            hue='gender',
            showfliers=False,
            ax=gen_ax_traffic[0],
            data=PS)

# Gender retweet boxplot
sns.boxplot(x='job',
            y='avg_retweet_count',
            palette='Set3',
            hue='gender',
            showfliers=False,
            ax=gen_ax_traffic[1],
            data=PS)

gen_fig_traffic.show(gen_ax_traffic)

gen_fig_words, gen_ax_words = plt.subplots(1, 2)

# Gender word count boxplot
# Gender char count boxplot
sns.boxplot(x='job',
            y='avg_char_count',
            palette='Set3',
            hue='gender',
            showfliers=False,
            ax=gen_ax_words[0],
            data=PS)

sns.boxplot(x='job',
            y='avg_word_count',
            palette='Set3',
            hue='gender',
            showfliers=False,
            ax=gen_ax_words[1],
            data=PS)

gen_fig_words.show(gen_ax_words)

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

# Party favorites boxplot
sns.boxplot(x='job',
            y='avg_favorite_count',
            palette='Set3',
            hue='organization',
            showfliers=False,
            data=PS[PS['job'] == 'Politician'])

# Party retweet boxplot
sns.boxplot(x='job',
            y='avg_retweet_count',
            palette='Set3',
            hue='organization',
            showfliers=False,
            data=PS[PS['job'] == 'Politician'])

# Party word count boxplot
sns.boxplot(x='job',
            y='avg_word_count',
            palette='Set3',
            hue='organization',
            showfliers=False,
            data=PS[PS['job'] == 'Politician'])

# Party char count boxplot
sns.boxplot(x='job',
            y='avg_char_count',
            palette='Set3',
            hue='organization',
            showfliers=False,
            data=PS[PS['job'] == 'Politician'])


# Media favorites boxplot
sns.boxplot(x='job',
            y='avg_favorite_count',
            palette='Set3',
            hue='organization',
            showfliers=False,
            data=PS[PS['job'] == 'Journalist'])

# Media retweet boxplot
sns.boxplot(x='job',
            y='avg_retweet_count',
            palette='Set3',
            hue='organization',
            showfliers=False,
            data=PS[PS['job'] == 'Journalist'])

# Media word count boxplot
sns.boxplot(x='job',
            y='avg_word_count',
            palette='Set3',
            hue='organization',
            showfliers=False,
            data=PS[PS['job'] == 'Journalist'])

# Media char count boxplot
sns.boxplot(x='job',
            y='avg_char_count',
            palette='Set3',
            hue='organization',
            showfliers=False,
            data=PS[PS['job'] == 'Journalist'])

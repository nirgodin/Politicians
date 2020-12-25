import pandas as pd
from _datetime import datetime
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
from bidi.algorithm import get_display
from Stopwords import stopwords_lst

# Week number and print data
week = '1'
printDate = str(datetime.now().day) + '-' + str(datetime.now().month) + '-' + str(datetime.now().year)

# Import data
PS = pd.read_csv(r'Data\Organized' + '\\' + printDate + '.csv')

# Defining few functions that will be relevant for the visualizations
# First function takes a sorted dataframe and returns only the head and the tail of it, with the specified num. of rows


def head_and_tail(df, nrow=20):
    df = df.head(nrow).append(df.tail(nrow))
    return df


# Second function takes a str and returns a dataframe with all the unique words in the string
# and the times each word appeared in it


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


# Creating an organization df, which will be useful for some of the visualizations
Organizations = PS.groupby(['organization'], as_index=False).agg({'job': ['first'],
                                                                  'retweet_count': ['sum', 'mean'],
                                                                  'favorite_count': ['sum', 'mean'],
                                                                  'word_count': ['sum', 'mean'],
                                                                  'char_count': ['sum', 'mean'],
                                                                  'negative': ['mean'],
                                                                  'neutral': ['mean'],
                                                                  'positive': ['mean'],
                                                                  'compound': ['mean'],
                                                                  'text': [' '.join]})

# Replace column names
Organizations.columns = list(map(''.join, Organizations.columns.values))
Organizations = Organizations.rename(columns={'jobfirst': 'job',
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
                                              'compoundmean': 'compound',
                                              'textjoin': 'text'})


##################################################     WORDCLOUD     ##################################################


# First, we'll create several dataframes with the groupby function, each of them grouping the tweets along
# different aspect. This will allow us to create different wordclouds to analyze different aspects
system_str = ' '.join(PS['text'])

# Remove stopwords from the system string - splitting, removing and joining back
system_token = system_str.split()
system_token = [word for word in system_token if word not in stopwords_lst]
system_wc = ' '.join(system_token)

# Reverse the words for correct visualization in hebrew
bidi_text = get_display(system_wc)

# Generate the wordcloud
wordcloud = WordCloud(max_font_size=80,
                      max_words=80,
                      background_color='white',
                      width=600,
                      height=335,
                      font_path=r'FreeSansBold.ttf').generate(bidi_text)

# Present the wordcloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Exporting the wordcloud
wordcloud.to_file(r'Visualizations\Wordclouds\Wordcloud ' + printDate + '.png')


################################################      TWEETS COUNT      ################################################


# Set plotting area
twt_fig, twt_ax = plt.subplots(1, 2)
twt_fig.set_size_inches(6, 3.35)

# Plot journalist figure
j_twt_fig = sns.barplot(x='tweet_count',
                        y='hebrew_name',
                        palette='ch:.25',
                        edgecolor='.6',
                        ax=twt_ax[0],
                        data=PS[PS['job'] == 'Journalist'].sort_values(by='tweet_count',
                                                                       ascending=False).head(20))

# Set title to journalist figure
j_twt_fig.set_title(get_display('עיתונאים'), fontsize=14)

p_twt_fig = sns.barplot(x='tweet_count',
                        y='hebrew_name',
                        palette='ch:.25',
                        edgecolor='.6',
                        ax=twt_ax[1],
                        data=PS[PS['job'] == 'Politician'].sort_values(by='tweet_count',
                                                                       ascending=False).head(20))

# Set title to politicians figure
p_twt_fig.set_title(get_display('פוליטיקאים'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    twt_ax[i].set_xlabel('')
    twt_ax[i].set_ylabel('')

# Set main title to the whole figure
twt_fig.suptitle(get_display('הצייצנים הפעילים ביותר'), fontsize=16)

# Show the tweet count figure
twt_fig.show(twt_ax)

# Export the tweet count figure
twt_fig.savefig(r'Visualizations\Tweets\Tweets ' + printDate + '.png')


#################################################      FAVORITES      #################################################


# Visualize the average Favorites, Retweets and Traffic Counts for journalists and politicians

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

# Set title to journalist figure
j_fav_fig.set_title(get_display('עיתונאים'), fontsize=14)

p_fav_fig = sns.barplot(x='avg_favorite_count',
                        y='hebrew_name',
                        palette='ch:.25',
                        edgecolor='.6',
                        ax=fav_ax[1],
                        data=PS[PS['job'] == 'Politician'].sort_values(by='avg_favorite_count',
                                                                       ascending=False).head(20))

# Set title to politicians figure
p_fav_fig.set_title(get_display('פוליטיקאים'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    fav_ax[i].set_xlabel('')
    fav_ax[i].set_ylabel('')

# Set main title to the whole figure
fav_fig.suptitle(get_display('הצייצנים עם מספר הפברוטים הגבוה ביותר'), fontsize=16)

# Show the favorites figure
fav_fig.show(fav_ax)


##################################################      RETWEETS      ##################################################


# Set plotting area
rt_fig, rt_ax = plt.subplots(1, 2)

# Plot journalist figure
j_rt_fig = sns.barplot(x='avg_retweet_count',
                       y='hebrew_name',
                       palette='ch:.25',
                       edgecolor='.6',
                       ax=rt_ax[0],
                       data=PS[PS['job'] == 'Journalist'].sort_values(by='avg_retweet_count',
                                                                      ascending=False).head(20))

# Set title to journalist figure
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

# Set main title to the whole figure
rt_fig.suptitle(get_display('הצייצנים עם מספר הריטוויטים הממוצע הגבוה ביותר'), fontsize=16)

# Show the retweets figure
rt_fig.show(rt_ax)

# Save figures
fav_fig.savefig(r'Visualizations\Favorites\Favorites ' + printDate + '.png')
rt_fig.savefig(r'Visualizations\Retweets\Retweets ' + printDate + '.png')


#############################################      SENTIMENT - PEOPLE      #############################################


# Set plotting area
sentiment_ppl_fig, sentiment_ppl_ax = plt.subplots(1, 2)

# Plot journalist figure
j_sentiment_ppl_fig = sns.barplot(x='compound',
                                  y='hebrew_name',
                                  palette='ch:.25',
                                  edgecolor='.6',
                                  ax=sentiment_ppl_ax[0],
                                  data=head_and_tail(PS[PS['job'] == 'Journalist'].sort_values(by='compound',
                                                                                               ascending=False)))

# Set title to journalist figure
j_sentiment_ppl_fig.set_title(get_display('עיתונאים'), fontsize=14)

p_sentiment_ppl_fig = sns.barplot(x='compound',
                              y='hebrew_name',
                              palette='ch:.25',
                              edgecolor='.6',
                              ax=sentiment_ppl_ax[1],
                              data=head_and_tail(PS[PS['job'] == 'Politician'].sort_values(by='compound',
                                                                                           ascending=False)))

# Set title to politicians figure
p_sentiment_ppl_fig.set_title(get_display('פוליטיקאים'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    sentiment_ppl_ax[i].set_xlabel('')
    sentiment_ppl_ax[i].set_ylabel('')

# Set main title to the whole figure
sentiment_ppl_fig.suptitle(get_display('הצייצנים עם הציוצים החיוביים ביותר והשליליים ביותר'), fontsize=16)

# Show the retweets figure
sentiment_ppl_fig.show(sentiment_ppl_ax)


#######################################       GENDER - WORD USE DIFFERENCE       #######################################


male_str = ' '.join(PS['text'][PS['gender'] == 'Male'])
female_str = ' '.join(PS['text'][PS['gender'] == 'Female'])
male_word_count = word_count(male_str)
female_word_count = word_count(female_str)
male_twt_count = len(PS[PS['gender'] == 'Male'])
female_twt_count = len(PS[PS['gender'] == 'Female'])

# Merge
gender_df = pd.merge(male_word_count,
                     female_word_count,
                     how='outer',
                     on='word',
                     suffixes=['_male', '_female'])

# Assign nan values the value zero, beacuse they indicates zero use of these words
gender_df = gender_df.fillna(0)

# Drop Stopwords
gender_df = gender_df[~gender_df['word'].isin(stopwords_lst)].reset_index(drop=True)

# Apply the get_display on the word for the visualization
gender_df['word'] = [get_display(word) for word in gender_df['word']]

# Normalize the word count to the number of tweets by male and female
gender_df['count_male'] = gender_df['count_male'] / male_twt_count
gender_df['count_female'] = gender_df['count_female'] / female_twt_count

# Compute the differnce in the count of each word between males and females
# A positive number indicates words that were used more frequently by females than by males.
# A negative number indictaes the opposite
gender_df['difference'] = gender_df['count_female'] - gender_df['count_male']

# Visualize
gen_word_diff = sns.catplot(x='difference',
                            y='word',
                            palette='ch:.25',
                            edgecolor='.6',
                            kind='bar',
                            data=head_and_tail(gender_df.sort_values(by='difference',
                                                                     ascending=False).reset_index(drop=True)))


########################################       GENDER - TRAFFIC ANALYSIS       ########################################


gen_fig_traffic, gen_ax_traffic = plt.subplots(1, 2)

# Gender favorites boxplot
fav_gen_fig = sns.boxplot(x='job',
                          y='avg_favorite_count',
                          palette='Set3',
                          hue='gender',
                          showfliers=False,
                          ax=gen_ax_traffic[0],
                          data=PS[PS['gender'].notna()])

# Set title to the gender favorites subplot
fav_gen_fig.set_title(get_display('פברוטים'), fontsize=14)

# Gender retweet boxplot
rt_gen_fig = sns.boxplot(x='job',
                         y='avg_retweet_count',
                         palette='Set3',
                         hue='gender',
                         showfliers=False,
                         ax=gen_ax_traffic[1],
                         data=PS[PS['gender'].notna()])

# Set title to the gender retweets subplot
rt_gen_fig.set_title(get_display('ריטוויטים'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    gen_ax_traffic[i].set_xlabel('')
    gen_ax_traffic[i].set_ylabel('')

# Set main title to the whole figure
gen_fig_traffic.suptitle(get_display('פברוטים וריטוויטים - לפי מגדר'), fontsize=18)

gen_fig_traffic.show(gen_ax_traffic)


#########################################       GENDER - WORD-CHAR COUNT       #########################################


gen_fig_words, gen_ax_words = plt.subplots(1, 2)

# Gender char count boxplot
sns.boxplot(x='job',
            y='avg_char_count',
            palette='Set3',
            hue='gender',
            showfliers=False,
            ax=gen_ax_words[0],
            data=PS)

# Gender word count boxplot
sns.boxplot(x='job',
            y='avg_word_count',
            palette='Set3',
            hue='gender',
            showfliers=False,
            ax=gen_ax_words[1],
            data=PS)

gen_fig_words.show(gen_ax_words)


#######################################       GENDER - SENTIMENT ANALYSIS       #######################################


# Gender char count boxplot
gen_fig_snt = sns.boxplot(x='job',
                          y='compound',
                          palette='Set3',
                          hue='gender',
                          showfliers=False,
                          data=PS[PS['job'].isin(['Journalist', 'Politician'])])


##############################################       ORGANIZATIONS       ##############################################


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


#####################################      ORGANIZATIONS - SENTIMENT ANALYSIS      #####################################


# Set plotting area
sentiment_org_fig, sentiment_org_ax = plt.subplots(1, 2)

# Plot journalist figure
j_sentiment_org_fig = sns.barplot(x='compound',
                                  y='organization',
                                  palette='ch:.25',
                                  edgecolor='.6',
                                  ax=sentiment_org_ax[0],
                                  data=head_and_tail(Organizations[Organizations['job'] == 'Journalist'].sort_values(by='compound',
                                                                                                                     ascending=False)))

# Set title to journalist figure
j_sentiment_org_fig.set_title(get_display('כלי תקשורת'), fontsize=14)

p_sentiment_org_fig = sns.barplot(x='compound',
                                  y='organization',
                                  palette='ch:.25',
                                  edgecolor='.6',
                                  ax=sentiment_org_ax[1],
                                  data=head_and_tail(Organizations[Organizations['job'] == 'Politician'].sort_values(by='compound',
                                                                                                                     ascending=False)))

# Set title to politicians figure
p_sentiment_org_fig.set_title(get_display('מפלגות'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    sentiment_org_ax[i].set_xlabel('')
    sentiment_org_ax[i].set_ylabel('')

# Set main title to the whole figure
sentiment_org_fig.suptitle(get_display('כלי התקשורת והמפלגות עם הציוצים החיוביים ביותר והשליליים ביותר'), fontsize=16)

# Show the retweets figure
sentiment_org_fig.show(sentiment_org_ax)

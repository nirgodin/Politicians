import numpy as np
import pandas as pd
from _datetime import datetime
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import re
import seaborn as sns
from bidi.algorithm import get_display
from Stopwords import stopwords_lst, verb_lst
from Functions import head_and_tail, word_count, df_punct, df_organizer

# Week number and print data
week = '4'
printDate = str(datetime.now().day) + '-' + str(datetime.now().month) + '-' + str(datetime.now().year)

# Import data
# Weekly data
weekly = pd.read_csv(r'Data\Raw\Weekly\Raw ' + printDate + '.csv')
weekly = df_punct(weekly)

# Overall data
PS = pd.read_csv(r'Data\Raw\Raw.csv')
PS = df_punct(PS)
PS = PS[PS['rt'] == 0]
PS = df_organizer(PS, sentiment='off')


# # Creating an organization df, which will be useful for some of the visualizations
# Organizations = PS.groupby(['organization'], as_index=False).agg({'job': ['first'],
#                                                                   'refollowers_count': ['sum', 'mean'],
#                                                                   'favorite_count': ['sum', 'mean'],
#                                                                   'word_count': ['sum', 'mean'],
#                                                                   'char_count': ['sum', 'mean'],
#                                                                   'negative': ['mean'],
#                                                                   'neutral': ['mean'],
#                                                                   'positive': ['mean'],
#                                                                   'compound': ['mean'],
#                                                                   'text': [' '.join]})
#
# # Replace column names
# Organizations.columns = list(map(''.join, Organizations.columns.values))
# Organizations = Organizations.rename(columns={'jobfirst': 'job',
#                                               'refollowers_countsum': 'refollowers_count',
#                                               'refollowers_countmean': 'avg_refollowers_count',
#                                               'favorite_countsum': 'favorite_count',
#                                               'favorite_countmean': 'avg_favorite_count',
#                                               'word_countsum': 'word_count',
#                                               'word_countmean': 'avg_word_count',
#                                               'char_countsum': 'char_count',
#                                               'char_countmean': 'avg_char_count',
#                                               'negativemean': 'negative',
#                                               'neutralmean': 'neutral',
#                                               'positivemean': 'positive',
#                                               'compoundmean': 'compound',
#                                               'textjoin': 'text'})


##################################################     WORDCLOUD     ##################################################


# First, we'll create several dataframes with the groupby function, each of them grouping the tweets along
# different aspect. This will allow us to create different wordclouds to analyze different aspects
system_str = ' '.join(weekly['text'])

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
twt_fig.set_size_inches(12, 6.7)

# Plot journalist figure
j_twt_fig = sns.barplot(x='followers_count',
                        y='hebrew_name',
                        palette='ch:.25',
                        edgecolor='.6',
                        ax=twt_ax[0],
                        data=PS[PS['job'] == 'Journalist'].sort_values(by='followers_count',
                                                                       ascending=False).head(20))

# Set title to journalist figure
j_twt_fig.set_title(get_display('עיתונאים'), fontsize=14)

p_twt_fig = sns.barplot(x='followers_count',
                        y='hebrew_name',
                        palette='ch:.25',
                        edgecolor='.6',
                        ax=twt_ax[1],
                        data=PS[PS['job'] == 'Politician'].sort_values(by='followers_count',
                                                                       ascending=False).head(20))

# Set title to politicians figure
p_twt_fig.set_title(get_display('פוליטיקאים'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    twt_ax[i].set_xlabel(get_display('מספר ציוצים'))
    twt_ax[i].set_ylabel('')

# Tight layout
twt_fig.tight_layout()

# Show the tweet count figure
twt_fig.show(twt_ax)

# Export the tweet count figure
twt_fig.savefig(r'Visualizations\Tweets\Tweets ' + printDate + '.png')


################################################      FOLLOWERS      ################################################


# Transform followers count to thosands
PS['followers_count'] = PS['followers_count'].apply(lambda x: x/1000)

# Set plotting area
flw_fig, flw_ax = plt.subplots(1, 2)
flw_fig.set_size_inches(12, 6.7)

# Plot journalist figure
j_flw_fig = sns.barplot(x=('followers_count'),
                        y='hebrew_name',
                        palette='ch:.25',
                        edgecolor='.6',
                        ax=flw_ax[0],
                        data=PS[PS['job'] == 'Journalist'].sort_values(by='followers_count',
                                                                       ascending=False).head(20))

# Set title to journalist figure
j_flw_fig.set_title(get_display('עיתונאים'), fontsize=14)

p_flw_fig = sns.barplot(x='followers_count',
                        y='hebrew_name',
                        palette='ch:.25',
                        edgecolor='.6',
                        ax=flw_ax[1],
                        data=PS[PS['job'] == 'Politician'].sort_values(by='followers_count',
                                                                       ascending=False).head(20))

# Set title to politicians figure
p_flw_fig.set_title(get_display('פוליטיקאים'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    flw_ax[i].set_xlabel(get_display('מספר עוקבים'))
    flw_ax[i].set_ylabel('')

# Tight layout
flw_fig.tight_layout()

# Show the tweet count figure
flw_fig.show(flw_ax)

# Export the tweet count figure
flw_fig.savefig(r'Visualizations\Tweets\Tweets ' + printDate + '.png')


#################################################      FAVORITES      #################################################


# Visualize the average Favorites, Retweets and Traffic Counts for journalists and politicians

# Set plotting area
fav_fig, fav_ax = plt.subplots(1, 2)
fav_fig.set_size_inches(12, 6.7)

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
    fav_ax[i].set_xlabel(get_display('ממוצע פברוטים לציוץ'))
    fav_ax[i].set_ylabel('')

# Tight layout
fav_fig.tight_layout()

# Show the favorites figure
fav_fig.show(fav_ax)

# Export the favorites count figure
fav_fig.savefig(r'Visualizations\Favorites\Favorites ' + printDate + '.png')


##################################################      RETWEETS      ##################################################


# Set plotting area
rt_fig, rt_ax = plt.subplots(1, 2)
rt_fig.set_size_inches(12, 6.7)

# Plot journalist figure
j_rt_fig = sns.barplot(x='avg_refollowers_count',
                       y='hebrew_name',
                       palette='ch:.25',
                       edgecolor='.6',
                       ax=rt_ax[0],
                       data=PS[PS['job'] == 'Journalist'].sort_values(by='avg_refollowers_count',
                                                                      ascending=False).head(20))

# Set title to journalist figure
j_rt_fig.set_title(get_display('עיתונאים'), fontsize=14)

p_rt_fig = sns.barplot(x='avg_refollowers_count',
                       y='hebrew_name',
                       palette='ch:.25',
                       edgecolor='.6',
                       ax=rt_ax[1],
                       data=PS[PS['job'] == 'Politician'].sort_values(by='avg_refollowers_count',
                                                                      ascending=False).head(20))

# Set main title to politicians figure
p_rt_fig.set_title(get_display('פוליטיקאים'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    rt_ax[i].set_xlabel(get_display('ממוצע ריטוויטים לציוץ'))
    rt_ax[i].set_ylabel('')

# Tight layout
rt_fig.tight_layout()

# Show the retweets figure
rt_fig.show(fav_ax)

# Export the retweets count figure
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


PS['text'] = [re.sub(r'[A-Z,a-z,\d+,_,]+', "", txt) for txt in PS['text']]

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
gender_df = gender_df[~gender_df['word'].isin(stopwords_lst + verb_lst)].reset_index(drop=True)

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


########################################       GENDER - TRAFFIC BARPLOTS       ########################################


# Set plotting area
gen_fig_barplot, gen_ax_barplot = plt.subplots(1, 2)
gen_fig_barplot.set_size_inches(12, 6.7)

# Favorites barplot
fav_gen_barplot = sns.barplot(x='job',
                              y='favorite_count',
                              hue='gender',
                              ax=gen_ax_barplot[0],
                              data=PS[PS['gender'].notna()])

# Set title to the gender favorites subplot
fav_gen_barplot.set_title(get_display('Likes'), fontsize=14)

# Remove the left legend
gen_ax_barplot[0].legend([], [], frameon=False)

# Retweets barplot
rt_gen_barplot = sns.barplot(x='job',
                             y='refollowers_count',
                             hue='gender',
                             ax=gen_ax_barplot[1],
                             data=PS[PS['gender'].notna()])

# Set title to the gender retweets subplot
rt_gen_barplot.set_title(get_display('Retweets'), fontsize=14)

# Modify slightly the legend
gen_ax_barplot[1].legend(title='Gender')

# Delete subplots axes titles
for i in range(0, 2):
    gen_ax_barplot[i].set_xlabel('')
    gen_ax_barplot[i].set_ylabel('')

# Tight layout
gen_fig_barplot.tight_layout()

# Show the retweets figure
gen_fig_barplot.show(gen_ax_barplot)

# Export the retweets count figure
gen_fig_barplot.savefig(r'Visualizations\Gender\Traffic Barplot ' + printDate + '.png')

########################################       GENDER - TRAFFIC BOXPLOTS       ########################################

BP = PS[(PS['favorite_count'] != 0) & (PS['refollowers_count'] != 0)]
BP['log_favorite_count'] = np.log(PS['favorite_count'])
BP['log_refollowers_count'] = np.log(PS['refollowers_count'])

# Set plotting area
gen_fig_boxplot, gen_ax_boxplot = plt.subplots(1, 2)
gen_fig_boxplot.set_size_inches(12, 6.7)

# Gender favorites boxplot
fav_gen_boxplot = sns.boxplot(x='job',
                              y='log_favorite_count',
                              hue='gender',
                              showfliers=False,
                              ax=gen_ax_boxplot[0],
                              data=BP[BP['gender'].notna()])

# Remove the left legend
gen_ax_boxplot[0].legend([], [], frameon=False)

# Set title to the gender favorites subplot
fav_gen_boxplot.set_title(get_display('Likes'), fontsize=14)

# Gender retweet boxplot
rt_gen_boxplot = sns.boxplot(x='job',
                             y='log_refollowers_count',
                             hue='gender',
                             showfliers=False,
                             ax=gen_ax_boxplot[1],
                             data=BP[BP['gender'].notna()])

# Set title to the gender retweets subplot
rt_gen_boxplot.set_title(get_display('Retweets'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    gen_ax_boxplot[i].set_xlabel('')
    gen_ax_boxplot[i].set_ylabel('')

# Modify slightly the legend
gen_ax_boxplot[1].legend(title='Gender')

# Tight layout
gen_fig_boxplot.tight_layout()

# Show the retweets figure
gen_fig_boxplot.show(gen_ax_boxplot)

# Export the retweets count figure
gen_fig_boxplot.savefig(r'Visualizations\Gender\Traffic Boxplot ' + printDate + '.png')


#########################################       GENDER - WORD-CHAR COUNT       #########################################


gen_fig_words, gen_ax_words = plt.subplots(1, 2)

# Gender char count boxplot
sns.boxplot(x='job',
            y='avg_char_count',
            palette='Set3',
            hue='gender',
            showfliers=False,
            ax=gen_ax_words[0],
            data=PS[PS['gender'].notna()])

# Gender word count boxplot
sns.boxplot(x='job',
            y='avg_word_count',
            palette='Set3',
            hue='gender',
            showfliers=False,
            ax=gen_ax_words[1],
            data=PS[PS['gender'].notna()])

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
                                                                  'followers_count': ['sum'],
                                                                  'word_count': ['sum'],
                                                                  'char_count': ['sum'],
                                                                  'text': [' '.join]})

Organizations.columns = list(map(''.join, Organizations.columns.values))
Organizations = Organizations.rename(columns={'jobfirst': 'job',
                                              'followers_countsum': 'followers_count',
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
            y='avg_refollowers_count',
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
            y='avg_refollowers_count',
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


#####################################      TIMESERIES -  SENTIMENT ANALYSIS      #####################################


dt = pd.read_csv(r'Data\Sentiment\Sentiment.csv')

# Transform the created at column to a date column with datetime format
dt['created_at'] = dt['created_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date())

# Group by date, and return the mean sentiment values
dt = dt.groupby(['created_at', 'job'], as_index=False).agg({'negative': ['mean'],
                                                     'neutral': ['mean'],
                                                     'positive': ['mean'],
                                                     'compound': ['mean']})

# Replace column names
dt.columns = list(map(''.join, dt.columns.values))
dt = dt.rename(columns={'created_at': 'date',
                        'negativemean': 'negative',
                        'neutralmean': 'neutral',
                        'positivemean': 'positive',
                        'compoundmean': 'compound'})

# Transform dataframe to long format
dt2 = pd.melt(dt,
              id_vars='date',
              value_vars=['negative', 'neutral', 'positive', 'compound'])

# Plot the compound sentiment over time
sns.lineplot(x='date',
             y='value',
             hue='variable',
             data=dt2)


# Compute traffic and average traffic count
df['traffic_count'] = df['refollowers_count'] + df['favorite_count']
df['avg_traffic_count'] = df['traffic_count'] / df['followers_count']

# Apply the get_display function on all the hebew names in the dataframe
df['hebrew_name'] = [get_display(df['hebrew_name'][i]) for i in df.index.tolist()]

# Drop rows with null text
df = df[df['text'] != '']


########################################             SCATTERPLOTS             ########################################

# Insert Word count and char count columns
PS['word_count'] = PS['text'].apply(lambda x: len(str(x).split(" ")))
PS['char_count'] = PS['text'].apply(lambda x: sum(len(word) for word in str(x).split(" ")))

# Scatterplot - Word count vs. favorites
sns.scatterplot(x='char_count',
                y='favorite_count',
                data=PS)

# Distplot - word and char count
sns.distplot(PS['char_count'])

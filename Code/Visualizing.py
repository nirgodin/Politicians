import numpy as np
import pandas as pd
from _datetime import datetime
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import re
import seaborn as sns
import demoji
from bidi.algorithm import get_display
from Code.Stopwords import stopwords_lst, verb_lst
from Code.Functions import head_and_tail, word_count, df_punct, df_organizer, to_datetime
from Code.Dictionaries import type_dct

# Set print date
printDate = str(datetime.now().day) + '-' + str(datetime.now().month) + '-' + str(datetime.now().year)

# Import data
# Weekly data
weekly = pd.read_csv(r'Data\Raw\Weekly\Raw ' + printDate + '.csv')

# Creating a dict of emoji' appearing in the df
emj_dct = demoji.findall(' '.join(weekly['text']))

# Removing punctuation
weekly = df_punct(weekly)

# Sentiment data
PS = pd.read_csv(r'Data\Sentiment\Sentiment.csv')
PS = PS[PS['rt'] == 0].reset_index(drop=True)
PS = df_organizer(PS, sentiment='on')


##################################################     WORDCLOUD     ##################################################


# First, we'll create several dataframes with the groupby function, each of them grouping the tweets along
# different aspect. This will allow us to create different wordclouds to analyze different aspects
system_str = ' '.join(weekly['text'])

# Remove emoji's from str
for emoji in emj_dct.values():
    system_str = system_str.replace(emoji, '')

# Remove stopwords from the system string - splitting, removing and joining back
system_token = system_str.split()
system_token = [word for word in system_token if word not in (stopwords_lst + verb_lst)]
system_wc = ' '.join(system_token)

# Reverse the words for correct visualization in hebrew
bidi_text = get_display(system_wc)

# Generate the wordcloud
wordcloud = WordCloud(max_font_size=80,
                      max_words=80,
                      background_color='white',
                      width=600,
                      height=335,
                      font_path=r'Other\FreeSansBold.ttf').generate(bidi_text)

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
PS['followers_count'] = PS['followers_count']/1000

# Set plotting area
flw_fig, flw_ax = plt.subplots(1, 2)
flw_fig.set_size_inches(12, 6.7)

# Plot journalist figure
j_flw_fig = sns.barplot(x=('followers_count'),
                        y='hebrew_name',
                        hue='gender',
                        dodge=False,
                        # palette='ch:.25',
                        # edgecolor='.6',
                        ax=flw_ax[0],
                        data=PS[PS['job'] == 'Journalist'].sort_values(by='followers_count',
                                                                       ascending=False).head(20))

# Set title to journalist figure
j_flw_fig.set_title(get_display('עיתונאים'), fontsize=14)

# Remove the left legend
flw_ax[0].legend([], [], frameon=False)

p_flw_fig = sns.barplot(x='followers_count',
                        y='hebrew_name',
                        hue='gender',
                        dodge=False,
                        # palette='ch:.25',
                        # edgecolor='.6',
                        ax=flw_ax[1],
                        data=PS[PS['job'] == 'Politician'].sort_values(by='followers_count',
                                                                       ascending=False).head(20))

# Set title to politicians figure
p_flw_fig.set_title(get_display('פוליטיקאים'), fontsize=14)

# Delete subplots axes titles
for i in range(0, 2):
    flw_ax[i].set_xlabel(get_display('מספר עוקבים (אלפים)'))
    flw_ax[i].set_ylabel('')
    flw_ax[i]

# Tight layout
flw_fig.tight_layout()

# Show the tweet count figure
flw_fig.show(flw_ax)

# Export the tweet count figure
flw_fig.savefig(r'Visualizations\Followers\Followers ' + printDate + '.png')


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


##########################################      SENTIMENT - JOURNALISTS      ##########################################


# Minor data adjustments
# Add media type to journalists and political Gush
PS['type'] = PS['organization'].map(type_dct)
PS['type'] = [get_display(name) for name in PS['type']]

# Set plotting area
j_sentiment_ppl_fig = plt.figure()
j_sentiment_ppl_fig.set_size_inches(12, 6.7)

# Plot journalists figure
j_sentiment_ppl_fig = sns.barplot(x='compound',
                                  y='hebrew_name',
                                  hue='type',
                                  dodge=False,
                                  data=head_and_tail(PS[PS['job'] == 'Journalist'].sort_values(by='compound',
                                                                                               ascending=False),
                                                     nrow=10))

# Set title to journalist figure
j_sentiment_ppl_fig.set_title(get_display('עיתונאים'), fontsize=16)

# Delete subplots axes titles
j_sentiment_ppl_fig.set_xlabel('')
j_sentiment_ppl_fig.set_ylabel('')

# Remove legend title
handles, labels = j_sentiment_ppl_fig.get_legend_handles_labels()
j_sentiment_ppl_fig.legend(handles=handles[0:], labels=labels[0:])

# Change legend position
j_sentiment_ppl_fig.legend(loc='lower right')

# Tight Layout
plt.tight_layout()

# Export figure
jrnl_snt_fig = j_sentiment_ppl_fig.get_figure()
jrnl_snt_fig.savefig(r'Visualizations\Sentiment\Journalists ' + printDate + '.png')


##########################################      SENTIMENT - POLITICIANS      ##########################################

# Set plotting area
p_sentiment_ppl_fig = plt.figure()
p_sentiment_ppl_fig.set_size_inches(12, 6.7)

# Plot politicians figure
p_sentiment_ppl_fig = sns.barplot(x='compound',
                                  y='hebrew_name',
                                  hue='type',
                                  dodge=False,
                                  data=head_and_tail(PS[PS['job'] == 'Politician'].sort_values(by='compound',
                                                                                               ascending=False),
                                                     nrow=10))

# Set title to politicians figure
p_sentiment_ppl_fig.set_title(get_display('פוליטיקאים'), fontsize=16)

# Delete subplots axes titles
p_sentiment_ppl_fig.set_xlabel('')
p_sentiment_ppl_fig.set_ylabel('')

# Remove legend title
handles, labels = p_sentiment_ppl_fig.get_legend_handles_labels()
p_sentiment_ppl_fig.legend(handles=handles[0:], labels=labels[0:])

# Change legend position
p_sentiment_ppl_fig.legend(loc='lower right')

# Tight Layout
plt.tight_layout()

# Export figure
plt_snt_fig = p_sentiment_ppl_fig.get_figure()
plt_snt_fig.savefig(r'Visualizations\Sentiment\Politicians ' + printDate + '.png')




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
dt['created_at'] = to_datetime(dt['created_at'])

# Drop from date column hour, minute and second
dt['created_at'] = [t.date() for t in dt['created_at']]

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
              id_vars=['date', 'job'],
              value_vars='compound')

# Plot the compound sentiment over time
sns.lineplot(x='date',
             y='value',
             hue='job',
             data=dt2)


# Compute traffic and average traffic count
df['traffic_count'] = df['retweet_count'] + df['favorite_count']
df['avg_traffic_count'] = df['traffic_count'] / df['retweet_count']

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


########################################             HEATMAPS             ########################################


DH = PS.copy()

# Subset out media and parties
DH = DH[DH['job'] != 'Media']
DH = DH[DH['job'] != 'Party']

DH = DH[DH['job'] == 'Politician']

# Transform the created at column to a date column with datetime format
DH['created_at'] = to_datetime(DH['created_at'])

# Create day and hour columns
DH['day'] = [t.strftime('%A') for t in DH['created_at']]
DH['hour'] = [t.hour for t in DH['created_at']]

# Groupby day and hour
# Group by date, and return the mean sentiment values
DH = DH.groupby(['day', 'hour'], as_index=False).agg({'favorite_count': ['median'],
                                                      'retweet_count': ['median']})

# Replace column names
DH.columns = list(map(''.join, DH.columns.values))
DH = DH.rename(columns={'favorite_countmedian': 'favorite_count',
                        'retweet_countmedian': 'retweet_count'})

# Round numbers
DH['favorite_count'] = [round(num, 0) for num in DH['favorite_count']]
DH['retweet_count'] = [round(num, 0) for num in DH['retweet_count']]

# Pivot data
fav_hm_df = pd.pivot_table(DH,
                           values='favorite_count',
                           index='day',
                           columns='hour')

# Change column order
fav_hm_df = fav_hm_df.reindex(index=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])

# Favorite Heatmap
sns.heatmap(fav_hm_df,
            cmap='Reds',
            vmax=350,
            annot=True,
            fmt='g',
            linewidths=.5)

# Pivot data
rt_hm_df = pd.pivot_table(DH,
                          values='retweet_count',
                          index='day',
                          columns='hour')

# Change column order
rt_hm_df = rt_hm_df.reindex(index=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])

# retweet Heatmap
sns.heatmap(rt_hm_df,
            cmap='Reds',
            vmax=15,
            annot=True,
            linewidths=.5)


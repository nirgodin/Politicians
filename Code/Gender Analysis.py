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
from Code.Dictionaries import type_dct, politicians_dct

# Data import
PS = pd.read_csv(r'Data\Raw\Raw.csv')

# Make sure texts in text column are in string format
PS['text'] = [str(txt) for txt in PS['text']]

# Remove users tagged
PS['text'] = [' '.join(re.sub('(@[A-Za-z0-9_]+)', ' ', txt).split()) for txt in PS['text']]

PS = df_punct(PS, emoji='off')
PS = PS[PS['rt'] == 0].reset_index(drop=True)
# PS = df_organizer(PS, sentiment='on')

# Set print date
printDate = str(datetime.now().day) + '-' + str(datetime.now().month) + '-' + str(datetime.now().year)


#######################################           WORD USE DIFFERENCE           #######################################

PS = PS[(PS['job'] == 'Journalist') | (PS['job'] == 'Politician')]

# Join separately all texts by males and all texts by females
male_str = ' '.join(PS['text'][PS['gender'] == 'Male'])
female_str = ' '.join(PS['text'][PS['gender'] == 'Female'])

# Create two different dataframes, one for each gender, with word count
male_word_count = word_count(male_str)
female_word_count = word_count(female_str)

# Count the number of words tweeted by each gender, which will be later used for scaling purposes
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
gender_df['count_male'] = gender_df['count_male']*100 / male_twt_count
gender_df['count_female'] = gender_df['count_female']*100 / female_twt_count

# Compute the differnce in the count of each word between males and females
# A positive number indicates words that were used more frequently by females than by males.
# A negative number indictaes the opposite
gender_df['difference'] = gender_df['count_female'] - gender_df['count_male']

# Create a gender variable for visualization purposes
gender_df['gender'] = ['Male' if diff < 0 else 'Female' for diff in gender_df['difference']]

# Initialize figure and set figure size
gen_word_diff_fig, gen_word_diff_ax = plt.subplots(1, 1)
gen_word_diff_fig.set_size_inches(12, 6.7)

# Visualize
sns.barplot(x='difference',
            y='word',
            hue='gender',
            hue_order=['Male', 'Female'],
            dodge=False,
            data=head_and_tail(gender_df.sort_values(by='difference',
                                                     ascending=False).reset_index(drop=True)))

# Slightly modify the legend
gen_word_diff_ax.legend(title='Gender',
                        loc='lower right',
                        fontsize=14,
                        title_fontsize=14)

# Add horizontal line to separate between male and women words
plt.axhline(y=19.5,
            color='black',
            linestyle='-.',
            linewidth=1.5)

# Delete axes titles
gen_word_diff_ax.set_xlabel('Difference in uses per tweet, percents', fontsize=16)
gen_word_diff_ax.set_ylabel('')

# Bigger tick labels and bigger x axis label
gen_word_diff_ax.tick_params(axis='y', which='major', labelsize=16)
gen_word_diff_ax.tick_params(axis='x', which='major', labelsize=14)

# Tight layout
gen_word_diff_fig.tight_layout()

# Show the figure
gen_word_diff_fig.show(gen_word_diff_ax)

# Export the figure
gen_word_diff_fig.savefig(r'Visualizations\Gender\Word Difference ' + printDate + '.png')


########################################            TRAFFIC BARPLOT            ########################################


# Set plotting area
gen_fig_barplot, gen_ax_barplot = plt.subplots(1, 2)
gen_fig_barplot.set_size_inches(12, 6.7)

# Favorites barplot
fav_gen_barplot = sns.barplot(x='job',
                              y='favorite_count',
                              hue='gender',
                              ax=gen_ax_barplot[0],
                              data=PS[(PS['job'] == 'Journalist') | (PS['job'] == 'Politician')])

# Set title to the gender favorites subplot
fav_gen_barplot.set_title(get_display('Likes'), fontsize=18)

# Remove the left legend
gen_ax_barplot[0].legend([], [], frameon=False)

# Retweets barplot
rt_gen_barplot = sns.barplot(x='job',
                             y='retweet_count',
                             hue='gender',
                             ax=gen_ax_barplot[1],
                             data=PS[(PS['job'] == 'Journalist') | (PS['job'] == 'Politician')])

# Set title to the gender retweets subplot
rt_gen_barplot.set_title(get_display('Retweets'), fontsize=18)

# Modify slightly the legend
gen_ax_barplot[1].legend(title='Gender',
                         fontsize=12,
                         title_fontsize=12)

# Delete subplots axes titles
for i in range(0, 2):
    gen_ax_barplot[i].set_xlabel('')
    gen_ax_barplot[i].set_ylabel('')
    gen_ax_barplot[i].tick_params(axis='both', which='major', labelsize=14)

# Tight layout
gen_fig_barplot.tight_layout()

# Show the retweets figure
gen_fig_barplot.show(gen_ax_barplot)

# Export the retweets count figure
gen_fig_barplot.savefig(r'Visualizations\Gender\Traffic Barplot ' + printDate + '.png')


########################################            TRAFFIC BOXPLOT            ########################################


BP = PS[(PS['favorite_count'] != 0) & (PS['retweet_count'] != 0)]
BP['log_favorite_count'] = np.log(BP['favorite_count'])
BP['log_retweet_count'] = np.log(BP['retweet_count'])

# Set plotting area
gen_fig_boxplot, gen_ax_boxplot = plt.subplots(1, 2)
gen_fig_boxplot.set_size_inches(12, 6.7)

# Gender favorites boxplot
fav_gen_boxplot = sns.boxplot(x='job',
                              y='log_favorite_count',
                              hue='gender',
                              showfliers=False,
                              ax=gen_ax_boxplot[0],
                              data=BP[(BP['job'] == 'Journalist') | (BP['job'] == 'Politician')])

# Remove the left legend
gen_ax_boxplot[0].legend([], [], frameon=False)

# Set title to the gender favorites subplot
fav_gen_boxplot.set_title(get_display('Likes'), fontsize=18)

# Gender retweet boxplot
rt_gen_boxplot = sns.boxplot(x='job',
                             y='log_retweet_count',
                             hue='gender',
                             showfliers=False,
                             ax=gen_ax_boxplot[1],
                             data=BP[(BP['job'] == 'Journalist') | (BP['job'] == 'Politician')])

# Set title to the gender retweets subplot
rt_gen_boxplot.set_title(get_display('Retweets'), fontsize=18)

# Delete subplots axes titles
for i in range(0, 2):
    gen_ax_boxplot[i].set_xlabel('')
    gen_ax_boxplot[i].set_ylabel('')
    gen_ax_boxplot[i].tick_params(axis='both', which='major', labelsize=14)

# Modify slightly the legend
gen_ax_boxplot[1].legend(title='Gender',
                         fontsize=12,
                         title_fontsize=12)

# Tight layout
gen_fig_boxplot.tight_layout()

# Show the retweets figure
gen_fig_boxplot.show(gen_ax_boxplot)

# Export the retweets count figure
gen_fig_boxplot.savefig(r'Visualizations\Gender\Traffic Boxplot ' + printDate + '.png')


#########################################           WORD-CHAR COUNT           #########################################


# Compute word and char count for each text
PS['word_count'] = PS['text'].apply(lambda x: len(str(x).split(" ")))
PS['char_count'] = PS['text'].apply(lambda x: sum(len(word) for word in str(x).split(" ")))

# Create plot area
gen_fig_words, gen_ax_words = plt.subplots(1, 2)

# Gender char count boxplot
sns.boxplot(x='job',
            y='char_count',
            hue='gender',
            showfliers=False,
            ax=gen_ax_words[0],
            data=PS[PS['job'].isin(['Journalist', 'Politician'])])

# Gender word count boxplot
sns.boxplot(x='job',
            y='word_count',
            hue='gender',
            showfliers=False,
            ax=gen_ax_words[1],
            data=PS[PS['job'].isin(['Journalist', 'Politician'])])

gen_fig_words.show(gen_ax_words)


#######################################            SENTIMENT ANALYSIS            #######################################


# Initialize figure area and size
gen_fig_snt, gen_fig_ax = plt.subplots()
gen_fig_snt.set_size_inches(12, 6.7)

# Plot
sns.boxplot(x='job',
            y='compound',
            hue='gender',
            # showfliers=False,
            data=PS[PS['job'].isin(['Journalist', 'Politician'])])

# Modify slightly the legend
gen_fig_ax.legend(title='Gender',
                  fontsize=14,
                  title_fontsize=14)

# Change x and y labels
gen_fig_ax.set_xlabel('')
gen_fig_ax.set_ylabel('Sentiment', size=18)
gen_fig_ax.tick_params(axis='x', which='major', labelsize=18)
gen_fig_ax.tick_params(axis='y', which='major', labelsize=12)

# Export Figure
gen_fig_snt.savefig(r'Visualizations\Gender\Sentiment Boxplot ' + printDate + '.png')

## About
This project scrapes tweets of 101 politicians, 159 journalists, 10 political parties and 21 media channels twitter accounts, and uses them to analyze several aspects of the Israeli political system. Most of the analysis was performed during the Israeli 4th consecutive election, conducted from December 20' to March 21'. 

## Motivation
The motivation behind this project is quite clear. In the last decade, politicians shifted vast majority of their election campaigns and resources to the social media. 
Journalists, although still dedicating most of their efforts to the traditional media channels, haven't stagnated and shifted much of theire activity to the social media as well.
In lights of these development and the exponential evolvement of the Natural Language Processing theory and tools, it is very interesting to analyze the way politicians and journalists behave and express themselves in the social media.

## Some Application Examples 
### *Wordclouds*
A clear, usefull and colourfull way to describe what's on the agenda is a wordcloud, which displays the words that were most commonly used during a given period of time. Each word's size indicates the number of times it was used relative to the other words. This cloud, for example, represents the agenda on the third week of the election, from 01-01-2021 to 08-01-2021. 

<p align="center">
  <img src="Visualizations/Wordclouds/Wordcloud%208-1-2021.png">
</p>

### *Popularity*
A nice way (though clearly unperfect) to check who are the most popular politicians and journalists is by checking their average number of likes and retweets per tweet. This barplot, for example, lists the top 20 politicians and journalis and the average number of likes they got in the first three weeks of the elections.

<p align="center">
  <img src="/Visualizations/Favorites/Favorites%209-1-2021.png" width="600"/>
</p>

### *Gender Relations*
The data gathered in this project is clearly most useful for politics analisys, but can be used for other purposes. An extremely important and interesting one is gender relations. This boxplot - gathering data on the ~50k tweets from the first month of the elections, reveals a huge gender gap in likes and retweets between men and women.

<p align="center">
  <img src="/Visualizations/Gender/Traffic%20Boxplot%2015-1-2021.png" width="600">
</p>

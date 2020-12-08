import pandas as pd
import numpy as np
import time
from _datetime import datetime
import tweepy
import re
import nltk
from pytz import timezone
import Credentials
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from bidi.algorithm import get_display

# Setting start and end date, to scrape tweets in between
# datetime function format is: Year, Month, Day, Hour, Minutes, Seconds, Timezone
startDate = datetime(2020, 12, 4, 20, 35, 00) # tzinfo=timezone('Israel')
endDate = datetime(2020, 12, 7, 20, 35, 00) # tzinfo=timezone('Israel')

# Creating relevant dictionaries to the scarping process
# The keys are the politician last name
# The values are lists which contain in index zero the politician @Hashtag id, and in index one it's party name
politicians_dct = {'Abou-Shahadeh': ['ShahadehAbou', 'Meshutefet'],
                   'Abutbul': ['Abutbulm', 'Shas'],
                   'Avidar': ['avidareli', 'Israel_Beytenu'],
                   'Edelstein': ['YuliEdelstein', 'Likud'],
                   'Elharrar': ['KElharrar', 'Yesh_Atid'],
                   'Alkhrumi': ['saeedalkhrumi', 'Meshutefet'],
                   'Elkin': ['zeev_elkin', 'Likud'],
                   'Amsalem': ['dudiamsalem', 'Likud'],
                   'Akunis': ['OfirAkunis', 'Likud'],
                   'Ashkenazi': ['Gabi_Ashkenazi', 'Kachol_Lavan'],
                   'Busso': ['BussoUriel', 'Shas'],
                   'Bitan': ['davidbitan', 'Likud'],
                   'Bennett': ['naftalibennett', 'Yamina'],
                   'Barbivay': ['OrnaBarb', 'Yesh_Atid'],
                   'Barak': ['KerenBarak', 'Likud'],
                   'Barkat': ['NirBarkat', 'Likud'],
                   'Golan_Yair': ['YairGolan1', 'Meretz'],
                   'Golan_May': ['GolanMay', 'Likud'],
                   'Ginzburg': ['EitanGinzburg', 'Kachol_Lavan'],
                   'Gallant': ['yoavgallant', 'Likud'],
                   'Gamliel': ['GilaGamliel', 'Likud'],
                   'Gantz': ['gantzbe', 'Kachol_Lavan'],
                   'Dayan': ['DayanUzi', 'Likud'],
                   'Dichter': ['avidichter', 'Likud'],
                   'Hauser': ['ZviHauser', 'Derech_Eretz'],
                   'Horowitz': ['NitzanHorowitz', 'Meretz'],
                   'Halevi': ['HaleviAmit', 'Likud'],
                   'Hanegbi': ['Tzachi_Hanegbi', 'Likud'],
                   'Hendel': ['YoazHendel1', 'Derech_Eretz'],
                   'Haskel': ['SharrenHaskel', 'Likud'],
                   'Cotler-Wunsh': ['CotlerWunsh', 'Kachol_Lavan'],
                   'Zohar': ['zoharm7', 'Likud'],
                   'Zamir': ['asafzamir', 'Kachol_Lavan'],
                   'Zandberg': ['tamarzandberg', 'Meretz'],
                   'Khatib-Yassin': ['khatib_eman', 'Meshutefet'],
                   'Toporovsky': ['BToporovsky', 'Yesh_Atid'],
                   'Tibi': ['Ahmad_tibi', 'Meshutefet'],
                   'Taieb': ['yossitaieb', 'Shas'],
                   'Yevarkan': ['GYevarkan', 'Likud'],
                   'Yankelevitch': ['omeryankelevitc', 'Kachol_Lavan'],
                   'Yaalon': ['bogie_yaalon', 'Yesh_Atid'],
                   'Cohen_Eli': ['elicoh1', 'Likud'],
                   'Cohen_Meir': ['MKmeircohen', 'Yesh_Atid'],
                   'Cohen_Meirav': ['cohen_meirav', 'Kachol_Lavan'],
                   'Kahana': ['MatanKahana', 'Yamina'],
                   'Kamal-Mreeh': ['GadeerMreeh', 'Yesh_Atid'],
                   'Cassif': ['ofercass', 'Meshutefet'],
                   'Katz_Ofir': ['OfirKatzMK', 'Likud'],
                   'Katz_Israel': ['Israel_katz', 'Likud'],
                   'Lahav-Hertzanu': ['YoraiLahav', 'Yesh_Atid'],
                   'Levy': ['MKMickeyLevy', 'Yesh_Atid'],
                   'Levy-Abekasis': ['Orly_levy', 'Gesher'],
                   'Liberman': ['AvigdorLiberman', 'Israel_Beytenu'],
                   'Lapid': ['yairlapid', 'Yesh_Atid'],
                   'Mark': ['OsnathilaMark', 'Likud'],
                   'Mulla': ['FateenMulla', 'Likud'],
                   'Michaeli': ['MeravMichaeli', 'Avoda'],
                   'Malinovsky': ['YuliaMalinovsky', 'Israel_Beytenu'],
                   'Malkieli': ['malkielim82', 'Shas'],
                   'Margi': ['yakmargi', 'Shas'],
                   'Nissenkorn': ['AviNissenkorn', 'Kachol_Lavan'],
                   'Netanyahu': ['netanyahu', 'Likud'],
                   'Segalovitz': ['YSegalovitz', 'Yesh_Atid'],
                   'Sova': ['evgenysova', 'Israel_Beytenu'],
                   'Sofer': ['ofir_sofer', 'Yamina'],
                   'Smotrich': ['bezalelsm', 'Yamina'],
                   'Saar': ['gidonsaar', 'Likud'],
                   'Abbas': ['mnsorabbas', 'Meshutefet'],
                   'Odeh': ['AyOdeh', 'Meshutefet'],
                   'Hava-Atia': ['ettyatia', 'Likud'],
                   'Forer': ['oded_forer', 'Israel_Beytenu'],
                   'Ploskov': ['TaliPloskov', 'Likud'],
                   'Froman': ['mkorlyfroman', 'Yesh_Atid'],
                   'Friedman': ['TehilaFriedman', 'Kachol_Lavan'],
                   'Peretz_Amir': ['amirperetz', 'Avoda'],
                   'Peretz_Rafi': ['realrafiperets', 'Bait_Yehudi'],
                   'Kushnir': ['kushnir_al', 'Israel_Beytenu'],
                   'Kisch': ['YoavKisch', 'Likud'],
                   'Kallner': ['ArielKallner', 'Likud'],
                   'Karhi': ['shlomo_karhi', 'Likud'],
                   'Regev': ['regev_miri', 'Likud'],
                   'Roll': ['idanroll', 'Yesh_Atid'],
                   'Razvozov': ['YRazvozov', 'Yesh_Atid'],
                   'Shasha-Biton': ['sbyifat', 'Likud'],
                   'Shihadeh': ['MtanesShihadeh', 'Meshutefet'],
                   'Steinitz': ['steinitz_yuval', 'Likud'],
                   'Shitrit': ['shitrit_keti', 'Likud'],
                   'Stern': ['Elazar_stern', 'Yesh_Atid'],
                   'Shay-Vazan': ['HVazan', 'Kachol_Lavan'],
                   'Shir': ['MichalShir', 'Likud'],
                   'Shelah': ['OferShelah', 'Yesh_Atid'],
                   'Shmuli': ['ishmuli', 'Avoda'],
                   'Shefa': ['ramshefa', 'Kachol_Lavan'],
                   'Shaked': ['Ayelet__Shaked', 'Yamina'],
                   'Touma-Sliman': ['AidaTuma', 'Meshutefet'],
                   'Tamano-Shata': ['pnina_tamano_sh', 'Kachol_Lavan']}

media_dct = {'Haaretz': 'Haaretz',
             'The_Marker': 'TheMarker',
             'Yediot': 'YediotAhronot',
             'Calcalist': 'calcalist',
             'Globes': 'globesnews',
             'Israel_Hayom': 'IsraelHayomHeb',
             'Maariv': 'MaarivOnline',
             'Makor_Rishon': 'MakorRishon',
             'Ynet' : 'ynetalerts',
             'Walla': 'WallaNews',
             'Mida': 'MidaWebsite',
             '7_Eye': 'the7i',
             'N12': 'N12News',
             'Reshet': 'Reshettv',
             'Kann': 'kann_news',
             'Arutz_20': 'arutz20',
             'Arutz_7': 'arutz7heb',
             'Knesset': 'KnessetT',
             'GLZ': 'GLZRadio',
             'Reshet_Bet': 'ReshetBet',
             '103FM': 'radio103fm'}

journalists_dct = {'Weiss': ['danawt', 'N12', 'Female'],        # N12
                   'Segal_Amit': ['amit_segal', 'N12', 'Male'],
                   'Nir': ['arad_nir', 'N12', 'Male'],
                   'Liel': ['DaphnaLiel', 'N12', 'Female'],
                   'Simchayoff': ['Elad_Si', 'N12', 'Male'],
                   'Cherki': ['yaircherki', 'N12', 'Male'],
                   'Avraham': ['yaronavraham', 'N12', 'Male'],
                   'Marciano': ['KerenMarc', 'N12', 'Female'],
                   'Levi': ['LeviYonit', 'N12', 'Female'],
                   'Cushmaro': ['DanyCushmaro', 'N12', 'Male'],
                   'Drucker': ['RavivDrucker', 'Reshet', 'Male'], # Reshet
                   'Kra': ['baruchikra', 'Reshet', 'Male'],
                   'Hasson': ['AyalaHasson', 'Reshet', 'Female'],
                   'Ovadia': ['sefiova', 'Reshet', 'Male'],
                   'Ben-Haim': ['AvishayBenHaim', 'Reshet', 'Male'],
                   'Glickman': ['aviadglickman', 'Reshet', 'Male'],
                   'Ish-Shalom': ['tamarishshalom', 'Reshet', 'Female'],
                   'Novick': ['akivanovick', 'Kann', 'Male'],              # Kann
                   'Lampel': ['DoriaLampel', 'Kann', 'Female'],
                   'Menashe': ['ela1949', 'Kann', 'Female'],
                   'Almog': ['almog_tamar', 'Kann', 'Female'],
                   'Amsterdamski': ['amsterdamski2', 'Kann', 'Male'],
                   'Krakovsky': ['YoavYoavkrak', 'Kann', 'Male'],
                   'Shemesh': ['shemeshmicha', 'Kann', 'Male'],
                   'Segal_Erel': ['ErelSegal', 'Arutz_20', 'Male'],    # Arutz 20
                   'Magal': ['YinonMagal', 'Arutz_20', 'Male'],
                   'Riklin': ['Riklin10', 'Arutz_20', 'Male'],
                   'Golan': ['BoazGolan', 'Arutz_20', 'Male'],
                   'Levinson': ['chaimlevinson', 'Haaretz', 'Male'],  # Haaretz
                   'Landau': ['noa_landau', 'Haaretz', 'Female'],
                   'Breiner': ['JoshBreiner', 'Haaretz', 'Male'],
                   'Tucker': ['nati_tucker', 'The_Marker', 'Male'],   # The Marker
                   'Rolnik': ['grolnik', 'The_Marker', 'Male'],
                   'Maor': ['DafnaMaor', 'The_Marker', 'Female'],
                   'Linder': ['RonnyLinder', 'The_Marker', 'Female'],
                   'Peretz_Sami': ['peretzsami', 'The_Marker', 'Male'],
                   'Avriel': ['EytanAvriel', 'The_Marker', 'Male'],
                   'Liebskind': ['KalmanLiebskind', 'Maariv', 'Male'],  # Maariv
                   'Caspit': ['BenCaspit', 'Maariv', 'Male'],
                   'Rayva-Barsky': ['AnnaBarskiy', 'Maariv', 'Female'],
                   'Eyal': ['Nadav_Eyal', 'Yediot', 'Male'],            # Yediot
                   'Shlezinger': ['judash0', 'Israel_Hayom', 'Male'],   # Israel Hayom
                   'Bismuth': ['BismuthBoaz', 'Israel_Hayom', 'Male'],
                   'Bigman': ['akibigman', 'Israel_Hayom', 'Male'],
                   'Tuchfeld': ['tuchfeld', 'Israel_Hayom', 'Male'],
                   'Kahana_Ariel': ['arik3000', 'Israel_Hayom', 'Male'],
                   'Allon': ['gideonallon', 'Israel_Hayom', 'Male'],
                   'Zwick': ['giladzw', 'Israel_Hayom', 'Male'],
                   'Segal_Haggai': ['haggai_segal', 'Makor_Rishon', 'Male'], # Makor Rishon
                   'Schnabel': ['ariel_schnabel', 'Makor_Rishon', 'Male'],
                   'German': ['ataragerman1', 'Makor_Rishon', 'Female'],
                   'Ifrach': ['yehuday30', 'Makor_Rishon', 'Male'],
                   'Goldclang': ['orlygogo', 'Makor_Rishon', 'Female'],
                   'Grinzaig': ['avishaigrinzaig', 'Globes', 'Male'],        # Globes
                   'Schneider': ['talschneider', 'Globes', 'Female'],
                   'Avitan-Cohen': ['Shiritc', 'Globes', 'Female'],
                   'Neubach': ['kereneubach', 'Reshet_Bet', 'Female'],       # Reshet Bet
                   'Lieberman': ['asaf_lib', 'Reshet_Bet', 'Male'],
                   'Kam': ['ZeevKam', 'Reshet_Bet', 'Male'],
                   'Shnerb': ['IshayShnerb', 'Galatz', 'Male'],              # Galatz
                   'Shtaif': ['hadasshtaif', 'Galatz', 'Female'],
                   'Shalev': ['talshalev1', 'Walla', 'Female'],              # Walla
                   'Ravid': ['BarakRavid', 'Walla', 'Male'],
                   'Nahari': ['OrenNahari', 'Walla', 'Male'],
                   'Adamker': ['YakiAdamker', 'Walla', 'Male'],
                   'Somfalvi': ['attilus', 'Ynet', 'Male']}                   # Ynet

# Setting the necessary twitter developer credentials to use the tweepy package and scrape tweets
# These are set as environment variables
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Create a dataframe in which the tweets will be stored
Tweets = pd.DataFrame()

# Iterate through the politicians twitter users and scrape each user tweets
# Code credit to Alexander Psiuk at https://gist.github.com/alexdeloy
# and Martin Beck at https://towardsdatascience.com/how-to-scrape-tweets-from-twitter-59287e20f0f1
for politician in politicians_dct.keys():
    username = politicians_dct[politician][0]
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
        tweets_list = [[politician,
                        politicians_dct[politician][1],
                        tweet.created_at,
                        tweet.id,
                        # tweet.quote_count,
                        # tweet.reply_count,
                        # tweet.retweet_count,
                        # tweet.favorite_count,
                        # tweet.in_reply_to_screen_name,
                        # tweet.is_quote_status,
                        # tweet.quoted_status,
                        tweet.text] for tweet in tweets]

        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list)
        Tweets = pd.concat([Tweets, tweets_df])
    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)

# Change Tweets df column names
Tweets = Tweets.rename(columns={0: 'politician',
                                1: 'party',
                                2: 'created_at',
                                3: 'id',
                                4: 'text'})

# Reset index
Tweets = Tweets.reset_index(drop=True)

# Text Preprocessing

# Delete all urls from the strings, which are almost solely used to retweet
Tweets['text'] = [re.sub(r'http\S+', "", txt) for txt in Tweets['text']]

# Delete punctuation
Tweets['text'] = [re.sub(r'[^\w\s]', '', str(txt).lower().strip()) for txt in Tweets['text']]

# Tokenize
Tweets['text'] = [txt.split() for txt in Tweets['text']]

# Delete stopwords

# Load the Mila Institute hebrew words dataset
stopwords_df = pd.read_excel(r'Mila - Stopwords.xlsx')

# Define the types of words we wand to delete from the texts and pass them to a list
delete_lst = ['conjunction', 'preposition', 'negation', 'pronoun', 'copula']
stopwords_lst = stopwords_df['Undotted'][stopwords_df['POS'].isin(delete_lst)].tolist()

# Delete
for txt in Tweets['text']:
    [txt.remove(word) for word in txt if word in stopwords_lst]

# Untokenize
for i in Tweets.index.values.tolist():
    Tweets['text'][i] = ' '.join(Tweets['text'][i])

# Now, we'll create several dataframes with the groupby function, each of them grouping the tweets along
# different aspect. This will allow us to create different wordclouds to analyze different aspects
system_df = ' '.join(txt for txt in Tweets.text)
politician_df = Tweets.groupby(['politician'], as_index=False).agg({'text': ' '.join})
party_df = Tweets.groupby(['party'], as_index=False).agg({'text': ' '.join})


# Creating the wordclouds
# bidi_text = get_display(system_df)
# wordcloud = WordCloud().generate(bidi_text)
#
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()

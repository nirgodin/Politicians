import pandas as pd
import numpy as np
import time
import tweepy
import Credentials

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
                   'Netanyahu': ['netanyahu', 'Likud']
                   'Segalovitz': ['YSegalovitz', 'Yesh_Atid'],
                   'Sova': ['evgenysova', 'Israel_Beytenu'],
                   'Sofer': ['ofir_sofer', 'Yamina'],
                   'Smotrich': ['bezalelsm', 'Yamina'],
                   'Saar': ['gidonsaar', 'Likud']
                   }

# No Twitter

# Yinon Azoulay
# Israel Eichler - Yahadut Hatora
# Moshe Arbel
# Yaakov Asher
# Ram ben barak
# Baruchi Eliyahu
# Youssef Jabarin
# Moshe Gafni - Yahadut Hatora
# Walid Taha
# Yaakov Tesler
# Hiba Yazbak
# Yitzchak Cohen
# Chaim Katz - Likud
# Yariv Levin - Likud
# Yaakov Litzman - Yahadut Hatora
# Nahari Meshulam
# Salah Sondus - Meshutefet
# Saadi Ossama - Meshutefet

# Maybe not official twitter

# Saeed Alkhrumi
# Ofir Akunis
# Keren Barak
# Eitan Ginzburg
# Uzi Dayan
# Avi Dichter
# Eman Khatib - Yassin
# Boaz Toporovsky
# Meir Cohen
# Ofer Cassif
# Fateen Mulla
# Yulia Malinovsky
# Michael Malkieli
# Yakov Margi
# yoav segalovitz
# Evgeny Sova

# Setting the necessary twitter developer credentials to use the tweepy package and scrape tweets
# These are set as environment variables
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Iterate through the politicians twitter users and scrape each user tweets
Tweets = pd.DataFrame(columns=['politician', 'party', 'created_at', 'id', 'text'])

for politician in politicians_dct.keys():
    username = politicians_dct[politician][0]
    count = 150
    try:
        # Creation of query method using parameters
        tweets = tweepy.Cursor(api.user_timeline, id=username).items(count)

        # Pulling information from tweets iterable object
        tweets_list = [[politician, politicians_dct[politician][1], tweet.created_at, tweet.id, tweet.text] for tweet in tweets]

        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list)
        Tweets = Tweets.append(tweets_df)
    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)



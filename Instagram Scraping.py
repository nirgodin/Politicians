from Credentials import mail, password
from instagramy import InstagramUser
import instagramy

def instush_df(dct):
    # Import relevant libraries
    import pandas as pd
    from instagramy import InstagramUser

    # Empty dataframe to append the scraped data
    Posts = pd.DataFrame()

    for user in dct.keys():
        username = InstagramUser(dct[user][0])
        posts = username.posts
        posts_lst = [[user,
                     dct[user][1],
                     dct[user][2],
                     dct[user][3],
                     posts[i]['timestamp'],
                     posts[i]['shortcode'],
                     posts[i]['likes'],
                     posts[i]['comments'],
                     posts[i]['caption'],
                     posts[i]['is_video'],
                     posts[i]['location']] for i in range(0, len(posts))]

        posts_df = pd.DataFrame(posts_lst)
        Posts = pd.concat([Posts, posts_df])

    # Change column names
    Posts = Posts.rename(columns={0: 'name',
                                  1: 'organization',
                                  2: 'gender',
                                  3: 'hebrew_name',
                                  4: 'timestamp',
                                  5: 'shortcode',
                                  6: 'likes_count',
                                  7: 'comments_count',
                                  8: 'caption',
                                  9: 'video',
                                  10: 'location'})

    return Posts


politicians_dct = {'Abutbul': ['mkabutbulmoshe', 'Shas', 'Male', 'אבוטבול'],
                   'Avidar': ['eavidar', 'Israel_Beytenu', 'Male', 'אבידר'],
                   'Edelstein': ['yuli.edelstein', 'Likud', 'Male', 'אדלשטיין'],
                   'Elharrar': ['karinel09', 'Yesh_Atid', 'Female', 'אלהרר'],
                   'Alkhrumi': ['saeed.alkhrumi', 'Meshutefet', 'Male', 'אלחרומי'],
                   'Elkin': ['zeev_elkin', 'Tikva_Chadasha', 'Male', 'אלקין'],
                   'Amsalem': ['amsalemdudi', 'Likud', 'Male', 'אמסלם'],
                   'Akunis': ['ofir_akunis', 'Likud', 'Male', 'אקוניס'],
                   'Ashkenazi': ['ashkenazigabi', 'Kachol_Lavan', 'Male', 'אשכנזי'],
                   'Bitan': ['david_bitan_official', 'Likud', 'Male', 'ביטן'],
                   'Bennett': ['naftalibennett', 'Yamina', 'Male', 'בנט'],
                   'Barak': ['kerenbarak5', 'Likud', 'Female', 'ברק'],
                   'Barkat': ['nir_barkat', 'Likud', 'Male', 'ברקת'],
                   'Golan_Yair': ['golan_yair1', 'Meretz', 'Male', 'גולן יאיר'],
                   'Golan_May': ['maygolan8', 'Likud', 'Female', 'גולן מאי'],
                   'Ginzburg': ['ginzburgeitan', 'Kachol_Lavan', 'Male', 'גינזבורג'],
                   'Gallant': ['yoav.gallant', 'Likud', 'Male', 'גלנט'],
                   'Gamliel': ['gila_gamliel', 'Likud', 'Female', 'גמליאל'],
                   'Gantz': ['gantzbe', 'Kachol_Lavan', 'Male', 'גנץ'],
                   'Dayan_Uzi': ['uzi.dayan', 'Likud', 'Male', 'דיין עוזי'],
                   'Dichter': ['avi_dichter', 'Likud', 'Male', 'דיכטר'],
                   'Hauser': ['zvihauser', 'Derech_Eretz', 'Male', 'האוזר'],
                   'Horowitz': ['nitzanho', 'Meretz', 'Male', 'הורוביץ'],
                   'Halevi': ['mkamithalevi', 'Likud', 'Male', 'הלוי'],
                   'Hanegbi': ['tzachi.hanegbi', 'Likud', 'Male', 'הנגבי'],
                   'Hendel': ['yoazh', 'Derech_Eretz', 'Male', 'הנדל'],
                   'Haskel': ['sharreni', 'Tikva_Chadasha', 'Female', 'השכל']}


lala = instush_df(politicians_dct)

from instascrape import *
from selenium import webdriver
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup

# Setting driver and enteting Instagram
driver = webdriver.Chrome(r'C:\Users\nirgo\PycharmProjects\Fantasy\Browsers\chromedriver.exe')
driver.get('https://instagram.com')
sleep(5)

# Set mail and password fields
mail_field = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
pass_field = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
login = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div')

# Fill the field with the mail and password
mail_field.send_keys(mail)
pass_field.send_keys(password)

# Login by clicking
login.click()

# Continue to the real homepage by dismissing instagram suggestions
notnow1 = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')
notnow1.click()
sleep(5)
notnow2 = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[3]/button[2]')
notnow2.click()
sleep(5)


b = Profile("ron.huldai")
# pst = Post('https://www.instagram.com/p/CKMJE5hhEhC/').to_dict()
b.scrape()
posts = b.get_posts(webdriver=driver)
posts_df = pd.DataFrame([post.to_dict() for post in posts])

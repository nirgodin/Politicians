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


bibi = InstagramUser('b.netanyahu')


p = bibi.posts

# return list of dicts
posts = user.get_posts_details()

p[0]['likes']
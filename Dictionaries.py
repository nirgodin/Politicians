import numpy as np
import pandas as pd

# Creating relevant dictionaries to the scarping process
# The keys are the politician last name
# The values are lists which contain in index zero the politician @Hashtag id, and in index one it's party name
politicians_dct = {'Abou-Shahadeh': ['ShahadehAbou', 'Meshutefet', 'Male', 'אבו-שחאדה'],
                   'Abutbul': ['Abutbulm', 'Shas', 'Male', 'אבוטבול'],
                   'Avidar': ['avidareli', 'Israel_Beytenu', 'Male', 'אבידר'],
                   'Edelstein': ['YuliEdelstein', 'Likud', 'Male', 'אדלשטיין'],
                   'Elharrar': ['KElharrar', 'Yesh_Atid', 'Female', 'אלהרר'],
                   'Alkhrumi': ['saeedalkhrumi', 'Meshutefet', 'Male', 'אלחרומי'],
                   'Elkin': ['zeev_elkin', 'Tikva_Chadasha', 'Male', 'אלקין'],
                   'Amsalem': ['dudiamsalem', 'Likud', 'Male', 'אמסלם'],
                   'Akunis': ['OfirAkunis', 'Likud', 'Male', 'אקוניס'],
                   'Ashkenazi': ['Gabi_Ashkenazi', 'Kachol_Lavan', 'Male', 'אשכנזי'],
                   'Busso': ['BussoUriel', 'Shas', 'Male', 'בוסו'],
                   'Bitan': ['davidbitan', 'Likud', 'Male', 'ביטן'],
                   'Bennett': ['naftalibennett', 'Yamina', 'Male', 'בנט'],
                   'Barbivay': ['OrnaBarb', 'Yesh_Atid', 'Female', 'ברביבאי'],
                   'Barak': ['KerenBarak', 'Likud', 'Female', 'ברק'],
                   'Barkat': ['NirBarkat', 'Likud', 'Male', 'ברקת'],
                   'Golan_Yair': ['YairGolan1', 'Meretz', 'Male', 'גולן יאיר'],
                   'Golan_May': ['GolanMay', 'Likud', 'Female', 'גולן מאי'],
                   'Ginzburg': ['EitanGinzburg', 'Kachol_Lavan', 'Male', 'גינזבורג'],
                   'Gallant': ['yoavgallant', 'Likud', 'Male', 'גלנט'],
                   'Gamliel': ['GilaGamliel', 'Likud', 'Female', 'גמליאל'],
                   'Gantz': ['gantzbe', 'Kachol_Lavan', 'Male', 'גנץ'],
                   'Dayan': ['DayanUzi', 'Likud', 'Male', 'דיין'],
                   'Dichter': ['avidichter', 'Likud', 'Male', 'דיכטר'],
                   'Hauser': ['ZviHauser', 'Derech_Eretz', 'Male', 'האוזר'],
                   'Horowitz': ['NitzanHorowitz', 'Meretz', 'Male', 'הורוביץ'],
                   'Halevi': ['HaleviAmit', 'Likud', 'Male', 'הלוי'],
                   'Hanegbi': ['Tzachi_Hanegbi', 'Likud', 'Male', 'הנגבי'],
                   'Hendel': ['YoazHendel1', 'Derech_Eretz', 'Male', 'הנדל'],
                   'Haskel': ['SharrenHaskel', 'Tikva_Chadasha', 'Female', 'השכל'],
                   'Cotler-Wunsh': ['CotlerWunsh', 'Kachol_Lavan', 'Female', 'וונש'],
                   'Zohar': ['zoharm7', 'Likud', 'Male', 'זוהר'],
                   'Zamir': ['asafzamir', 'Kachol_Lavan', 'Male', 'זמיר'],
                   'Zandberg': ['tamarzandberg', 'Meretz', 'Female', 'זנדברג'],
                   'Huldai': ['Ron_Huldai', 'Haisraelim', 'Male', 'חולדאי'],
                   'Khatib-Yassin': ['khatib_eman', 'Meshutefet', 'Female', 'חטיב-יאסין'],
                   'Haimovich': ['mikihaimovich1', 'Kachol_Lavan', 'Female', 'חיימוביץ'],
                   'Toporovsky': ['BToporovsky', 'Yesh_Atid', 'Male', 'טופורובסקי'],
                   'Tibi': ['Ahmad_tibi', 'Meshutefet', 'Male', 'טיבי'],
                   'Taieb': ['yossitaieb', 'Shas', 'Male', 'טייב'],
                   'Yevarkan': ['GYevarkan', 'Likud', 'Male', 'יברקן'],
                   'Yankelevitch': ['omeryankelevitc', 'Kachol_Lavan', 'Female', 'ינקלביץ'],
                   'Yaalon': ['bogie_yaalon', 'Yesh_Atid', 'Male', 'יעלון'],
                   'Cohen_Eli': ['elicoh1', 'Likud', 'Male', 'כהן אלי'],
                   'Cohen_Meir': ['MKmeircohen', 'Yesh_Atid', 'Male', 'כהן מאיר'],
                   'Cohen_Meirav': ['cohen_meirav', 'Yesh_Atid', 'Female', 'כהן מירב'],
                   'Cohen_Roee': ['roee_cohen19', 'Tnufa', 'Male', 'כהן רועי'],
                   'Kahana': ['MatanKahana', 'Yamina', 'Male', 'כהנא'],
                   'Kamal-Mreeh': ['GadeerMreeh', 'Yesh_Atid', 'Female', 'כמאל-מריח'],
                   'Cassif': ['ofercass', 'Meshutefet', 'Male', 'כסיף'],
                   'Katz_Ofir': ['OfirKatzMK', 'Likud', 'Male', 'כץ אופיר'],
                   'Katz_Israel': ['Israel_katz', 'Likud', 'Male', 'כץ ישראל'],
                   'Lahav-Hertzanu': ['YoraiLahav', 'Yesh_Atid', 'Male', 'להר-הרצנו'],
                   'Levy': ['MKMickeyLevy', 'Yesh_Atid', 'Male', 'לוי'],
                   'Levy-Abekasis': ['Orly_levy', 'Gesher', 'Female', 'לוי-אבקסיס'],
                   'Liberman': ['AvigdorLiberman', 'Israel_Beytenu', 'Male', 'ליברמן'],
                   'Lapid': ['yairlapid', 'Yesh_Atid', 'Male', 'לפיד'],
                   'Mark': ['OsnathilaMark', 'Likud', 'Female', 'מארק'],
                   'Mulla': ['FateenMulla', 'Likud', 'Male', 'מולא'],
                   'Michaeli': ['MeravMichaeli', 'Avoda', 'Female', 'מיכאלי'],
                   'Malinovsky': ['YuliaMalinovsky', 'Israel_Beytenu', 'Female', 'מלינובסקי'],
                   'Malkieli': ['malkielim82', 'Shas', 'Male', 'מלכיאלי'],
                   'Margi': ['yakmargi', 'Shas', 'Male', 'מרגי'],
                   'Nahon': ['karineb', 'Haisraelim', 'Female', 'נהון'],
                   'Nissenkorn': ['AviNissenkorn', 'Haisraelim', 'Male', 'ניסנקורן'],
                   'Netanyahu': ['netanyahu', 'Likud', 'Male', 'נתניהו'],
                   'Segalovitz': ['YSegalovitz', 'Yesh_Atid', 'Male', 'סגלוביץ'],
                   'Sova': ['evgenysova', 'Israel_Beytenu', 'Male', 'סובה'],
                   'Sofer': ['ofir_sofer', 'Yamina', 'Male', 'סופר'],
                   'Smotrich': ['bezalelsm', 'Yamina', 'Male', 'סמוטריץ'],
                   'Saar': ['gidonsaar', 'Tikva_Chadasha', 'Male', 'סער'],
                   'Abbas': ['mnsorabbas', 'Meshutefet', 'Male', 'עבאס'],
                   'Odeh': ['AyOdeh', 'Meshutefet', 'Male', 'עודה'],
                   'Atia-Hava': ['ettyatia', 'Likud', 'Female', 'עטייה-חוה'],
                   'Forer': ['oded_forer', 'Israel_Beytenu', 'Male', 'פורר'],
                   'Ploskov': ['TaliPloskov', 'Likud', 'Female', 'פלוסקוב'],
                   'Froman': ['mkorlyfroman', 'Yesh_Atid', 'Female', 'פרומן'],
                   'Friedman': ['TehilaFriedman', 'Kachol_Lavan', 'Female', 'פרידמן'],
                   'Peretz_Amir': ['amirperetz', 'Avoda', 'Male', 'פרץ עמיר'],
                   'Peretz_Rafi': ['realrafiperets', 'Bait_Yehudi', 'Male', 'פרץ רפי'],
                   'Kushnir': ['kushnir_al', 'Israel_Beytenu', 'Male', 'קושניר'],
                   'Kisch': ['YoavKisch', 'Likud', 'Male', 'קיש'],
                   'Kallner': ['ArielKallner', 'Likud', 'Male', 'קלנר'],
                   'Karhi': ['shlomo_karhi', 'Likud', 'Male', 'קרעי'],
                   'Regev': ['regev_miri', 'Likud', 'Female', 'רגב'],
                   'Roll': ['idanroll', 'Yesh_Atid', 'Male', 'רול'],
                   'Razvozov': ['YRazvozov', 'Yesh_Atid', 'Male', 'רזבוזוב'],
                   'Shasha-Biton': ['sbyifat', 'Tikva_Chadasha', 'Female', 'שאשא-ביטון'],
                   'Shihadeh': ['MtanesShihadeh', 'Meshutefet', 'Male', 'שחאדה'],
                   'Steinitz': ['steinitz_yuval', 'Likud', 'Male', 'שטייניץ'],
                   'Shitrit': ['shitrit_keti', 'Likud', 'Female', 'שטרית'],
                   'Stern': ['Elazar_stern', 'Yesh_Atid', 'Male', 'שטרן'],
                   'Shay-Vazan': ['HVazan', 'Kachol_Lavan', 'Female', 'שי-וזאן'],
                   'Shir': ['MichalShir', 'Tikva_Chadasha', 'Female', 'שיר'],
                   'Shelah': ['OferShelah', 'Tnufa', 'Male', 'שלח'],
                   'Shmuli': ['ishmuli', 'Avoda', 'Male', 'שמולי'],
                   'Shefa': ['ramshefa', 'Kachol_Lavan', 'Male', 'שפע'],
                   'Shaked': ['Ayelet__Shaked', 'Yamina', 'Female', 'שקד'],
                   'Touma-Sliman': ['AidaTuma', 'Meshutefet', 'Female', 'תומא-סלימאן'],
                   'Tamano-Shata': ['pnina_tamano_sh', 'Kachol_Lavan', 'Female', 'תמנו-שטה'],
                   'Zelekha': ['PZelekha', 'Hacalcalit', 'Male', 'זליכה']}

parties_dct = {'Likud': ['Likud_Party', 'Likud', np.nan, 'ליכוד'],
               'Kachol_Lavan': ['Kachollavan19', 'Kachol_Lavan', np.nan, 'כחול לבן'],
               'Israel_Beytenu': ['Beytenu', 'Israel_Beytenu', np.nan, 'ישראל ביתנו'],
               'Yesh_Atid': ['YeshAtidParty', 'Yesh_Atid', np.nan, 'יש עתיד'],
               'Meretz': ['meretzparty', 'Meretz', np.nan, 'מרץ'],
               'Avoda': ['HavodaParty', 'Avoda', np.nan, 'העבודה'],
               'Bait_Yehudi': ['RealBaitYehudi', 'Bait_Yehudi', np.nan, 'הבית היהודי'],
               'Yamina': ['yeminaparty', 'Yamina', np.nan, 'ימינה'],
               'Derech_Eretz': ['dereheretz', 'Derech_Eretz', np.nan, 'דרך ארץ'],
               'Gesher': ['GesherParty', 'Gesher', np.nan, 'גשר']}

media_dct = {'Haaretz': ['Haaretz', 'Haaretz', np.nan, 'הארץ'],
             'The_Marker': ['TheMarker', 'The_Marker', np.nan, 'The Marker'],
             'Yediot': ['YediotAhronot', 'Yediot', np.nan, 'ידיעות אחרונות'],
             'Calcalist': ['calcalist', 'Calcalist', np.nan, 'כלכליסט'],
             'Globes': ['globesnews', 'Globes', np.nan, 'גלובס'],
             'Israel_Hayom': ['IsraelHayomHeb', 'Israel_Hayom', np.nan, 'ישראל היום'],
             'Maariv': ['MaarivOnline', 'Maariv', np.nan, 'מעריב'],
             'Makor_Rishon': ['MakorRishon', 'Makor_Rishon', np.nan, 'מקור ראשון'],
             'Ynet': ['ynetalerts', 'Ynet', np.nan, 'Ynet'],
             'Walla': ['WallaNews', 'Walla', np.nan, 'וואלה'],
             'Mida': ['MidaWebsite', 'Mida', np.nan, 'מידה'],
             '7_Eye': ['the7i', '7_Eye', np.nan, 'העין השביעית'],
             'N12': ['N12News', 'N12', np.nan, 'N12'],
             'Reshet': ['Reshettv', 'Reshet', np.nan, 'רשת'],
             'Kann': ['kann_news', 'Kann', np.nan, 'כאן'],
             'Arutz_20': ['arutz20', 'Arutz_20', np.nan, 'ערוץ 20'],
             'Arutz_7': ['arutz7heb', 'Arutz_7', np.nan, 'ערוץ 7'],
             'Knesset': ['KnessetT', 'Knesset', np.nan, 'ערוץ הכנסת'],
             'GLZ': ['GLZRadio', 'GLZ', 'GLZ', 'גלצ'],
             'Reshet_Bet': ['ReshetBet', 'Reshet_Bet', np.nan, 'רשת ב'],
             '103FM': ['radio103fm', '103FM', np.nan, '103FM']}

journalists_dct = {'Weiss': ['danawt', 'N12', 'Female', 'דנה וייס'],                    # N12
                   'Segal_Amit': ['amit_segal', 'N12', 'Male', 'עמית סגל'],
                   'Nir': ['arad_nir', 'N12', 'Male', 'ערד ניר'],
                   'Liel': ['DaphnaLiel', 'N12', 'Female', 'דפנה ליאל'],
                   'Simchayoff': ['Elad_Si', 'N12', 'Male', 'אלעד שימחיוף'],
                   'Cherki': ['yaircherki', 'N12', 'Male', 'יאיר שרקי'],
                   'Avraham': ['yaronavraham', 'N12', 'Male', 'ירון אברהם'],
                   'Marciano': ['KerenMarc', 'N12', 'Female', 'קרן מרציאנו'],
                   'Levi': ['LeviYonit', 'N12', 'Female', 'יונית לוי'],
                   'Cushmaro': ['DanyCushmaro', 'N12', 'Male', 'דני קושמרו'],
                   'Hemo': ['ohadh1', 'N12', 'Male', 'אוהד חמו'],
                   'Reshef': ['ReshefRafi', 'N12', 'Male', 'רפי רשף'],
                   'Dadon': ['DadonAdva', 'N12', 'Female', 'אדוה דדון'],
                   'Tvizer': ['inbartvizer', 'N12', 'Female', 'ענבר טויזר'],
                   'Duek_Amalya': ['AmalyaDuek', 'N12', 'Female', 'עמליה דואק'],
                   'Drucker': ['RavivDrucker', 'Reshet', 'Male', 'רביב דרוקר'],          # Reshet
                   'Kra': ['baruchikra', 'Reshet', 'Male', 'ברוך קרא'],
                   'Hasson_Ayala': ['AyalaHasson', 'Reshet', 'Female', 'איילה חסון'],
                   'Lieberman_Chen': ['Liberwomen', 'Reshet', 'Female', 'חן ליברמן'],
                   'Ovadia': ['sefiova', 'Reshet', 'Male', 'ספי עובדיה'],
                   'Ben-Haim': ['AvishayBenHaim', 'Reshet', 'Male', 'אבישי בן-חיים'],
                   'Glickman': ['aviadglickman', 'Reshet', 'Male', 'אביעד גליקמן'],
                   'Ish-Shalom': ['tamarishshalom', 'Reshet', 'Female', 'תמר איש-שלום'],
                   'Lerer': ['guylerer', 'Reshet', 'Male', 'גיא לרר'],
                   'Herman': ['D0ronhe', 'Reshet', 'Male', 'דורון הרמן'],
                   'Heller': ['OrHeller', 'Reshet', 'Male', 'אור הלר'],
                   'Boker': ['bokeralmog', 'Reshet', 'Male', 'אלמוג בוקר'],
                   'Kenan': ['LiorKenan', 'Reshet', 'Female', 'ליאור קינן'],
                   'Maniv': ['omrimaniv', 'Reshet', 'Male', 'עמרי מניב'],
                   'Eli_Yossi': ['Yossi_eli', 'Reshet', 'Male', 'יוסי אלי'],
                   'Shiper': ['hadarshiper', 'Reshet', 'Male', 'הדר שיפר'],
                   'Rivlin_Haim': ['LifeRivlin', 'Reshet', 'Male', 'חיים ריבלין'],
                   'Tzur': ['TzurMaor', 'Reshet', 'Male', 'מאור צור'],
                   'Novick': ['akivanovick', 'Kann', 'Male', 'עקיבא נוביק'],              # Kann
                   'Lampel': ['DoriaLampel', 'Kann', 'Female', 'דוריה למפל'],
                   'Menashe': ['ela1949', 'Kann', 'Female', 'כרמלה מנשה'],
                   'Almog': ['almog_tamar', 'Kann', 'Female', 'תמר אלמוג'],
                   'Amsterdamski': ['amsterdamski2', 'Kann', 'Male', 'שאול אמסטרדמסקי'],
                   'Krakovsky': ['YoavYoavkrak', 'Kann', 'Male', 'יואב קרקובסקי'],
                   'Shemesh_Michael': ['shemeshmicha', 'Kann', 'Male', 'מיכאל שמש'],
                   'Ben-Ovadia': ['talibo8', 'Kann', 'Female', 'טלי בן-עובדיה'],
                   'Yarkechy': ['DanaYarkechy', 'Kann', 'Female', 'דנה ירקחי'],
                   'Shickman': ['ittaishick', 'Kann', 'Male', 'איתי שיקמן'],
                   'Moshe-Fredo': ['NOFARMOS', 'Kann', 'Female', 'נופר משה-פרדו'],
                   'Berger': ['galberger', 'Kann', 'Male', 'גל ברגר'],
                   'Shapira': ['yaara_shapira', 'Kann', 'Female', 'יערה שפירא'],
                   'Kogainof': ['lirankog', 'Kann', 'Male', 'לירן כוגהינוף'],
                   'Hammerschlag': ['rubih67', 'Kann', 'Male', 'רובי המרשלג'],
                   'Pelman': ['VeredPelman', 'Kann', 'Female', 'ורד פלמן'],
                   'Reuveni': ['Nov_reuveny', 'Kann', 'Male', 'נוב ראובני'],
                   'Sharon_Roy': ['roysharon11', 'Kann', 'Male', 'רועי שרון'],
                   'Dangor': ['carmeldangor', 'Kann', 'Female', 'כרמל דנגור'],
                   'Stein': ['AmichaiStein1', 'Kann', 'Male', 'עמיחי שטיין'],
                   'Aharon': ['diklaaharon', 'Kann', 'Female', 'דקלה אהרון'],
                   'Segal_Erel': ['ErelSegal', 'Arutz_20', 'Male', 'אראל סגל'],           # Arutz 20
                   'Magal': ['YinonMagal', 'Arutz_20', 'Male', 'ינון מגל'],
                   'Riklin': ['Riklin10', 'Arutz_20', 'Male', 'שמעון ריקלין'],
                   'Golan': ['BoazGolan', 'Arutz_20', 'Male', 'בועז גולן'],
                   'Bitton-Rosen': ['BittonRosen', 'Arutz_20', 'Male', 'הלל ביטון-רוזן'],
                   'Shemesh_Lital': ['Litalsun', 'Arutz_20', 'Female', 'ליטל שמש'],
                   'Levinson': ['chaimlevinson', 'Haaretz', 'Male', 'חיים לוינסון'],      # Haaretz
                   'Landau': ['noa_landau', 'Haaretz', 'Female', 'נעה לנדאו'],
                   'Breiner': ['JoshBreiner', 'Haaretz', 'Male', 'גוש בריינר'],
                   'Hasson_Nir': ['nirhasson', 'Haaretz', 'Male', 'ניר חסון'],
                   'Lee': ['VeredLee1', 'Haaretz', 'Female', 'ורד לי'],
                   'Misgav': ['UriMisgav', 'Haaretz', 'Male', 'אורי משגב'],
                   'Peleg_Bar': ['bar_peleg', 'Haaretz', 'Male', 'בר פלג'],
                   'Rabinoviz': ['AronRabino1', 'Haaretz', 'Male', 'אהרון רבינוביץ'],
                   'Bandel': ['netaelbandel', 'Haaretz', 'Male', 'נטעאל בנדל'],
                   'Ronel': ['AsafRonel', 'Haaretz', 'Male', 'אסף רונאל'],
                   'Yaron': ['lee_yaron', 'Haaretz', 'Female', 'לי ירון'],
                   'Tucker': ['nati_tucker', 'The_Marker', 'Male', 'נתי טוקר'],           # The Marker
                   'Rolnik': ['grolnik', 'The_Marker', 'Male', 'גיא רולניק'],
                   'Maor': ['DafnaMaor', 'The_Marker', 'Female', 'דפנה מאור'],
                   'Linder': ['RonnyLinder', 'The_Marker', 'Female', 'רוני לינדר'],
                   'Peretz_Sami': ['peretzsami', 'The_Marker', 'Male', 'סמי פרץ'],
                   'Avriel': ['EytanAvriel', 'The_Marker', 'Male', 'איתן אבריאל'],
                   'Megiddo': ['GurMegiddo', 'The_Marker', 'Male', 'גור מגידו'],
                   'Ashcknasy_Bini': ['BiniAshcknasy', 'The_Marker', 'Male', 'ביני אשכנזי'],
                   'Klingbail': ['sivan_kli', 'The_Marker', 'Female', 'סיון קלינגבייל'],
                   'Sadeh': ['shukisadeh', 'The_Marker', 'Male', 'שוקי שדה'],
                   'Liebskind': ['KalmanLiebskind', 'Maariv', 'Male', 'קלמן ליבסקינד'],   # Maariv
                   'Caspit': ['BenCaspit', 'Maariv', 'Male', 'בן כספית'],
                   'Batito': ['EliavBatito', 'Maariv', 'Male', 'אליאב בטיטו'],
                   'Rayva-Barsky': ['AnnaBarskiy', 'Maariv', 'Female', 'אנה רביה-ברסקי'],
                   'Levin': ['talialin', 'Maariv', 'Female', 'טליה לוין'],
                   'Lev-Ram': ['tallevram', 'Maariv', 'Male', 'טל לב-רם'],
                   'Bender': ['arikbender', 'Maariv', 'Male', 'אריק בנדר'],
                   'Eyal': ['Nadav_Eyal', 'Yediot', 'Male', 'נדב אייל'],                  # Yediot
                   'Attali': ['attaliami', 'Yediot', 'Male', 'עמיחי אתאלי'],
                   'Karni': ['YuvalKarni', 'Yediot', 'Male', 'יובל קרני'],
                   'Yehoshua': ['YehoshuaYosi', 'Yediot', 'Male', 'יוסי יהושע'],
                   'Shechnik': ['RazShechnik', 'Yediot', 'Male', 'רז שכניק'],
                   'Eichner': ['itamareichner', 'Yediot', 'Male', 'איתמר אייכנר'],
                   'Cohen_Gilad': ['GiladCohenJR', 'Yediot', 'Male', 'גלעד כהן'],
                   'Senyor': ['SenyorEli', 'Yediot', 'Male', 'אלי סניור'],
                   'Shlezinger': ['judash0', 'Israel_Hayom', 'Male', 'יהודה שלזינגר'],    # Israel Hayom
                   'Bismuth': ['BismuthBoaz', 'Israel_Hayom', 'Male', 'בועז ביסמוט'],
                   'Bigman': ['akibigman', 'Israel_Hayom', 'Male', 'עקיבא ביגמן'],
                   'Tuchfeld': ['tuchfeld', 'Israel_Hayom', 'Male', 'מתי טוכפלד'],
                   'Kahana_Ariel': ['arik3000', 'Israel_Hayom', 'Male', 'אריאל כהנא'],
                   'Allon': ['gideonallon', 'Israel_Hayom', 'Male', 'גדעון אלון'],
                   'Zwick': ['giladzw', 'Israel_Hayom', 'Male', 'גלעד צוויק'],
                   'Limor': ['LimorYoav', 'Israel_Hayom', 'Male', 'יואב לימור'],
                   'Segal_Haggai': ['haggai_segal', 'Makor_Rishon', 'Male', 'חגי סגל'],   # Makor Rishon
                   'Schnabel': ['ariel_schnabel', 'Makor_Rishon', 'Male', 'אריאל שנבל'],
                   'German': ['ataragerman1', 'Makor_Rishon', 'Female', 'עטרה גרמן'],
                   'Ifrach': ['yehuday30', 'Makor_Rishon', 'Male', 'יהודה יפרח'],
                   'Goldclang': ['orlygogo', 'Makor_Rishon', 'Female', 'אורלי גולדקלנג'],
                   'Amir_Noam': ['noamamir74', 'Makor_Rishon', 'Male', 'נועם אמיר'],
                   'Kolman': ['batelkol', 'Makor_Rishon', 'Female', 'בתאל קולמן'],
                   'Kraus': ['yair_kraus', 'Makor_Rishon', 'Male', 'יאיר קראוס'],
                   'Grinzaig': ['avishaigrinzaig', 'Globes', 'Male', 'אבישי גרינצייג'],   # Globes
                   'Schneider': ['talschneider', 'Globes', 'Female', 'טל שניידר'],
                   'Avitan-Cohen': ['Shiritc', 'Globes', 'Female', 'שירית אביטן-כהן'],
                   'Maanit': ['chenmaanit7', 'Globes', 'Male', 'חן מענית'],
                   'Sikolar': ['naamasik', 'Globes', 'Female', 'נעמה סיקולר'],
                   'Baron': ['alonabaron', 'Globes', 'Female', 'אלונה בר-און'],
                   'Dokow': ['Gidon_Dokow', 'Globes', 'Male', 'גדעון דוקוב'],
                   'Ashkenazi_Shani': ['ShaniAshkenazi', 'Globes', 'Female', 'שני אשכנזי'],
                   'Gutman_Lior': ['GutmanLior', 'Calcalist', 'Male', 'ליאור גוטמן'],     # Calcalist
                   'Salinas': ['shaysalinas', 'Calcalist', 'Male', 'שי סלינס'],
                   'Filut': ['AdrianFilut', 'Calcalist', 'Male', 'אדריאן פילוט'],
                   'Ganon': ['tomer_ganon', 'Calcalist', 'Male', 'תומר גנון'],
                   'Ilan_Shahar': ['shaharilan', 'Calcalist', 'Male', 'שחר אילן'],
                   'Esteron': ['YoelEsteron', 'Calcalist', 'Male', 'יואל אסטרון'],
                   'Marmor': ['drormarmor', 'Calcalist', 'Male', 'דרור מרמור'],
                   'Neubach': ['kereneubach', 'Reshet_Bet', 'Female', 'קרן נויבך'],       # Reshet Bet
                   'Lieberman_Assaf': ['asaf_lib', 'Reshet_Bet', 'Male', 'אסף ליברמן'],
                   'Kam': ['ZeevKam', 'Reshet_Bet', 'Male', 'זאב קם'],
                   'Deckel': ['YaronDeckel', 'Reshet_Bet', 'Male', 'ירון דקל'],
                   'Binyamini': ['rbinyamini', 'Reshet_Bet', 'Male', 'רן בנימיני'],
                   'Perez_Esty': ['perez_esty', 'Reshet_Bet', 'Female', 'אסתי פרז'],
                   'Weinreb': ['yairweinreb', 'Reshet_Bet', 'Male', 'יאיר ויינרב'],
                   'Shnerb': ['IshayShnerb', 'Galatz', 'Male', 'ישי שנרב'],               # Galatz
                   'Shtaif': ['hadasshtaif', 'Galatz', 'Female', 'הדס שטייף'],
                   'Zror': ['RinoZror', 'Galatz', 'Male', 'רינו צרור'],
                   'Canetti': ['Sykocan', 'Galatz', 'Female', 'נורית קנטי'],
                   'Barcai': ['razibarcay', 'Galatz', 'Male', 'רזי ברקאי'],
                   'Cozin': ['yanircozin', 'Galatz', 'Male', 'יניר כוזין'],
                   'Segev': ['Segev_Yuval', 'Galatz', 'Male', 'יובל שגב'],
                   'Hauser-Tov': ['HauserTov', 'Galatz', 'Male', 'מיכאל האוזר-טוב'],
                   'Yagur': ['NivYagur', 'Galatz', 'Female', 'ניב יגור'],
                   'Erel': ['ErelYuval', 'Galatz', 'Male', 'יובל אראל'],
                   'Triger': ['efitriger', 'Galatz', 'Male', 'אפי טריגר'],
                   'Daboush': ['TsahiDaboush', 'Galatz', 'Male', 'צחי דבוש'],
                   'Asraf-Wolberg': ['moriah_asraf', 'Galatz', 'Female', 'מוריה אסרף-וולברג'],
                   'Bardugo': ['bardugojacob', 'Galatz', 'Male', 'יעקב ברדוגו'],
                   'Shalev': ['talshalev1', 'Walla', 'Female', 'טל שלו'],                  # Walla
                   'Ravid': ['BarakRavid', 'Walla', 'Male', 'ברק רביד'],
                   'Nahari': ['OrenNahari', 'Walla', 'Male', 'אורן נהרי'],
                   'Adamker': ['YakiAdamker', 'Walla', 'Male', 'יקי אדמקר'],
                   'Levi_Liran': ['liran__levi', 'Walla', 'Male', 'לירן לוי'],
                   'Somfalvi': ['attilus', 'Ynet', 'Male', 'אטילה שומפלבי'],               # Ynet
                   'Azulay': ['moran_ynet', 'Ynet', 'Female', 'מורן אזולאי'],
                   'Rimon': ['RimonRan', 'Ynet', 'Male', 'רן רימון'],
                   'Blumental': ['ItayBlumental', 'Ynet', 'Male', 'איתי בלומנטל']}



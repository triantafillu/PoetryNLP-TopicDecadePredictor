import pandas as pd
import bs4
import requests
from sklearn import preprocessing
import numpy as np
import json

topics = ['lunch', 'dance', 'teaching', 'eating', 'infidelity', 'new york city', 'reading', 'separation & divorce', 'body', 'night', 'desire', 'silence', 'photography & film', 'labor day', 'summer', 'martin luther king jr. day', 'moving', 'christmas', 'city', 'easter', 'pacifism', 'trees & flowers', 'audio & music', 'lgbtq', 'survival', 'ambition', 'birth', 'social justice', 'beauty', 'history & politics', 'oceans', 'memorial day', 'race & ethnicity', 'reading & books', 'lust', 'for children', 'autumn', 'incarceration', 'rosh hashanah', 'family', 'hanukkah', 'drugs', 'men & women', 'crime & punishment', 'gardening', 'toasts & celebrations', 'farewells & good luck', 'black history month', 'animals', 'environment', 'time', 'jealousy', 'mythology', 'school & learning', 'juneteenth', 'flowers', 'for teens', 'birds', 'regret', 'future', 'work', 'miracles', 'vanity', 'apocalypse', 'theft', 'food', 'arts & sciences', 'winter', 'anger', 'cinco de mayo', 'passover', 'independence day', 'creation', 'beginning', 'anxiety', 'infatuation & crushes', 'despair', 'language', 'disappointment & failure', 'pastoral', 'painting & sculpture', 'myth', 'realistic & complicated', 'god & the divine', "st. patrick's day", 'war', 'thought', 'nature', 'identity', 'plants', 'flight', 'aging', "father's day", 'breakfast', 'september 11', 'movies', 'new year', 'religion', 'thanksgiving', 'architecture & design', 'election day', 'storms', 'enemies', 'spirituality', 'farewell', 'inaugural', 'seas, rivers, & streams', 'health & illness', 'dreams', 'marriage', 'suffrage', 'life', 'immigration', 'innocence', 'public domain', 'politics', 'popular culture', 'self', 'spanish', 'technology', 'clothing', 'class', "women's history month", 'oblivion', 'america', 'writing', 'chanukah', 'veterans day', 'national parks', 'sports', 'rebellion', 'violence', 'loneliness', 'time & brevity', 'weather', 'translation', 'fourth of july', 'the mind', 'love', 'money', 'heartache', 'get well & recovery', 'buildings', 'doubt', 'afterlife', 'earth', 'patience', 'deception', 'halloween', 'coming of age', 'faith & doubt', 'travel', 'activities', 'happiness', 'luck', 'migration', 'nostalgia', 'slavery', 'friendship', "mother's day", 'past', 'youth', 'vacations', 'visual art', 'math', 'asian/pacific american heritage month', 'memories', 'town & country life', 'native american heritage month', 'for mom', 'underworld', 'existential', 'death', 'kwanzaa', 'theater & dance', 'yom kippur', "valentine's day", 'hispanic heritage month', 'hope', 'space', 'sex', 'relationships', 'landscapes', 'earth day', 'social commentaries', 'breakups', 'carpe diem', 'anniversary', 'living', 'old age', 'philosophy', 'horror', 'heroes', 'stars, planets, heavens', 'gratitude & apologies', 'spring', 'home', 'travels & journeys', 'turmoil', 'poetry & poets', 'humor', 'ramadan']



def scrape_topics():
    
    """ Use scraped html from poets.org to get a full list of topics"""
    
    list = """<select data-v-5b5868c7="" class="custom-select" inline="" id="__BVID__67"><option data-v-5b5868c7="" value="">
                      Themes</option><option value="851">Afterlife</option><option value="856">Aging</option><option value="861">Ambition</option><option value="866">America</option><option value="871">American Revolution</option><option value="1691">Americana</option><option value="876">Ancestry</option><option value="881">Anger</option><option value="886">Animals</option><option value="1531">Anxiety</option><option value="891">Apocalypse</option><option value="896">Audio</option><option value="901">Beauty</option><option value="906">Beginning</option><option value="911">Birds</option><option value="916">Body</option><option value="921">Brothers</option><option value="1421">Buildings</option><option value="926">Carpe Diem</option><option value="931">Cats</option><option value="936">Childhood</option><option value="941">Cities</option><option value="1908">Civil War</option><option value="946">Clothing</option><option value="951">Cooking</option><option value="956">Creation</option><option value="961">Dance</option><option value="966">Daughters</option><option value="971">Death</option><option value="1576">Deception</option><option value="976">Desire</option><option value="1536">Despair</option><option value="981">Divorce</option><option value="986">Dogs</option><option value="1581">Doubt</option><option value="991">Dreams</option><option value="996">Drinking</option><option value="1001">Drugs</option><option value="1006">Earth</option><option value="1011">Eating</option><option value="1586">Economy</option><option value="1016">Enemies</option><option value="1815">Environment</option><option value="1591">Existential</option><option value="1541">Family</option><option value="1021">Fathers</option><option value="1026">Flight</option><option value="1031">Flowers</option><option value="1566">For Children</option><option value="1036">For Mom</option><option value="1041">For Teens</option><option value="1046">Friendship</option><option value="1051">Future</option><option value="1056">Gardens</option><option value="1061">Gender</option><option value="1066">Ghosts</option><option value="1071">Gratitude</option><option value="1076">Grief</option><option value="1701">Gun Violence</option><option value="1081">Happiness</option><option value="1086">Heartache</option><option value="1091">Heroes</option><option value="1096">High School</option><option value="1101">History</option><option value="1106">Home</option><option value="1111">Hope</option><option value="1596">Humor</option><option value="1116">Identity</option><option value="1121">Illness</option><option value="1126">Immigration</option><option value="1896">Incarceration</option><option value="1131">Infidelity</option><option value="1136">Innocence</option><option value="1601">Jealousy</option><option value="1151">LGBTQ</option><option value="1141">Landscapes</option><option value="1146">Language</option><option value="1156">Loneliness</option><option value="1161">Loss</option><option value="1166">Love</option><option value="1171">Love, Contemporary</option><option value="1176">Luck</option><option value="1181">Lust</option><option value="1626">Marriage</option><option value="1606">Math</option><option value="1186">Memories</option><option value="1785">Migration</option><option value="1191">Miracles</option><option value="1546">Money</option><option value="1196">Mothers</option><option value="1201">Mourning</option><option value="1206">Movies</option><option value="1211">Moving</option><option value="1216">Music</option><option value="1221">Myth</option><option value="1736">National Parks</option><option value="1226">Nature</option><option value="1231">New York City</option><option value="1236">Night</option><option value="1611">Nostalgia</option><option value="1616">Oblivion</option><option value="1241">Oceans</option><option value="1246">Old Age</option><option value="1251">Pacifism</option><option value="1256">Parenting</option><option value="1261">Past</option><option value="1621">Pastoral</option><option value="1266">Patience</option><option value="1271">Pets</option><option value="1276">Plants</option><option value="1281">Politics</option><option value="1631">Popular Culture</option><option value="1456">Public Domain</option><option value="1286">Reading</option><option value="1291">Rebellion</option><option value="1296">Regret</option><option value="1636">Religion</option><option value="1301">Romance</option><option value="1641">Sadness</option><option value="1306">School</option><option value="1311">Science</option><option value="1316">Self</option><option value="1646">Sex</option><option value="1321">Silence</option><option value="1521">Sisters</option><option value="1909">Slavery</option><option value="1746">Social Justice</option><option value="1326">Sons</option><option value="1331">Space</option><option value="1726">Spanish</option><option value="1651">Spirituality</option><option value="1336">Sports</option><option value="1341">Storms</option><option value="1346">Suburbia</option><option value="1910">Suffrage</option><option value="1351">Survival</option><option value="1356">Teaching</option><option value="1656">Technology</option><option value="1361">Theft</option><option value="1366">Thought</option><option value="1371">Time</option><option value="1376">Tragedy</option><option value="1872">Translation</option><option value="1381">Travel</option><option value="1386">Turmoil</option><option value="1391">Underworld</option><option value="1396">Vanity</option><option value="1661">Violence</option><option value="1666">Visual Art</option><option value="1401">War</option><option value="1406">Weather</option><option value="1411">Work</option><option value="1416">Writing</option></select>"""
    
    soup = bs4.BeautifulSoup(list, 'html.parser')
    topics_html = soup.find_all('option')
    topics = []
    for topic in topics_html[1:]:
        topics.append(topic.text)
    topics = [t.lower() for t in topics]
    return topics


def encode_topics(topics):
    
    """ Encode topics and return a dictionary of topics and their codes """
    
    encoder = preprocessing.LabelEncoder()
    encoded_topics = encoder.fit_transform(topics)
    mapping = dict(zip(encoder.classes_, range(len(encoder.classes_))))
    return mapping


def encode_column(x):
    
    """ Usage: df['themes'].apply(encode_column) """
    
    themes = {'activities': 0, 'afterlife': 1, 'aging': 2, 'ambition': 3, 'america': 4, 'anger': 5, 'animals': 6, 'anniversary': 7, 'anxiety': 8, 'apocalypse': 9, 'architecture & design': 10, 'arts & sciences': 11, 'asian/pacific american heritage month': 12, 'audio & music': 13, 'autumn': 14, 'beauty': 15, 'beginning': 16, 'birds': 17, 'birth': 18, 'black history month': 19, 'body': 20, 'breakfast': 21, 'breakups': 22, 'buildings': 23, 'carpe diem': 24, 'chanukah': 25, 'christmas': 26, 'cinco de mayo': 27, 'city': 28, 'class': 29, 'clothing': 30, 'coming of age': 31, 'creation': 32, 'crime & punishment': 33, 'dance': 34, 'death': 35, 'deception': 36, 'desire': 37, 'despair': 38, 'disappointment & failure': 39, 'doubt': 40, 'dreams': 41, 'drugs': 42, 'earth': 43, 'earth day': 44, 'easter': 45, 'eating': 46, 'election day': 47, 'enemies': 48, 'environment': 49, 'existential': 50, 'faith & doubt': 51, 'family': 52, 'farewell': 53, 'farewells & good luck': 54, "father's day": 55, 'flight': 56, 'flowers': 57, 'food': 58, 'for children': 59, 'for mom': 60, 'for teens': 61, 'fourth of july': 62, 'friendship': 63, 'future': 64, 'gardening': 65, 'get well & recovery': 66, 'god & the divine': 67, 'gratitude & apologies': 68, 'halloween': 69, 'hanukkah': 70, 'happiness': 71, 'health & illness': 72, 'heartache': 73, 'heroes': 74, 'hispanic heritage month': 75, 'history & politics': 76, 'home': 77, 'hope': 78, 'horror': 79, 'humor': 80, 'identity': 81, 'immigration': 82, 'inaugural': 83, 'incarceration': 84, 'independence day': 85, 'infatuation & crushes': 86, 'infidelity': 87, 'innocence': 88, 'jealousy': 89, 'juneteenth': 90, 'kwanzaa': 91, 'labor day': 92, 'landscapes': 93, 'language': 94, 'lgbtq': 95, 'life': 96, 'living': 97, 'loneliness': 98, 'love': 99, 'luck': 100, 'lunch': 101, 'lust': 102, 'marriage': 103, 'martin luther king jr. day': 104, 'math': 105, 'memorial day': 106, 'memories': 107, 'men & women': 108, 'migration': 109, 'miracles': 110, 'money': 111, "mother's day": 112, 'movies': 113, 'moving': 114, 'myth': 115, 'mythology': 116, 'national parks': 117, 'native american heritage month': 118, 'nature': 119, 'new year': 120, 'new york city': 121, 'night': 122, 'nostalgia': 123, 'oblivion': 124, 'oceans': 125, 'old age': 126, 'pacifism': 127, 'painting & sculpture': 128, 'passover': 129, 'past': 130, 'pastoral': 131, 'patience': 132, 'philosophy': 133, 'photography & film': 134, 'plants': 135, 'poetry & poets': 136, 'politics': 137, 'popular culture': 138, 'public domain': 139, 'race & ethnicity': 140, 'ramadan': 141, 'reading': 142, 'reading & books': 143, 'realistic & complicated': 144, 'rebellion': 145, 'regret': 146, 'relationships': 147, 'religion': 148, 'rosh hashanah': 149, 'school & learning': 150, 'seas, rivers, & streams': 151, 'self': 152, 'separation & divorce': 153, 'september 11': 154, 'sex': 155, 'silence': 156, 'slavery': 157, 'social commentaries': 158, 'social justice': 159, 'space': 160, 'spanish': 161, 'spirituality': 162, 'sports': 163, 'spring': 164, "st. patrick's day": 165, 'stars, planets, heavens': 166, 'storms': 167, 'suffrage': 168, 'summer': 169, 'survival': 170, 'teaching': 171, 'technology': 172, 'thanksgiving': 173, 'the mind': 174, 'theater & dance': 175, 'theft': 176, 'thought': 177, 'time': 178, 'time & brevity': 179, 'toasts & celebrations': 180, 'town & country life': 181, 'translation': 182, 'travel': 183, 'travels & journeys': 184, 'trees & flowers': 185, 'turmoil': 186, 'underworld': 187, 'vacations': 188, "valentine's day": 189, 'vanity': 190, 'veterans day': 191, 'violence': 192, 'visual art': 193, 'war': 194, 'weather': 195, 'winter': 196, "women's history month": 197, 'work': 198, 'writing': 199, 'yom kippur': 200, 'youth': 201}
    zeros_array = np.zeros(len(themes))
    for topic in x:
        for key in themes:
            if key == topic:
                index = themes[key]
                zeros_array[index]=1
    return zeros_array


def clear_nans(df):
    """Clears dataframe from nans and empty authors and text"""
    
    df2 = df.copy()
    
    #remove rows with empty authors and text
    df2 = df2.loc[df2['text'] != '']
    
    df2 = df2.dropna(subset = ['text', 'themes'])
    
    df2['title'] = df2['title'].fillna('')
    df2['url'] = df2['url'].fillna('')
    df2['author'] = df2['author'].fillna('')
    df2['year'] = df2['year'].fillna(df2['year'].median())
    
    df2 = df2.reset_index(drop=True)
    
    
    return df2


def init_author_encoding(df):
    """Create .txt file with mapped labels"""
    
    #row to be encoded
    column = 'author'
    df2 = df.copy()
    
    #encode column with label encoder
    le = preprocessing.LabelEncoder()
    le.fit(df2[column])
    df2['author'] = le.transform(df2['author'])
    
    #write dictionary of mapped labels, method tolist() for correct json writing
    le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_).tolist()))
    with open(column+'_encoding.txt', 'w') as f:
        f.write(json.dumps(le_name_mapping))
    
    return df2


def file_author_encoding(df):
    """Read mapped previosly author labels from file create new if error"""
    
    df2 = df.copy()
    
    #read mappings from file create new if error
    try:
        with open("author_encoding.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("File not found initializign new labels file")
        df2 = init_author_encoding(df2)
        
        return df2
    
    #convert txt to dictionary
    dictionary = json.loads(contents)
    
    #apply mappings to column
    df2.author = df.author.map(dictionary)
    
    return df2

def replace_categories(x):

    """ Replace categories in order to merge dataframes """

    conditions = {'birth': ['birth & birthdays', 'birthdays', 'birth'],
                  'lgbtq': ['gender', 'gay, lesbian, queer', 'gender & sexuality', 'lgbtq', 'lgbtq pride month'],
                  'religion': ['islam', 'buddhism', 'christianity', 'judaism', 'religion', 'other religions'],
                  'war': ['war', 'world war i', 'world war ii', 'civil war', 'war & conflict'],
                  'mythology': ['mythology & folklore', 'greek & roman mythology', 'mythology',
                                'ghosts & the supernatural', 'ghosts', 'fairy-tales & legends'],
                  'love': ['romance', 'love, contemporary', 'classic love', 'love', 'first love', 'unrequited love',
                           'break-ups & vexed love', 'romantic love'],
                  'family': ['family', 'daughters', 'marriage', 'fathers', 'mothers', 'divorce', 'sisters', 'sons',
                             'family & ancestors', 'brothers', 'marriage & companionship', 'parenthood', 'weddings',
                             'ancestry', 'parenting'],
                  'america': ['america', 'american revolution', 'americana'],
                  'animals': ['animals', 'pets', 'cats', 'dogs'],
                  'food': ['eating & drinking', 'cooking', 'dinner', 'drinking'],
                  'heartache': ['sorrow & grieving', 'grief', 'sadness', 'tragedy', 'funerals', 'loss',
                                'heartache & loss', 'mourning'],
                  'arts & sciences': ['arts & sciences', 'science', 'sciences'],
                  # 'religious holiday' : ['hanukkah', 'chanukah', 'kwanzaa', 'ramadan', 'rosh hashanah', "yom kippur", "yom kippur"],
                  'school & learning': ['school', 'high school', 'graduation', 'school & learning'],
                  'city': ['cities & urban life', 'cities', 'suburbia'],
                  'money': ['economy', 'money & economics'],
                  'youth': ['childhood', 'infancy', 'youth'],
                  'violence': ['violence', 'gun violence'],
                  'september 11': ['september 11th', 'september 11'],
                  'friendship': ['friendship', 'friends & enemies'],
                  'humor': ['humor', 'humor & satire'],
                  'work': ['work', 'jobs & working'],
                  'language': ['language', 'language & linguistics'],
                  'marriage': ['weddings', 'engagement', 'marriage & companionship', 'marriage'],
                  'audio & music': ['audio', 'music'],
                  'pastoral': ['pastoral', 'landscapes & pastorals'],
                  'body': ['body', 'the body'],
                  'new year': ["new year's", 'new year'],
                  'activities': ['activities', 'sports & outdoor activities', 'indoor activities'],
                  'autumn': ['fall', 'autumn'],
                  'gardening': ['gardening', 'gardens'],
                  'gratitude & apologies': ['gratitude', 'gratitude & apologies'],
                  'old age': ['old age', 'growing old'],
                  'health & illness': ['health & illness', 'illness'],
                  'heroes': ['heroes & patriotism', 'heroes'],
                  'history & politics': ['history & politics', 'history'],
                  'home': ['home', 'home life'],
                  'life': ['life choices', 'midlife'],
                  'spirituality': ['spirituality', 'the spiritual']}

    if not isinstance(x, float) and len(x)>0:
        for i in range(len(x)):
            theme = x[i]
            for k,v in conditions.items():
                if theme in v:
                    x[i] = k
                    

def merge_themes_occasions(df):

    """ Megre themes and occasions columns in df"""

    for index, row in df.iterrows():
        oc = row['occasions']
        themes = row['themes']

        if not isinstance(oc, float) and not isinstance(themes, float) and len(oc) > 0:
            for o in oc:
                themes.append(o)
        elif not isinstance(oc, float) and isinstance(themes, float):
            row['themes'] = oc

    return df.drop('occasions', 1)


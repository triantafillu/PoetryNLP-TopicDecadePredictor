import pandas as pd
import bs4
import requests
from sklearn import preprocessing
import numpy as np
import json

topics = ['plants', 'movies', 'language & linguistics', 'reading & books', 'animals', 'myth', 'architecture & design', 'migration', 'memories', 'immigration', 'underworld', 'weather', 'halloween', 'death', 'hispanic heritage month', 'rebellion', 'race & ethnicity', 'gardening', 'faith & doubt', 'infatuation & crushes', 'carpe diem', 'work', 'cinco de mayo', 'for children', 'luck', 'for mom', 'heartache', 'environment', 'get well & recovery', 'writing', 'love, contemporary', 'hope', 'slavery', 'despair', 'old age', 'miracles', 'farewell', 'new york city', 'dance', 'lunch', 'apocalypse', 'city', 'black history month', 'nature', 'oceans', 'silence', 'thought', 'aging', 'martin luther king jr. day', 'turmoil', 'survival', 'afterlife', 'labor day', "valentine's day", 'drugs', 'humor', 'independence day', 'eating', 'birth', 'music', 'regret', 'god & the divine', 'sports & outdoor activities', 'incarceration', 'breakfast', 'fourth of july', 'friendship', 'earth', 'enemies', 'existential', 'inaugural', 'happiness', 'identity', 'war', 'town & country life', 'night', 'asian/pacific american heritage month', 'home life', 'spirituality', 'vanity', 'gratitude & apologies', 'disappointment & failure', 'visual art', 'infidelity', 'history', 'reading', 'painting & sculpture', 'sorrow & grieving', 'coming of age', 'travel', 'activities', 'midlife', 'violence', 'flight', 'national parks', 'earth day', 'new year', 'clothing', 'time', 'romance', 'living', 'growing old', 'oblivion', 'birds', 'home', 'theater & dance', 'classic love', 'jealousy', 'the mind', 'past', 'theft', 'language', 'realistic & complicated', 'doubt', 'self', 'poetry & poets', 'teaching', "mother's day", 'creation', 'social justice', 'trees & flowers', 'nostalgia', 'men & women', 'engagement', 'the spiritual', 'pacifism', 'native american heritage month', 'space', 'food', 'future', 'toasts & celebrations', 'travels & journeys', 'public domain', "father's day", 'landscapes', 'storms', 'separation & divorce', 'horror', 'deception', 'health & illness', 'lgbtq', 'photography & film', 'family', 'stars, planets, heavens', 'buildings', 'beauty', 'mythology', 'thanksgiving', 'innocence', 'moving', 'beginning', 'crime & punishment', 'philosophy', 'suffrage', 'pastoral', 'autumn', 'school & learning', "women's history month", 'life choices', 'math', 'spring', 'gratitude', 'history & politics', 'love', "st. patrick's day", 'september 11', 'audio', 'veterans day', 'flowers', 'ambition', "new year's", 'lust', 'heroes', 'desire', 'translation', 'relationships', 'indoor activities', 'anxiety', 'technology', 'seas, rivers, & streams', 'religious holiday', 'body', 'youth', 'election day', 'christmas', 'money', 'easter', 'popular culture', 'time & brevity', 'summer', 'fall', 'passover', 'illness', 'the body', 'breakups', 'class', 'sports', 'juneteenth', 'anniversary', 'heroes & patriotism', 'social commentaries', 'winter', 'sex', 'religion', 'dreams', 'gardens', 'vacations', 'farewells & good luck', 'memorial day', 'loneliness', 'patience', 'america', 'arts & sciences', 'politics', 'for teens', 'spanish', 'gender', 'landscapes & pastorals', 'anger']



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
    
    themes = {'activities': 0,
 'afterlife': 1,
 'aging': 2,
 'ambition': 3,
 'america': 4,
 'anger': 5,
 'animals': 6,
 'anniversary': 7,
 'anxiety': 8,
 'apocalypse': 9,
 'architecture & design': 10,
 'arts & sciences': 11,
 'asian/pacific american heritage month': 12,
 'audio': 13,
 'autumn': 14,
 'beauty': 15,
 'beginning': 16,
 'birds': 17,
 'birth': 18,
 'black history month': 19,
 'body': 20,
 'breakfast': 21,
 'breakups': 22,
 'buildings': 23,
 'carpe diem': 24,
 'christmas': 25,
 'cinco de mayo': 26,
 'city': 27,
 'class': 28,
 'classic love': 29,
 'clothing': 30,
 'coming of age': 31,
 'creation': 32,
 'crime & punishment': 33,
 'dance': 34,
 'death': 35,
 'deception': 36,
 'desire': 37,
 'despair': 38,
 'disappointment & failure': 39,
 'doubt': 40,
 'dreams': 41,
 'drugs': 42,
 'earth': 43,
 'earth day': 44,
 'easter': 45,
 'eating': 46,
 'election day': 47,
 'enemies': 48,
 'engagement': 49,
 'environment': 50,
 'existential': 51,
 'faith & doubt': 52,
 'fall': 53,
 'family': 54,
 'farewell': 55,
 'farewells & good luck': 56,
 "father's day": 57,
 'flight': 58,
 'flowers': 59,
 'food': 60,
 'for children': 61,
 'for mom': 62,
 'for teens': 63,
 'fourth of july': 64,
 'friendship': 65,
 'future': 66,
 'gardening': 67,
 'gardens': 68,
 'gender': 69,
 'get well & recovery': 70,
 'god & the divine': 71,
 'gratitude': 72,
 'gratitude & apologies': 73,
 'growing old': 74,
 'halloween': 75,
 'happiness': 76,
 'health & illness': 77,
 'heartache': 78,
 'heroes': 79,
 'heroes & patriotism': 80,
 'hispanic heritage month': 81,
 'history': 82,
 'history & politics': 83,
 'home': 84,
 'home life': 85,
 'hope': 86,
 'horror': 87,
 'humor': 88,
 'identity': 89,
 'illness': 90,
 'immigration': 91,
 'inaugural': 92,
 'incarceration': 93,
 'independence day': 94,
 'indoor activities': 95,
 'infatuation & crushes': 96,
 'infidelity': 97,
 'innocence': 98,
 'jealousy': 99,
 'juneteenth': 100,
 'labor day': 101,
 'landscapes': 102,
 'landscapes & pastorals': 103,
 'language': 104,
 'language & linguistics': 105,
 'lgbtq': 106,
 'life choices': 107,
 'living': 108,
 'loneliness': 109,
 'love': 110,
 'love, contemporary': 111,
 'luck': 112,
 'lunch': 113,
 'lust': 114,
 'martin luther king jr. day': 115,
 'math': 116,
 'memorial day': 117,
 'memories': 118,
 'men & women': 119,
 'midlife': 120,
 'migration': 121,
 'miracles': 122,
 'money': 123,
 "mother's day": 124,
 'movies': 125,
 'moving': 126,
 'music': 127,
 'myth': 128,
 'mythology': 129,
 'national parks': 130,
 'native american heritage month': 131,
 'nature': 132,
 'new year': 133,
 "new year's": 134,
 'new york city': 135,
 'night': 136,
 'nostalgia': 137,
 'oblivion': 138,
 'oceans': 139,
 'old age': 140,
 'pacifism': 141,
 'painting & sculpture': 142,
 'passover': 143,
 'past': 144,
 'pastoral': 145,
 'patience': 146,
 'philosophy': 147,
 'photography & film': 148,
 'plants': 149,
 'poetry & poets': 150,
 'politics': 151,
 'popular culture': 152,
 'public domain': 153,
 'race & ethnicity': 154,
 'reading': 155,
 'reading & books': 156,
 'realistic & complicated': 157,
 'rebellion': 158,
 'regret': 159,
 'relationships': 160,
 'religion': 161,
 'religious holiday': 162,
 'romance': 163,
 'school & learning': 164,
 'seas, rivers, & streams': 165,
 'self': 166,
 'separation & divorce': 167,
 'september 11': 168,
 'sex': 169,
 'silence': 170,
 'slavery': 171,
 'social commentaries': 172,
 'social justice': 173,
 'sorrow & grieving': 174,
 'space': 175,
 'spanish': 176,
 'spirituality': 177,
 'sports': 178,
 'sports & outdoor activities': 179,
 'spring': 180,
 "st. patrick's day": 181,
 'stars, planets, heavens': 182,
 'storms': 183,
 'suffrage': 184,
 'summer': 185,
 'survival': 186,
 'teaching': 187,
 'technology': 188,
 'thanksgiving': 189,
 'the body': 190,
 'the mind': 191,
 'the spiritual': 192,
 'theater & dance': 193,
 'theft': 194,
 'thought': 195,
 'time': 196,
 'time & brevity': 197,
 'toasts & celebrations': 198,
 'town & country life': 199,
 'translation': 200,
 'travel': 201,
 'travels & journeys': 202,
 'trees & flowers': 203,
 'turmoil': 204,
 'underworld': 205,
 'vacations': 206,
 "valentine's day": 207,
 'vanity': 208,
 'veterans day': 209,
 'violence': 210,
 'visual art': 211,
 'war': 212,
 'weather': 213,
 'winter': 214,
 "women's history month": 215,
 'work': 216,
 'writing': 217,
 'youth': 218}
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

    conditions = {'birth' : ['birth & birthdays', 'birthdays', 'birth'],
                  'lgbtq' : ['gay, lesbian, queer', 'gender & sexuality', 'lgbtq', 'lgbtq pride month'],
                  'religion' : ['islam', 'buddhism', 'christianity', 'judaism', 'religion', 'other religions'],
                  'war' : ['war', 'world war i', 'world war ii', 'civil war', 'war & conflict'],
                  'mythology' : ['mythology & folklore', 'greek & roman mythology', 'mythology', 'ghosts & the supernatural', 'ghosts', 'fairy-tales & legends'],
                  'love' : ['love', 'first love', 'unrequited love', 'break-ups & vexed love', 'romantic love'],
                  'family' : ['family', 'daughters', 'marriage', 'fathers', 'mothers', 'divorce', 'sisters', 'sons', 'family & ancestors', 'brothers', 'marriage & companionship', 'parenthood', 'weddings', 'ancestry', 'parenting'],
                  'america' : ['america', 'american revolution', 'americana'],
                  'animals' : ['animals', 'pets', 'cats', 'dogs'],
                  'food' : ['eating & drinking', 'cooking', 'dinner', 'drinking'],
                  'heartache' : ['grief', 'sadness', 'tragedy', 'funerals', 'loss', 'heartache & loss', 'mourning'],
                  'arts & sciences' : ['arts & sciences', 'science', 'sciences'],
                  'religious holiday' : ['hanukkah', 'chanukah', 'kwanzaa', 'ramadan', 'rosh hashanah', "yom kippur", "yom kippur"],
                  'school & learning' : ['school', 'high school', 'graduation', 'school & learning'],
                  'city' : ['cities & urban life', 'cities', 'suburbia'],
                  'money' : ['economy', 'money & economics'],
                  'youth' : ['childhood', 'infancy', 'youth'],
                  'violence' : ['violence', 'gun violence'],
                  'september 11' : ['september 11th', 'september 11'],
                  'friendship' : ['friendship', 'friends & enemies'],
                  'humor' : ['humor', 'humor & satire'],
                  'work' : ['work', 'jobs & working']}

    if not isinstance(x, float) and len(x)>0:
        for theme in x:
            for k,v in conditions.items():
                if theme in v:
                    ind = x.index(theme)
                    x[ind] = k


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


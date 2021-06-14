import pandas as pd
import bs4
import requests
from sklearn import preprocessing
import numpy as np
import json


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
    
    themes = {'afterlife': 0, 'aging': 1, 'ambition': 2, 'america': 3, 'american revolution': 4, 'americana': 5, 'ancestry': 6, 'anger': 7, 'animals': 8, 'anxiety': 9, 'apocalypse': 10, 'audio': 11, 'beauty': 12, 'beginning': 13, 'birds': 14, 'body': 15, 'brothers': 16, 'buildings': 17, 'carpe diem': 18, 'cats': 19, 'childhood': 20, 'cities': 21, 'civil war': 22, 'clothing': 23, 'cooking': 24, 'creation': 25, 'dance': 26, 'daughters': 27, 'death': 28, 'deception': 29, 'desire': 30, 'despair': 31, 'divorce': 32, 'dogs': 33, 'doubt': 34, 'dreams': 35, 'drinking': 36, 'drugs': 37, 'earth': 38, 'eating': 39, 'economy': 40, 'enemies': 41, 'environment': 42, 'existential': 43, 'family': 44, 'fathers': 45, 'flight': 46, 'flowers': 47, 'for children': 48, 'for mom': 49, 'for teens': 50, 'friendship': 51, 'future': 52, 'gardens': 53, 'gender': 54, 'ghosts': 55, 'gratitude': 56, 'grief': 57, 'gun violence': 58, 'happiness': 59, 'heartache': 60, 'heroes': 61, 'high school': 62, 'history': 63, 'home': 64, 'hope': 65, 'humor': 66, 'identity': 67, 'illness': 68, 'immigration': 69, 'incarceration': 70, 'infidelity': 71, 'innocence': 72, 'jealousy': 73, 'landscapes': 74, 'language': 75, 'lgbtq': 76, 'loneliness': 77, 'loss': 78, 'love': 79, 'love, contemporary': 80, 'luck': 81, 'lust': 82, 'marriage': 83, 'math': 84, 'memories': 85, 'migration': 86, 'miracles': 87, 'money': 88, 'mothers': 89, 'mourning': 90, 'movies': 91, 'moving': 92, 'music': 93, 'myth': 94, 'national parks': 95, 'nature': 96, 'new york city': 97, 'night': 98, 'nostalgia': 99, 'oblivion': 100, 'oceans': 101, 'old age': 102, 'pacifism': 103, 'parenting': 104, 'past': 105, 'pastoral': 106, 'patience': 107, 'pets': 108, 'plants': 109, 'politics': 110, 'popular culture': 111, 'public domain': 112, 'reading': 113, 'rebellion': 114, 'regret': 115, 'religion': 116, 'romance': 117, 'sadness': 118, 'school': 119, 'science': 120, 'self': 121, 'sex': 122, 'silence': 123, 'sisters': 124, 'slavery': 125, 'social justice': 126, 'sons': 127, 'space': 128, 'spanish': 129, 'spirituality': 130, 'sports': 131, 'storms': 132, 'suburbia': 133, 'suffrage': 134, 'survival': 135, 'teaching': 136, 'technology': 137, 'theft': 138, 'thought': 139, 'time': 140, 'tragedy': 141, 'translation': 142, 'travel': 143, 'turmoil': 144, 'underworld': 145, 'vanity': 146, 'violence': 147, 'visual art': 148, 'war': 149, 'weather': 150, 'work': 151, 'writing': 152}
    zeros_array = np.zeros(len(themes))
    for topic in x:
        for key in themes:
            if key == topic:
                index = themes[key]
                zeros_array[index]=1
    return zeros_array


def clear_nans(df):
    """Clears dataframe from nans and empty authors"""

    
    df2 = df.copy()
    
    #drop columns with most nans
    #df2 = df2.drop(columns=['forms', 'occasions'])
    #remove rows with empty authors
    df2 = df2.loc[df2['author'] != '']
    #drop rows wiht nan and reset row indices
    df2 = df2.dropna(axis=0).reset_index(drop=True)
    
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

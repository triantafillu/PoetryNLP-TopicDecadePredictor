# https://www.metrolyrics.com/pokemon-theme-lyrics-pokemon.html
import requests
import bs4

req = requests.get('https://www.metrolyrics.com/pokemon-theme-lyrics-pokemon.html')
req.raise_for_status()

file = open('raw_lyrics.txt', 'wb')
for chunk in req.iter_content(100000):
    file.write(chunk)
file.close()

soup = bs4.BeautifulSoup(req.text, 'html.parser')
lyrics_body = soup.find('div', {'class': 'lyrics-body'})
final_text = lyrics_body.find_all('p', ({'class': 'verse'}))

with open('final_lyrics.txt', 'w') as file:
    for i in final_text:
        file.write(str(i.getText()))






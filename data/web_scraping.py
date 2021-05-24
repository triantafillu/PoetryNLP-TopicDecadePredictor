import time
import json

from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

SOURCE_URL = 'https://poets.org/poems'
LOADING_PAUSE_TIME = 5 


def scrap_poems(outfile, pages=100, skip_pages = 0):
    """takes number of pages to scrap
        returns list with poems dicts"""
    
    #main window to paginate through poems list
    browser = webdriver.Firefox() 
    time.sleep(LOADING_PAUSE_TIME)
    
    browser.get(SOURCE_URL)
    time.sleep(LOADING_PAUSE_TIME)
    
    #second window to scrap poem tags and text
    poem_window = webdriver.Firefox() 
    time.sleep(LOADING_PAUSE_TIME)
    
    
    for page in range(pages):
        print('PAGE #{}'.format(page+skip_pages))
        try:
            #retrieving table with poems
            poems_table = browser.find_elements_by_tag_name('tr')
            poems_table = poems_table[1:]
            for row in poems_table:
                json.dump(get_poem(row, poem_window), outfile, indent=2)
                outfile.write(', \n')
                
            browser.find_element_by_css_selector('li.page-item:nth-child(7) > a:nth-child(1)').click()
            time.sleep(LOADING_PAUSE_TIME)
        except StaleElementReferenceException:
            browser.refresh()
            time.sleep(LOADING_PAUSE_TIME*3)

def get_poem(row, poem_window):
    """takes driver instance and table row from poems list
       returns dictionary with all poem data"""
    
    #  row processing, year appears only here
    properties = row.find_elements_by_tag_name('td')
    title = properties[0].text
    a_tag = properties[0].find_element_by_tag_name('a')
    poem_url = a_tag.get_attribute("href")
    author = properties[1].text
    if (properties[2].text):
        year = int(properties[2].text)
    else:
        year = None
    
    #  scrapping poem text and tags
    poem_window.get(poem_url)
    time.sleep(LOADING_PAUSE_TIME*2)
    poem_body = poem_window.find_element_by_class_name('poem__body')
    poem_text = "".join(
        [row.text + "\n" for row in poem_body.find_elements_by_class_name('long-line')]
        )
    
    poem = {
        'title': title,
        'author': author,
        'text': poem_text,
        'url': poem_url,
        'year': year
    }
    tags = poem_window.find_element_by_class_name('poet--aside__tags').text
    if "Forms" in tags:
        tags, forms = tuple(tags.split('Forms\n'))
        forms = forms.split('\n')
        poem['forms'] = forms
    if "Themes" in tags:
        tags, themes = tuple(tags.split('Themes\n'))
        themes = themes.split('\n')[:-1]
        poem['themes'] = themes
    if "Occasions" in tags:
        tags, occasions = tuple(tags.split('Occasions\n'))
        occasions = occasions.split('\n')[:-1]
        poem['occasions'] = occasions
        
    return poem
    

with open('result.json', 'w') as outfile:
    outfile.write('[')
    scrap_poems(outfile, 500, 11)
    outfile.write('{}]')
    
    
    


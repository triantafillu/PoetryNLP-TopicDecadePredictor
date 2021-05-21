import time
import json

from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException


SOURCE_URL = 'https://poets.org/poems'
LOADING_PAUSE_TIME = 2  


def scrap_poems(n=100):
    """takes number of pages to scrap
        returns list with poems dicts"""
    result = []
    
    #main window to paginate through poems list
    browser = webdriver.Firefox() 
    time.sleep(LOADING_PAUSE_TIME)
    
    browser.get(SOURCE_URL)
    time.sleep(LOADING_PAUSE_TIME)
    
    #second window to scrap poem tags and text
    poem_window = webdriver.Firefox() 
    time.sleep(LOADING_PAUSE_TIME)
    
    for i in range(n):
        #retrieving table with poems
        poems_table = browser.find_elements_by_tag_name('tr')
        poems_table = poems_table[1:]
        for row in poems_table:
            result.append(get_poem(row, poem_window))
        
        browser.find_element_by_css_selector('li.page-item:nth-child(7) > a:nth-child(1)').click()
        
    return result
    


def get_poem(row, poem_window):
    """takes driver instance and table row from poems list
       returns dictionary with all poem data"""
    
    #  row processing, year appears only here
    properties = row.find_elements_by_tag_name('td')
    title = properties[0].text
    a_tag = properties[0].find_element_by_tag_name('a')
    poem_url = a_tag.get_attribute("href")
    author = properties[1].text
    year = int(properties[2].text)
    
    #  scrapping poem text and tags
    poem_window.get(poem_url)
    time.sleep(LOADING_PAUSE_TIME)
    time.sleep(LOADING_PAUSE_TIME)
    poem_body = poem_window.find_element_by_class_name('poem__body')
    poem_text = "".join(
        [row.text + "\n" for row in poem_body.find_elements_by_class_name('long-line')]
        )
    
    poem = {
        'title': title,
        'author': author,
        'url': poem_url,
        'text': poem_text,
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
    
result = scrap_poems(500)
with open('result.json', 'w') as outfile:
    json.dump(result, outfile)
    
    


import time
import json

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

SOURCE_URL = 'https://poets.org/poems'
LOADING_PAUSE_TIME = 1
RETRIES = 60


def scrap_poems(outfile, pages=100, skip_pages = 0):
    """takes number of pages to scrap
        returns list with poems dicts"""
    
    #main window to paginate through poems list
    browser = webdriver.Firefox() 
    time.sleep(LOADING_PAUSE_TIME*5)
    
    browser.get(SOURCE_URL)
    time.sleep(LOADING_PAUSE_TIME*5)
    
    #second window to scrap poem tags and text
    poem_window = webdriver.Firefox() 
    time.sleep(LOADING_PAUSE_TIME)
    
    # skip pages which are already parsed
    for page in range(skip_pages):  
        for i in range(RETRIES):
            try:
                browser.find_element_by_css_selector('li.page-item:nth-child(7) > a:nth-child(1)').click()
                break
            except NoSuchElementException:
                pass
            time.sleep(LOADING_PAUSE_TIME)
        
    for page in range(pages):
        try:
            #  wait to be sure json is loaded
            time.sleep(LOADING_PAUSE_TIME*5)
            
            #  retriev table with poems
            poems_table = browser.find_elements_by_tag_name('tr')
            poems_table = poems_table[1:]
            
            #  iterate through list of poems on current page
            for row in poems_table:
                poem = get_poem(row, poem_window)
                if  poem:
                    json.dump(poem , outfile, indent=2)
                    outfile.write(',')
        
        #  if json wasn't loaded in time link to elements lost
        except StaleElementReferenceException:
            pass
            
        #  go to next page
        for i in range(RETRIES):
            try:
                browser.find_element_by_css_selector('li.page-item:nth-child(7) > a:nth-child(1)').click()
                break
            except NoSuchElementException:
                pass
            time.sleep(LOADING_PAUSE_TIME)

def get_poem(row, poem_window):
    """takes driver instance and table row from poems list
       returns dictionary with all poem data"""
    
    try:
        poem = {}
        #  process row, year appears only here
        properties = row.find_elements_by_tag_name('td')
        poem['title'] = properties[0].text
        a_tag = properties[0].find_element_by_tag_name('a')
        poem['url'] = a_tag.get_attribute("href")
        poem['author'] = properties[1].text
        if (properties[2].text):
            poem['year'] = int(properties[2].text)
        else:
            poem['year'] = None
        
        #  scrap poem text and tags
        poem_window.get(poem['url'])
        time.sleep(LOADING_PAUSE_TIME*2)
        for i in range(RETRIES):
            try:
                poem_text = poem_window.find_element_by_css_selector('.px-md-4').text
                poem['text'] = poem_text
                break
            except NoSuchElementException:
                pass
            time.sleep(LOADING_PAUSE_TIME)
        
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
    # for case when broken pages and 404 answer appears
    except NoSuchElementException:
        return None
    

with open('result.json', 'w') as outfile:
    outfile.write('[')
    scrap_poems(outfile, 1000)
    outfile.write(']')
    
    
    


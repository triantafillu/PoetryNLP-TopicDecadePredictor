#scraping poems from https://poetryarchive.org
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import re
import json


def get_title(soup):
    
    title = soup.find(class_='single-poem-title').text
    
    return title


def get_poem_text(soup):
    poem = soup.find(class_='poem-content')
    poem_text = list()
    
    text = poem.find_all("p")
    #Sometimes text of a poem can be in <div> tag
    if (len(text) == 0):
        text = poem.find_all("div")
    #Write rows of the poem in array and concatenate to get one single string
    for row in text:
        poem_text.append(row.text)
    poem_text = ' '.join(poem_text)
    
    return poem_text


def get_year(soup):
    
    year_box = soup.find(class_='source-box bg-grey pa-boxed small-text')
    
    #Search for 4 digit number in string but sometimes there might be more than 1 year but returns first found
    year = re.search(r'\b\d{4}\b', year_box.text)
    #Check if found
    if year != None:
        year = int(year.group(0))
        
    return year


def get_author(soup):
    
    sidebar = soup.find(class_='frac4 poem-sidebar')
    
    author = sidebar.find(class_='poet-name').find('h3').text
    
    return author


def get_themes(soup):
    
    sidebar = soup.find(class_='frac4 poem-sidebar')
    
    #There are multiple grey boxes with content
    tags = sidebar.findAll(class_='pa-boxed bg-grey')
    
    #Sometimes there are no grey boxes with themes, this if just for avoid error
    if ((len(tags) > 1) and (tags[1].find('h6').text == 'Themes')):
        tags = tags[1].findAll(class_='btn btn-tiny btn-meta btn-corn-solid')
    else:
        return None
    
    themes = list()
    for theme in tags:
        themes.append(theme.text)

    return themes


def get_links(url):
    
    #Site does not allow to send requests without headers, it's just random headers from the net
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    result.raise_for_status()
    
    soup = BeautifulSoup(result.content, 'html.parser')
    
    #Get all titles, they contain links
    poem_titles = soup.findAll(class_='poem-title')
    poem_links = list()
    for poem_title in poem_titles:
        poem_links.append(poem_title.find('a')['href'])
    return poem_links


def get_poem_dict(url):
    
    #Dictionary to store poem data
    poem = {}
    
    #Site does not allow to send requests without headers, it's just random headers from the net
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    result = requests.get(url, headers=headers)
    result.raise_for_status()

    soup = BeautifulSoup(result.content, 'html.parser')
    
    #Write data into dictionary
    poem['title'] = get_title(soup)
    poem['url'] = url
    poem['author'] = get_author(soup)
    poem['text'] = get_poem_text(soup)
    poem['themes'] = get_themes(soup)
    
    return(poem)


def scrap_poems(outfile, num_pages=180):
    """Function gets file to write and number of pages (182 max) and in loop
     for every page scraps data from each poem on the page and writes it into json file"""
    
    for page_num in range(num_pages):
        url = 'https://poetryarchive.org/explore/page/{}/?type=poems'.format(page_num+1)
        links = get_links(url)
        for link in links:
            poem = get_poem_dict(link)
            print(poem['title'])
            #If poem is not empty write it i
            if poem:
                json.dump(poem , outfile, indent=2)
                #Trailing coma must be remowed by hand or in program (TODO if necessary)
                outfile.write(',')
                
                
if __name__ == 'main':
    with open('result.json', 'w') as outfile:
        outfile.write('[')
        scrap_poems(outfile, 3)
        outfile.write(']')

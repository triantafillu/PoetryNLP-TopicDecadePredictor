from selenium import webdriver
import bs4
import requests
import re
import time
from random import randint
import json


def scrape_poem(url):
    """ Scrape poem information from poetryfoundation.org """

    poem_request = requests.get(url)
    poem_request.raise_for_status()

    poem_soup = bs4.BeautifulSoup(poem_request.text, 'html.parser')

    # Scrape the title
    title = poem_soup.find('h1', class_='c-hdgSans c-hdgSans_2 c-mix-hdgSans_inline')
    if title != None:
        title = title.text.strip()
    else:
        title = None

    # Scrape the author
    by_author = poem_soup.find('span', class_='c-txt c-txt_attribution')
    if by_author != None:
        author = by_author.find('a')
        if author != None:
            author = author.text.strip()
        else:
            author = None
    else:
        author = None

    # Scrape the text of poem
    lines_outer = poem_soup.find('div', {"class": "c-feature-bd"})
    if lines_outer != None:
        lines = lines_outer.find_all('div', {"style": "text-indent: -1em; padding-left: 1em;"})
        if lines != None:
            poem_text = ''
            for line in lines:
                poem_text = poem_text + line.text + '\n'
        else:
            poem_text = None
    else:
        poem_text = None

    # Scrape the year
    # Find 4 consequent digits in copyright or source using regex
    copyright_outer = poem_soup.find('div', class_='o-vr_2x')
    source_outer = poem_soup.find('div', class_='o-vr o-vr_2x')
    if copyright_outer != None:
        copyright = copyright_outer.find('span', class_="c-txt c-txt_note c-txt_note_mini")
        if copyright != None:
            year = re.findall(r'\d{4}', copyright.text)
            if len(year) > 0:
                year = year[0]
            else:
                year = None
        else:
            year = None
    elif source_outer != None:
        source = source_outer.find('span', class_='c-txt c-txt_note c-txt_note_mini')
        if source != None:
            year = re.findall(r'\d{4}', source.text)
            if len(year) > 0:
                year = year[0]
            else:
                year = None
        else:
            year = None
    else:
        year = None

    return {'title': title, 'author': author, 'text': poem_text, 'year': year}


# Counter of poems scraped
poem_counter = 0


def scrape_search(c, outfile):
    """ Scrape all the poems from search list
        c - number of search page
        outfile - json file to write the info to """

    global poem_counter

    # Open the search page
    url = 'https://www.poetryfoundation.org/poems/browse#page=' + c + '&sort_by=recently_added'
    driver = webdriver.Firefox()
    driver.get(url)

    # Find the frame with all the search results
    el_list = driver.find_elements_by_css_selector(
        '#js-assetViewport > div > div > div:nth-child(2) > div > div.o-grid-col.o-grid-col_9of12 > div.c-assetViewport.isInteractive > ol > li')

    # Scrape the poem from every search result
    for el in el_list:
        soup = bs4.BeautifulSoup(el.get_attribute('innerHTML'), 'html.parser')

        # Find the link of poem
        poem_url_html = soup.find('a')
        poem_url = poem_url_html['href']

        # Scrape the themes
        topics_frame = soup.find('span', class_='u-obscuredAfter8')
        if topics_frame != None:
            topics_html = topics_frame.find_all('a')
            themes = []
            for t in topics_html:
                if t.text != 'Appeared in Poetry Magazine':
                    themes.append(t.text.lower())
            if len(themes) == 0:
                themes = None
        else:
            themes = None

        if themes == None:
            print ('no themes')
            continue

        # Scrape poems from link
        attributes = scrape_poem(poem_url)
        attributes['url'] = poem_url
        attributes['themes'] = themes

        poem_counter = poem_counter + 1
        print(poem_counter)
        time.sleep(randint(2, 10))

        # Write info into the json file
        json.dump(attributes, outfile)
        outfile.write(',')

    # Close the tab
    driver.close()


with open('sample1.json', 'w') as outfile:
    outfile.write('[')
    for i in range(329, 500):
        scrape_search(str(i), outfile)
        print(f'page: {i}')
    outfile.write(']')
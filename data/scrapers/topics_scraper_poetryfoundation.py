from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import bs4
import re
import time
from random import randint

categories = []

def get_categories(c):

    """ Scrape topics from poetry foundation.org """

    time.sleep(randint(2, 10))
    url = 'https://www.poetryfoundation.org/poems/browse#page=1&sort_by=recently_added&topics='+c
    driver = webdriver.Firefox()
    driver.get(url)

    try:
        # Wait until page loads
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.o-site'))
        WebDriverWait(driver, 15).until(element_present)

        # Avoid exception on pages without topic
        theme_box = driver.find_element_by_css_selector('#js-assetViewport > div > div > div:nth-child(1) > div > div.c-filterPanel > div.c-filterPanel-actions > ul > li:nth-child(1) > a > div > div.u-showAboveSmall')
    except:
        print('no topic: '+ c)
    else:
        if theme_box != None:
            box_html = theme_box.get_attribute('innerHTML')
            soup = bs4.BeautifulSoup(box_html, 'html.parser')

            # General topic
            cat1 = soup.find('span', class_ = "c-filterPill")

            # Companion topic
            cat2 = soup.find('span', class_ = "c-txt c-txt_filterCompanion")

            if cat1 != None and cat1.text != "" :
                # Separate general topic from companion one
                if ':' in cat1.text.lower():
                    cat1_txt = re.findall(r'[^:]+', cat1.text.lower())[0]
                    # If category not in final list
                    if cat1_txt not in categories:
                        categories.append(cat1_txt)
                else:
                    if cat1.text.lower() not in categories:
                        categories.append(cat1.text.lower())
            if cat2 != None and cat2.text != "":
                # Delete ": " from the beginning of companion topic
                if ':' in cat2.text.lower():
                    cat2_txt = cat2.text.lower()[2:]
                    # If category not in final list
                    if cat2_txt not in categories:
                        categories.append(cat2_txt)
                else:
                    if cat2.text.lower() not in categories:
                        categories.append(cat2.text.lower())
    driver.close()

for i in range(2,150):
    get_categories(str(i))

    if i%10 == 0:
        print(categories)

print(categories)
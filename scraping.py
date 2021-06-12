#!/usr/bin/env python3

# import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import shutil
import os.path
import argparse

# import caffeine  # For keeping computer awake during process

# INITIATE THE PARSER
parser = argparse.ArgumentParser()
parser.add_argument("-D", "--dev", help="Pauses the web driver after scraping each page and provides an option to end "
                                        "the program prematurely.", action="store_true")
parser.add_argument("-T", "--time", help="Set a custom sleep time between pagination, in seconds.", action="store",
                    type=int, required=False)
parser.add_argument("-L", "--link", help="Provide an alternative link to scrape. The link must be enclosed in double "
                                         "quotes. Will only work with Uppsala Bibliotek.",
                    action="store", type=str, required=False)

# PARSE ARGUMENTS FROM THE CLI
args = parser.parse_args()

# DEVELOPMENT MODE
# activates a break option between pagination, so that a user doesn't need to wait for the entire scrape to finish
if args.dev:
    dev_mode = True
else:
    dev_mode = False

if args.time:
    nap = args.time
else:
    nap = 10

# GET LINK TO SCRAPE
if args.link:
    link = args.link
else:
    link = 'https://bibliotekuppsala.se/web/arena/search-extended?p_p_id=searchResult_WAR_arenaportlet&p_p_lifecycle' \
           '=1&p_p_state=normal&p_r_p_arena_urn%3Aarena_facet_queries=&p_r_p_arena_urn%3Aarena_search_query' \
           '=organisationId_index%3AASE100230%5C%7C10000+AND+mediaClass_index%3AvideoGame&p_r_p_arena_urn' \
           '%3Aarena_search_type=solr&p_r_p_arena_urn%3Aarena_sort_advice=field%3DRelevance%26direction%3DDescending '

# SET DRIVER AND OPTIONS
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('/Users/danny/PycharmProjects/uppsalaBibliotekTvSpelScraper/chromedriver',
                          options=chrome_options)

# INITIAL LOAD
print('Initialising web driver...')
driver.get(link)

# ALLOW FOR CRAPPY INTERNET
time.sleep(nap)

# INITIALISE LIST
titles = []

# INITIALISE PAGE NUMBER
current_page = 0

# MAIN INDEXING LOOP
repeat = True
while repeat:
    # PRINT CURRENT PAGE NUMBER TO INDICATE PROGRESS
    current_page += 1
    print("Indexing page:", current_page)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    # FIND TITLES
    title_finder = soup.find_all('div', class_="arena-record-title")

    # ITERATE THROUGH TITLES AND ADD TO LIST 'TITLES'
    for title in title_finder:
        names = title.find_all("span", class_=None)
        for name in names:
            titles.append(name.text)

    # CLICK THROUGH TO NEXT PAGE AND WAIT 10 SECONDS FOR DATA TO LOAD
    rightElement = driver.find_element_by_class_name("arena-record-right")
    rightElement.click()
    time.sleep(nap)

    # BREAK IF PAGE IS THE SAME (I.E, END OF RESULTS)
    compare = driver.page_source
    if compare == page_source:
        repeat = False

    # DURING DEVELOPMENT OPTION TO CANCEL AFTER EACH PAGE
    if dev_mode:
        indexNextPage = str(input("Continue indexing? (Y/N) "))
        if indexNextPage == "Y" or indexNextPage == "y":
            continue
        else:
            print("Indexing ended prematurely after page", current_page)
            break

# QUIT DRIVER ON COMPLETION
driver.quit()

# COPY ORIGINAL LIBRARY.TXT FILE
file_exists = os.path.isfile("Library.txt")

if file_exists:
    shutil.copyfile('Library.txt', 'Library_temp.txt')
else:
    file = open("Library.txt", "w")
    file.close()
    shutil.copyfile('Library.txt', 'Library_temp.txt')

# WRITE LIST TO TEXT FILE
text_file = open("Library.txt", "w")
for title in titles:
    text_file.write(title + "\n")
text_file.close()

# COMPARE FILE TO COPY
originalFile = open("Library.txt", "r")
latestFile = open("Library_temp.txt", "r")
li1 = originalFile.read().splitlines()  # Previous version of list
li2 = latestFile.read().splitlines()  # Current version of list
li3 = [i for i in li1 + li2 if i not in li1 or i not in li2]  # All changes
# li4 = Titles added (IN li2 and NOT IN li1)
# li5 = Titles removed (IN li1 and NOT IN li2)

# REMOVE TEMP FILE
os.remove('Library_temp.txt')

# IF DIFFERENT, STATE DIFFERENCE
if not li3:
    print("Nothing new found")
else:
    print("New titles found:")
    for title in li3:
        print(title)

print("Scrape completed!")

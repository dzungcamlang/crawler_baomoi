from bs4 import BeautifulSoup
import os, os.path
from urllib.request import urlopen as uReg
import multiprocessing
import requests
urlTest = 'https://baomoi.com/a/c/12222212.epi'
indexTest = 12222212

def count_file():
    DIR = 'data/'
    fileCount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    print(fileCount)

def get_title(indexChosen):
    link = 'https://baomoi.com/a/c/' + str(indexChosen) + '.epi'
    uClient = requests.get(link)
    # print(uClient.content)
    page_html = uClient.content
    soup = BeautifulSoup(page_html, 'html.parser')
    # print(soup)
    # soup = BeautifulSoup(page_html.decode('utf-8'))
    new_feeds = soup.find_all("h1")
    if len(new_feeds) == 0:
        # print(page_html)
        return
    print(link)
    # if indexChosen % 50 == 0:
        # print(link)
    count_file()
    source = soup.find("a", {"class": "source"}).text
    print(source)
    for new in new_feeds:
        if len(new.text) > 0:
            with open('data/' + str(indexChosen) + '.txt', 'w') as f:
                f.write(new.text)
    tagsHtmlList = soup.find_all('a', {'class': 'keyword'})
    print(tagsHtmlList)
# req = requests.get(url)
# with multiprocessing.Pool(processes=5) as pool:
#     arr = range(11111111,11151111)
#     pool.map(get_title, arr)
# print(fileCount)
# for i in range(11111111,77777777):
#     urlChosen = 'https://baomoi.com/a/c/' + str(i) + '.epi'
#     if get_title(indexChosen):
#         count = count + 1
#         print('count: ', count)
#     if count > 20000: break
get_title(indexTest)
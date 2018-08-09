import asyncio

import os, os.path
import aiohttp
from bs4 import BeautifulSoup

import logging

def check_404(soup):
    titles = soup.find_all("h1")
    if len(titles) == 0:
        return True
    return False

def find_objects(soup):
    titles = soup.find_all("h1")
    for t in titles:
        if len(t.text) > 0:
            # print(new.text)
            title = t.text
    source = soup.find("a", {"class": "source"}).text
    tagsHtmlList = soup.find_all("div", {"class": "article__tag"},'a', {'class': 'keyword'})
    tags = ','.join(list(map(lambda h: h.text, tagsHtmlList)))

    return title, source, tags

class AsnycGrab(object):

    def __init__(self, index_list, max_threads):

        self.indexs = index_list
        # self.results = {}
        self.max_threads = max_threads

    def write_text(self, title, source, tags, indexChosen):
        with open('data/' + str(indexChosen) + '.txt', 'w') as f:
            f.write(title + '\n' + source + '\n' + tags)

    def count_file(self):
        DIR = 'data/'
        fileCount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        print(fileCount)

    def __parse_results(self, url, html, index):

        try:
            soup = BeautifulSoup(html, 'html.parser')
            # print(url)
            title = None
            if not check_404(soup):
                title, source, tags = find_objects(soup)
        except Exception as e:
            raise e

        if title:
            # print(index)
            self.write_text(title, source, tags, index)
            self.count_file()

    async def get_body(self, index):
        url = 'https://baomoi.com/a/c/' + str(index) + '.epi'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                assert response.status == 200
                html = await response.read()
                return response.url, html

    async def get_results(self, index):
        url, html = await self.get_body(index)
        self.__parse_results(url, html, index)
        return 'Completed'

    async def handle_tasks(self, task_id, work_queue):
        while not work_queue.empty():
            current_index = await work_queue.get()
            try:
                task_status = await self.get_results(current_index)
            except Exception as e:
                logging.exception('Error for {}'.format(current_index),exc_info=True)

    def eventloop(self):
        q = asyncio.Queue()
        # urls = list(map(lambda index: 'https://baomoi.com/a/c/' + str(index) + '.epi', self.indexs))
        [q.put_nowait(index) for index in self.indexs]
        loop = asyncio.get_event_loop()
        tasks = [self.handle_tasks(task_id, q, ) for task_id in range(self.max_threads)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

def count_file():
    DIR = 'data/'
    fileCount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    return fileCount

def asyncCraw(indexList):
    async_example = AsnycGrab(indexList, 5)
    async_example.eventloop()

if __name__ == '__main__':
    testResults = []
    # for i in range(0, 300):
    #     indexList = range(11111111 + i * 100, 11111111 + (i+1) * 100 )
    # fileCount = 0
    # indexJump = 0
    # while fileCount < 20000:
    # print(fileCount)
    # indexList = range(11111111 + indexJump, 11111211 + indexJump)
    indexList = range(11111111, 11136111)
    async_example = AsnycGrab(indexList, 5)
    async_example.eventloop()
    # fileCount = count_file()
    # indexJump = indexJump + 1

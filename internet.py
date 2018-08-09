from bs4 import BeautifulSoup
import urllib.request

url =  'https://vnexpress.net'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

new_feeds = soup.find(
	'section', class_='featured container clearfix').find_all('a')

for feed in new_feeds:
	title = feed.get('title')
	link = feed.get('href')
	print('Title: {} - Link: {}'.format(title, link))

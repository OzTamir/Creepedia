from bs4 import BeautifulSoup as bs
from urllib import urlopen

class WikiParse:
    def __init__(self, url):
        self.url  = url
        self.html = urlopen(self.url).read()
        self.soup = bs(self.html)
    def parseTitle(self):
        title = bs(str(self.soup.find('h1', {'id': 'firstHeading'})))
        title = title.findAll('span')[0]
        title = title.text
        if len(title) == 0:
            return 'TITLE MISSING'
        return str(title)

    def parseImage(self):
        image = bs(str(self.soup.find('a', {'class': 'image'})))
        image = image.findAll('img')[0].get('src')
        return str(image)

class articleParse:
    def __init__(self, url):
        self.url = url
        article = WikiParse(self.url)
        self.title = article.parseTitle()
        self.image = article.parseImage()
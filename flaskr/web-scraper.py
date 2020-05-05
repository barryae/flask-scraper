import sys as sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

query = sys.argv[1]
scrapeFormat = sys.argv[2]


def getHTMLContent(link):
    html = urlopen(link)
    soup = BeautifulSoup(html, 'html.parser')
    return soup


content = getHTMLContent('https://en.wikipedia.org/wiki/'+query)
paragraphs = content.find_all('p')

for p in paragraphs:
    if scrapeFormat == 'html':
        print(p)
    if scrapeFormat == 'plain':
        response = p.getText()
        print(response)

sys.stdout.flush()

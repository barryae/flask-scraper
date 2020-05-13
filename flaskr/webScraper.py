import sys as sys
from urllib.request import urlopen
from bs4 import BeautifulSoup


def getHTMLContent(link):
    html = urlopen(link)
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def scrape(searchWord):
    content = getHTMLContent('https://en.wikipedia.org/wiki/'+searchWord)
    paragraphs = content.find_all('p')
    results = ''
    for p in paragraphs:
        results += p.getText()
        # if analysisType == 'html':
        #     return p
        # if analysisType == 'plain':
        #     response += p.getText()
        #     return response

    return results

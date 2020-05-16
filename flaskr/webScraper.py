import sys as sys
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup


def getHTMLContent(link):
    html = urlopen(link)
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def scrape(searchWord, analysisType):
    content = getHTMLContent('https://en.wikipedia.org/wiki/'+searchWord)
    paragraphs = content.find_all('p')
    results = ''

    if analysisType == 'Plain Text':
        for p in paragraphs:
            results += p.getText()

    elif analysisType == 'Vocab List':
        for p in paragraphs:
            results += p.getText()
        words = set(nltk.word_tokenize(results))
        words = sorted([word.lower() for word in words if word.isalpha()])
        results = ", ".join(words)

    return results

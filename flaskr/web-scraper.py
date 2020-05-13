import sys as sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
bp = Blueprint('scrape', __name__, url_prefix='/scrape')

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

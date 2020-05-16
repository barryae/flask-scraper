# flask-scraper

A web scraper using Flask!

## Goals

- Create a beautiful app that scrapes, analyzes, and stores text data from the web
- Leverage Flask and Python in general to create a secure and reliable web app
- Integrate Prosemirror text editor that gives realtime analysis of text being written.

## Outline of Development

- Create HTML template for search input
- Connect web-scraper.py to HTML
- Create NLTK functionality that analyzes search results
- Implement search, search results, and search analysis results being created in database

## Technology Used

- Python
- Flask
- NLTK
- HTML
- CSS
- JavaScript
- SQLite3

## Steps to develop

Create an environment, activate it, and install Flask:

<https://flask.palletsprojects.com/en/1.1.x/installation/>

While in venv also install nltk & bs4:

```bash
pip install nltk bs4
```

When you want to develop:

```bash

. venv/bin/activate

export FLASK_APP=flaskr

export FLASK_ENV=development

flask run
```

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
from flaskr.webScraper import scrape
bp = Blueprint('', __name__, url_prefix='/')
results = ''


@bp.route('/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        searchWord = request.form['searchWord']
        analysisType = request.form['format']
        print(analysisType)
        db = get_db()
        error = None
        alreadySearched = db.execute(
            'SELECT id, search_word FROM search WHERE search_word = ?', (
                searchWord,)
        ).fetchone()
        searchedAndAnalyzed = None

        if alreadySearched is not None:
            searchedAndAnalyzed = db.execute(
                'SELECT id, body FROM analysis WHERE search_id = ? AND analysis_type = ?', (
                    alreadySearched['id'], analysisType)
            ).fetchone()

        if not searchWord:
            error = 'Please put in a word to scrape.'
        elif not analysisType:
            error = 'Analysis type not set.'

        if searchedAndAnalyzed is not None:
            results = searchedAndAnalyzed['body']

            return render(results, searchWord, analysisType)

        if error is None:
            # scrape using code from web-scraper.py
            body = scrape(searchWord, analysisType)
            # save scrape results in db
            if alreadySearched is None:
                db.execute(
                    'INSERT INTO search (search_word) VALUES (?)',
                    (searchWord,)
                )
                db.commit()

            search_id = db.execute(
                'SELECT id FROM search WHERE search_word = ?', (
                    searchWord,)
            ).fetchone()

            db.execute(
                'INSERT INTO analysis (search_id, analysis_type, body) VALUES (?,?,?)',
                (search_id['id'], analysisType, body)
            )
            db.commit()

            results = body

            return render(results, searchWord, analysisType)

        flash(error)

    return render(results, searchWord, analysisType)


def render(results, searchWord, analysisType):
    return render_template('./scraper/scraper.html',
                           results=results, search=searchWord, analysisType=analysisType)

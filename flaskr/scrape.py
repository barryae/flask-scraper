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
        db = get_db()
        error = None
        alreadySearched = db.execute(
            'SELECT id, search_word FROM search WHERE search_word = ?', (
                searchWord,)
        ).fetchone()

        if not searchWord:
            error = 'Please put in a word to scrape.'
        elif not analysisType:
            error = 'Analysis type not set.'

        if alreadySearched is not None:
            analysis = db.execute(
                'SELECT id, body FROM analysis WHERE search_id = ?', (
                    alreadySearched['id'],)
            ).fetchone()

            results = analysis['body']

            return render_template('./scraper/scraper.html', results=results)

        if error is None:
            # scrape using code from web-scraper.py
            body = scrape(searchWord)
            # save scrape results in db
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
            return render_template('./scraper/scraper.html', results=results)

        flash(error)

    return render_template('./scraper/scraper.html', results=results)

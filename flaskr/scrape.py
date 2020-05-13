import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
bp = Blueprint('scrape', __name__, url_prefix='/scrape')


@bp.route('/wikipedia', methods=('GET', 'POST'))
def scrapeWikipedia():
    if request.method == 'POST':
        searchWord = request.form['searchWord']
        option = request.form['format']
        db = get_db()
        error = None
        alreadySearched = db.execute(
            'SELECT id, body FROM analysis WHERE search_id = ? AND analysis_type= ?', (
                alreadySearched, option)
        ).fetchone()

        if not searchWord:
            error = 'Please put in a word to scrape.'
        elif not option:
            error = 'Analysis type not set.'

        if alreadySearched is not None:
            session.clear()
            g.results = alreadySearched['body']
            return render_template('./scraper/scraper.html')
            # return search to client

        if error is None:
            # scrape using code from web-scraper.py
            body = 'scrape results'
            # save scrape results in db
            db.execute(
                'INSERT INTO search (search_word) VALUES (?)',
                (searchWord)
            )
            search_id = db.execute(
                'SELECT id FROM search WHERE search_word = ?', (searchWord,)
            )
            db.execute(
                'INSERT INTO analysis (search_id, analysis_type, body) VALUES (?,?,?)',
                (search_id, analysis_type, body)
            )
            db.commit()
            session.clear()
            g.results = body
            return render_template('./scraper/scraper.html')

        flash(error)

    return render_template('./scraper/scraper.html')

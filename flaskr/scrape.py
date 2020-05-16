import functools
from flaskr.db import get_db
from flaskr.webScraper import scrape
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('', __name__, url_prefix='/')
results = ''


@bp.route('/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        db = get_db()
        error = None

        # Bring in parameters from form
        searchWord = request.form['searchWord']
        analysisType = request.form['format']

        # Catching input errors
        if not searchWord:
            error = 'Please put in a word to scrape.'
        elif not analysisType:
            error = 'Analysis type not set.'

        # Initialize with searched and analyzed being none
        searchedAndAnalyzed = None

        # Query to see if search_word exists
        alreadySearched = db.execute(
            'SELECT id, search_word FROM search WHERE search_word = ?', (
                searchWord,)
        ).fetchone()

        # If it has been searched, we then query the search_word and analysis type
        #  to see if this particular analysis type has been saved
        if alreadySearched is not None:
            searchedAndAnalyzed = db.execute(
                'SELECT id, body FROM analysis WHERE search_id = ? AND analysis_type = ?', (
                    alreadySearched['id'], analysisType)
            ).fetchone()

        # If the word has been searched and been analyzed in the specified way, we return searchedAndAnalyzed
        if searchedAndAnalyzed is not None:
            results = searchedAndAnalyzed['body']
            return renderResults(results, searchWord, analysisType)

        # If it has not been searched before, we search and scrape, save the search word into search table
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

            return renderResults(results, searchWord, analysisType)

        flash(error)

    return renderResults(results, searchWord, analysisType)


def renderResults(results, searchWord, analysisType):
    return render_template('./scraper/scraper.html',
                           results=results, search=searchWord, analysisType=analysisType)

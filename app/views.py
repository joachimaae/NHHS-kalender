from flask import render_template
from app import app
from app import gcal

@app.route('/index')
@app.route('/')
def index():
    events = gcal.hent_events()
    return render_template("index.html", eventer=events)

@app.route('/liste')
def liste():
    """ Lister opp events
    """
    
    events = gcal.hent_events()
    return render_template("liste.html",
                           eventer=events)
                           
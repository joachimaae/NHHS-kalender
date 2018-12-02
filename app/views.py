from flask import render_template
from app import app
from app import gcal
import datetime
@app.route('/index')
@app.route('/')
def index():
    events = gcal.hent_events()
    ukenr = datetime.datetime.now().isocalendar()[1]
    return render_template("index.html", eventer=events, ukenummer_dag=int(ukenr))

@app.route('/index/<weeknum>')
def weekswitch(weeknum):
    events = gcal.hent_events()
    return render_template("index.html", eventer=events, ukenummer_dag=int(weeknum))

@app.route('/liste')
def liste():
    """ Lister opp events
    """
    
    events = gcal.hent_events()
    return render_template("liste.html",
                           eventer=events)
                           
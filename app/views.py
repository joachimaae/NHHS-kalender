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


"""
eksempel på flask:
    fakeTittel = {'tittel1': 'Fotball', 'tittel2': 'Håndball'}
    fakeStartTid = {'startTid1': '08:30','startTid2': '09:30'}
    fakeSluttTid = {'sluttTid1': '08:30','sluttTid2': '09:30'}
    fakeId = {'id1': '1','id2': '2'}

    tittel = {}
    startTid = {}
    sluttTid = {}
    id = {}
    for x in range(0, len(fakeTittel) - 1):
        tittel.update(fakeTittel[x])
        startTid.update(fakeStartTid[x])
        sluttTid.update(fakeSluttTid[x])
        id.update(fakeId[x])
"""
from flask import render_template
from app import app
from app import gcal

events = gcal.hent_events()

@app.route('/index')
@app.route('/')
def index():
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

    return render_template("index.html",
                           tittel=tittel,
                           startTid=startTid,
                           sluttTid=sluttTid,
                           id=id)

@app.route('/liste')
def liste():
    """ Lister opp events
    """
    return render_template("liste.html",
                           tittel=events)


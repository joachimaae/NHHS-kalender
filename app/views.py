from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    tittel = {'tittel1': 'Fotball', 'tittel2': 'Håndball'}
    startTid = {'startTid1': '08:30'}
    sluttTid = {'sluttTid1': '09:30'}
    id = {'id1': '1'}
    return render_template("index.html",
                           tittel=tittel,
                           startTid=startTid,
                           sluttTid=sluttTid,
                           id=id)

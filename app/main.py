from flask import Flask, render_template
import gcal
import datetime

app = Flask(__name__)

# Helper function that gets all dates of a week
def get_dates(year, week):
    d = datetime.date(year,1,1)
    if(d.weekday()<= 3):
        d = d - datetime.timedelta(d.weekday())             
    else:
        d = d + datetime.timedelta(7-d.weekday())
    dlt = datetime.timedelta(days = (week-1)*7)
    start = d + dlt
    rawdatelist = [
        start,
        start + datetime.timedelta(days=1),
        start + datetime.timedelta(days=2),
        start + datetime.timedelta(days=3),
        start + datetime.timedelta(days=4),
        start + datetime.timedelta(days=5),
        start + datetime.timedelta(days=6)
        ]
    datelist = []
    for i in rawdatelist:
        datelist.append(str(i.day) + '.' + str(i.month))

    return datelist


@app.route('/', defaults={'lang': 'no'})
@app.route('/<lang>/')
def index(lang):
    events = gcal.hent_events()
    ukenr = datetime.datetime.now().isocalendar()[1]
    year = datetime.datetime.now().isocalendar()[0]
    dates = get_dates(year, ukenr)
    if(lang == 'no'):
        return render_template("index.html", eventer=events, ukenummer_dag=int(ukenr), lang=lang, dates=dates)
    else:
        return render_template("indexeng.html", eventer=events, ukenummer_dag=int(ukenr), lang=lang, dates=dates)

@app.route('/<lang>/<weeknum>')
def weekswitch(weeknum, lang):
    events = gcal.hent_events()
    year = datetime.datetime.now().isocalendar()[0]
    dates = get_dates(year, int(weeknum))
    if(lang == 'no'):
        return render_template("index.html", eventer=events, ukenummer_dag=int(weeknum), lang=lang, dates=dates)
    else:
        return render_template("indexeng.html", eventer=events, ukenummer_dag=int(weeknum), lang=lang, dates=dates)

@app.route('/liste')
def liste():
    """ Lister opp events
    """
    
    events = gcal.hent_events()
    return render_template("liste.html",
                           eventer=events)
                           

if __name__ == "__main__":
    app.run(debug=True)


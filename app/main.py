from flask import Flask, render_template
import gcal
import datetime
import search

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
    datelist = [
        start,
        start + datetime.timedelta(days=1),
        start + datetime.timedelta(days=2),
        start + datetime.timedelta(days=3),
        start + datetime.timedelta(days=4),
        start + datetime.timedelta(days=5),
        start + datetime.timedelta(days=6)
        ]
    datelist = [str(i.day) + '.' + str(i.month) for i in datelist]
    return datelist



@app.route('/', defaults={'lang': 'no', 'cal': 'nhhs', 'year':datetime.datetime.now().isocalendar()[0], 'weeknum':datetime.datetime.now().isocalendar()[1]})
@app.route('/<lang>/<cal>/', defaults={'year':datetime.datetime.now().isocalendar()[0], 'weeknum':datetime.datetime.now().isocalendar()[1]})
@app.route('/<lang>/<cal>/<year>/<weeknum>')

def weekswitch(year, weeknum, lang, cal):
    events = gcal.hent_events(lang, cal)
    dates = get_dates(int(year), int(weeknum))

    link = gcal.get_url(cal, lang)
    link = link[link.index('/'):]
    link = 'webcal:' + link 

    if(lang == 'no'):
        return render_template("index.html", eventer=events, ukenummer_dag=int(weeknum), aar=int(year), lang=lang, dates=dates, cal=cal, link=link)
    else:
        return render_template("indexeng.html", eventer=events, ukenummer_dag=int(weeknum), aar=int(year), lang=lang, dates=dates, cal=cal, link=link)




@app.route('/liste')
def liste():
    """ Lister opp events
    """
    
    events = gcal.hent_events('no')
    return render_template("liste.html",
                           eventer=events)

@app.route('/search/<item>')
def lookFor(item):
    events = search.searchFor(item)
    return render_template('liste.html', eventer=events)

if __name__ == "__main__":
    app.run(debug=True)


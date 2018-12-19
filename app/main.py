from flask import Flask, render_template
import gcal
import datetime

app = Flask(__name__)

@app.route('/', defaults={'lang': 'no'})
@app.route('/<lang>/')
def index(lang):
    events = gcal.hent_events()
    ukenr = datetime.datetime.now().isocalendar()[1]
    if(lang == 'no'):
        return render_template("index.html", eventer=events, ukenummer_dag=int(ukenr), lang=lang)
    else:
        return render_template("indexeng.html", eventer=events, ukenummer_dag=int(ukenr), lang=lang)

@app.route('/<lang>/<weeknum>')
def weekswitch(weeknum, lang):
    events = gcal.hent_events()
    if(lang == 'no'):
        return render_template("index.html", eventer=events, ukenummer_dag=int(weeknum), lang=lang)
    else:
        return render_template("indexeng.html", eventer=events, ukenummer_dag=int(weeknum), lang=lang)

@app.route('/liste')
def liste():
    """ Lister opp events
    """
    
    events = gcal.hent_events()
    return render_template("liste.html",
                           eventer=events)
                           

if __name__ == "__main__":
    app.run(debug=True)


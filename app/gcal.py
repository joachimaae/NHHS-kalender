# Requires: google-api-python-client, oauth2client

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

from google.oauth2 import service_account

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CLIENT_SECRET_FILE = 'cred.json'
APPLICATION_NAME = 'Google Calendar API'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    # Use service account if available
    SERVICE_ACCOUNT_FILE="cred.json"
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return credentials
    except:
        return
    '''
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
        '''


def hent_events(lang='no'):
    """ Henter arrangementer og lagrer de i en dictionary "eventer"
    -> dict of list of str

    eventer har  som verdi en liste med arrangementets starttidspunkt, tittel og evt. beskrivelse.
    """
    credentials = get_credentials()
    #http = credentials.authorize(httplib2.Http())
    #service = discovery.build('calendar', 'v3', http=http)
    service = discovery.build('calendar', 'v3', credentials=credentials)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    CalID = 'v612u1rohvpfau1fkgthola1dk@group.calendar.google.com' if lang=='no' else 'pfj36dednqcnd0rm55rqjdfrho@group.calendar.google.com'
    eventsResult = service.events().list(
        calendarId=CalID,
        timeMin=now, maxResults=50, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    eventer = {}
    i = 1
    kommentar = "Hei"
    for event in events:
        #print("Ny event:")
        #print(event)
        if ('date' in event['start']):
            date = event['start'].get('date')
            event['start'] = {'dateTime': date + 'T07:00:00+01:00'}
            event['end'] = {'dateTime': date + 'T23:59:00+01:00'}


        start = event['start'].get('dateTime')[11:16]
        slutt = event['end'].get('dateTime')[11:16]
        varighet = datetime.datetime.strptime(event['end'].get('dateTime')[:-6], '%Y-%m-%dT%H:%M:%S') - datetime.datetime.strptime(event['start'].get('dateTime')[:-6], '%Y-%m-%dT%H:%M:%S')
        varighet = varighet.seconds/3600
        dato = event['start'].get('dateTime')[:10]
        ukedag = datetime.datetime.strptime(dato, "%Y-%m-%d").weekday()
        ukenummer = datetime.datetime.strptime(dato, "%Y-%m-%d").isocalendar()[1]
        tittel = event['summary']
        try:
            description = event['description']
        except:
            description = "Ingen beskrivelse tilgjengelig"
        event_id = event['id']

        event_dict = {
            'start_tid':start,
            'slutt_tid': slutt,
            'dato':dato,
            'tittel': tittel,
            'beskrivelse':description,
            'ukedag':ukedag,
            'ukenummer':ukenummer,
            'farge':i,
            'varighet':varighet
        }

        # Farger
        if i < 4:
            i += 1
        else: 
            i = 1
            
        eventer[event_id] = event_dict

    return eventer


if __name__ == "__main__":
    """ Denne brukes for å teste programmet. Dette kjøres når man kjører gcal.py i terminal
    """
    print(hent_events())

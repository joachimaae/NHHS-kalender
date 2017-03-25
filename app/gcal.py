# Requires: pip install --upgrade google-api-python-client

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
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

def list_events():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='v612u1rohvpfau1fkgthola1dk@group.calendar.google.com', timeMin=now, maxResults=50, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    print(events)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        try:  
            print(event['description'])
        except:
            pass

def hent_events():
    """ Henter arrangementer og lagrer de i en dictionary "eventer"
    -> dict of list of str

    eventer har  som verdi en liste med arrangementets starttidspunkt, tittel og evt. beskrivelse.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(
        calendarId='v612u1rohvpfau1fkgthola1dk@group.calendar.google.com',
        timeMin=now, maxResults=50, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
 
    eventer = {}

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))

        if event['id'] in eventer:
            eventer[event].append([start, event['summary']])
            try:
                eventer[event['id']].append(event['description'])
            except:
                pass
        else:
            eventer[event['id']] = [start, event['summary']]
            try:
                eventer[event['id']].append(event['description'])
            except:
                pass

    return eventer


"""Marcus checking in"""


if __name__ == "__main__":
    """ Denne brukes for å teste programmet. Dette kjøres når man kjører gcal.py i terminal
    """
    print(hent_events())
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
import itertools

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

defaultPos = 'center'

def get_credentials():
   
    # Use service account if available
    SERVICE_ACCOUNT_FILE="cred.json"
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return credentials
    except:
        return

## Test for hvis to tidpunkt overlapper, Hjelpefunskjon til check_for_overlaps  
def overlap(tid1, tid2, tid3):
    delta1 = tid2 - tid1
    delta2 = tid3 - tid1

    if(delta2 < delta1):
         return True
    
    return False

## Finn den motsatte siden, Hjelpefunskjon til check_for_overlaps  
def opositeSide(side):
    if (side == 'left'):
        return 'right'
    
    return 'left'

## Funskjon for å legge til side for eventer hvor det er flere på et tidspunkt
def check_for_overlaps(liste):
    global defaultPos
    datepairs = []

    ## Finn eventer som er på samme dag
    for k, v in liste.items():
        dato_1 =  v['dato']
        
        for l, m in liste.items():
            ## Test hvis det er samme event
            if (k == l):
                continue

            dato_2 = m['dato']
        
            ## Test hvis hendelsen ikke skjer på sammme dato
            if (dato_1 != dato_2):
                continue
            
            templist = [k, l]
            templist.sort()
            datepairs.append(templist)
               
    # Fjern duplekater av eventer på samme dag
    datepairs = set(map(tuple, datepairs))
    datepairs = list(map(list, datepairs))


    ## Se om eventene på samme dag overlapper med tanke på tidspunkt
    for i in datepairs:
        isOverlap = False
        ## Henter nåværende posisjon
        pos1 = liste[i[0]]['posisjon']
        pos2 = liste[i[1]]['posisjon']


        ## Finn start-slutt tid på event 1
        start_tid_1 = datetime.datetime.strptime(liste[i[0]]['start_tid'], '%H:%M')#.time()
        slutt_tid_1 = datetime.datetime.strptime(liste[i[0]]['slutt_tid'], '%H:%M')#.time()

        ## Finn start-slutt tid på event 2
        start_tid_2 = datetime.datetime.strptime(liste[i[1]]['start_tid'], '%H:%M')#.time()
        slutt_tid_2 = datetime.datetime.strptime(liste[i[1]]['slutt_tid'], '%H:%M')#.time()
        
        
        ## Hvis 1 starter før 2
        if (start_tid_1 < start_tid_2):
            isOverlap = overlap(start_tid_1, slutt_tid_1, start_tid_2)

        ## Hvis 2 starter før 1
        if (start_tid_2 < start_tid_1):
            isOverlap = overlap(start_tid_2, slutt_tid_2, start_tid_1)
        
        ## Hvis de starter likt
        if (start_tid_1 == start_tid_2):
            isOverlap = True

        ## Hvis overlapp (litt ekstra logikk for når det er 2 som har overlapp med 1)
        if (isOverlap):
            if (pos1 == defaultPos and pos2 == defaultPos):
                liste[i[0]]['posisjon'] = 'left'
                liste[i[1]]['posisjon'] = 'right'
                continue
            
            if (pos1 == defaultPos and pos2 != defaultPos):
                liste[i[0]]['posisjon'] = opositeSide(pos2)

            if (pos2 == defaultPos and pos1 != defaultPos):
                liste[i[1]]['posisjon'] = opositeSide(pos1)
    
    return liste

       
def hent_events(lang='no'):
    """ Henter arrangementer og lagrer de i en dictionary "eventer"
    -> dict of list of str

    eventer har  som verdi en liste med arrangementets starttidspunkt, tittel og evt. beskrivelse.
    """
    global defaultPos
    credentials = get_credentials()
    #http = credentials.authorize(httplib2.Http())
    #service = discovery.build('calendar', 'v3', http=http)
    service = discovery.build('calendar', 'v3', credentials=credentials)

    now = str(datetime.date.today() - datetime.timedelta(days=7)) + 'T00:00:0.0Z'
    CalID = 'v612u1rohvpfau1fkgthola1dk@group.calendar.google.com' if lang=='no' else 'pfj36dednqcnd0rm55rqjdfrho@group.calendar.google.com'
    eventsResult = service.events().list(
        calendarId=CalID,
        timeMin=now, maxResults=50, 
        singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    

    eventer = {}
    i = 1
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
            'varighet':varighet,
            'posisjon': defaultPos
        }

        # Farger
        if i < 4:
            i += 1
        else: 
            i = 1
            
        eventer[event_id] = event_dict
    
    eventer = check_for_overlaps(eventer)
    return eventer


if __name__ == "__main__":
    """ Denne brukes for å teste programmet. Dette kjøres når man kjører gcal.py i terminal
    """
    eventer = hent_events()
    eventer = check_for_overlaps(eventer)
    #print(hent_events())

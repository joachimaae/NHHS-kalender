import requests
import icalendar
import time
import datetime
import timeit
import json

defaultPos = 'center'

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


def hent_ical(url):
    rawical = requests.get(url).text
    cal = icalendar.Calendar().from_ical(rawical)
    components = cal.walk()
    components = filter(lambda c: c.name=='VEVENT', components)
    #components = sorted(components, key=lambda c: c.get('dtstart').dt, reverse=False)
    return components

def get_url(service, lang):
    with open('icals.json') as file:
        data = json.load(file)

    return data[service][lang]

def timeConverter(tid):
    return datetime.datetime.strptime(tid, '%H:%M')#.time()

def hent_events(lang, cal):
    global defaultPos

    url = get_url(cal, lang)
    ical_events = hent_ical(url)

    eventer = {}

    i = 1
    for e in ical_events:
        uid = str(e.get('UID'))

        start = e.get('DTSTART').dt
        slutt = e.get('DTEND').dt

        if(type(start) == datetime.datetime): ## Hvis det ikke er heldags
            startTid = '{:d}:{:02d}'.format(start.hour, start.minute)
            sluttTid = '{:d}:{:02d}'.format(slutt.hour, slutt.minute)
        else:
            startTid = '08:00' ## Hvis det er heldags
            sluttTid = '23:00'
        

        if timeConverter(startTid) < timeConverter('08:00'):
            startTid = '08:00'
        if timeConverter(sluttTid) <= timeConverter('08:00'):
            sluttTid = '09:00'
                
        varighet = (datetime.datetime.strptime(sluttTid, '%H:%M') - datetime.datetime.strptime(startTid, '%H:%M')).seconds/3600

        dato = '{}-{:02d}-{:02d}'.format(start.year, start.month, start.day)
        ukedag = datetime.datetime.strptime(dato, "%Y-%m-%d").weekday()
        ukenummer = datetime.datetime.strptime(dato, "%Y-%m-%d").isocalendar()[1]

        year = start.year

        tittel = str(e.get('SUMMARY'))
        beskrivelse = str(e.get('DESCRIPTION'))

        event_dict = {
            'start_tid': startTid,
            'slutt_tid': sluttTid,
            'dato': dato,
            'tittel': tittel,
            'beskrivelse': beskrivelse,
            'ukedag': ukedag,
            'ukenummer': ukenummer,
            'aar': year,
            'farge': i,
            'varighet': varighet,
            'posisjon': defaultPos
        }

        eventer[uid] = event_dict
       
        # Farger
        if i < 4:
            i += 1
        else: 
            i = 1
    
    eventer = check_for_overlaps(eventer) 
    return eventer


if __name__ == "__main__":
    """ Denne brukes for å teste programmet. Dette kjøres når man kjører gcal.py i terminal
    """



    link = get_url('nhhs', 'no')
    link = link[link.index('/'):]
    link = 'webcal:' + link 
    print(link)


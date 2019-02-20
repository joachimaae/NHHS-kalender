# NHHS Kalender

En HTML/CSS/JS kalender som oppdateres fra en Google kalender ved bruk av Python og Google API.

Basert på denne templaten: https://codyhouse.co/demo/schedule-template/index.html

## Funksjonalitet:

Henter inn fra google calendar:

- [x] Tittel 
- [x] Tidspunkt, og plassere i riktig sted i kalenderen.
- [x] Beskrivelse, som skal kunne vises hvis man klikker på arrangementet.

Andre funksjoner:

- [x] Bytte uke
- [x] Mulighet for overlappende tidspunkter. (Flere arrangementer over samme tidsrom, [eksempel.](http://it.nhhs.no/FKU-Cal2/intma/))
- [x] Engelsk språk
- [x] Lagrede credentials for Google
- [ ] Knapp for å abonnere på Google kalenderen
- [ ] Hente inn fra NU kalenderen

Etterspurte funksjoner:
- [ ] Søkefunksjon

bugs:

- [x] Når man går fra uke 52 til uke 1 så vil ikke datoene stemme pga. årstallet ikke øker.
- [x] Appen crasher når man lager heldagsevent.
- [ ] Det går ikke an å ha flere enn to eventer samtidig.

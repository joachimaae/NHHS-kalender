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
- [ ] Mulighet for overlappende tidspunkter. (Flere arrangementer over samme tidsrom)
- [x] Engelsk språk
- [x] Lagrede credentials for Google

Kjente bugs:

- Når man går fra uke 52 til uke 1 så vil ikke datoene stemme pga. årstallet ikke øker.
- Kalenderen er for lang, man kan fikse dette ved å endre antall tidspunkt (indextwo.html), men da må man også endre CSS slik at padding på :
    @media only screen and (min-width: 800px)
        .cd-schedule .events .single-event a {
            padding: 0.3em;
        }


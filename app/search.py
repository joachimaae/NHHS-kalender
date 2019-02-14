import jellyfish
import gcal


def searchFor(item):
    events = gcal.hent_events()
    limit = 0.55
    matches = {}
    for key, value in events.items():
        tittel = value['tittel']
        distance = jellyfish.jaro_distance(tittel.capitalize(), item.capitalize())
        if (distance <= limit):
            continue
        matches[key] = value
        
    return matches
        


if __name__ == "__main__":
    events = searchFor('bbl')
    print(events)

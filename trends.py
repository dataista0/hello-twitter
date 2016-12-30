"""API to trending topics per location.

cli usage:
    `python trends.py`
    enter to a human loop for exploring places on earth
    `python trends.py Argentina`
    print the 10 tts of Argentina and exit.
        * 'Argentina' represents any value in the second election of the `python trends.py` loop.

advanced usage:
    import trends
    # reload(trends)
    trends.update_cache()
    trends.run('Buenos Aires')
    trends.run('New York') # will print the 10 tts of New York and return

    trends.run() # will enter the same human loop as with cli usage

    trends.run(country='Argentina') # will enter a human loop for that country's places.
"""

import sys
import json

import basic

AVAILABLE_TRENDS_CACHE_FILE = 'cache/available_trends.json'

def print_msg(msg):
    """3.0 display."""
    msg = "== %s ==" % msg
    print "=" * len(msg)
    print msg
    print "=" * len(msg)

def update_cache():
    """Update AVAILABLE_TRENDS_CACHE_FILE with an API call.

    It just calls trends_available with tweepy and dumps it in AVAILABLE_TRENDS_CACHE_FILE
    Useful since the request has a limit per hout and it's basically a constant index of locations.
    Fails violently on failures.
    """
    api = basic.get_tweepy_api()
    availables = api.trends_available()
    with open(AVAILABLE_TRENDS_CACHE_FILE, 'w') as cache_file:
        json.dump(availables, cache_file)

def run(place=False, country=False):
    """ Search trending topics per place.

    If no parameters are provided will enter an interactive loop to explore the options.
    If country is provided, will loop only through country options.
    If place is provided will print the trending topics for that place and exit.
    If place is provided, country is ignored.
    The params are not validated.
    """
    try:
        with open(AVAILABLE_TRENDS_CACHE_FILE) as cache_file:
            availables = json.load(cache_file)
    except:
        print 'problem getting cache, try running update_cache()'
        return 1

    countries = sorted(list(set([available['country'] for available in availables])))
    print_msg('Welcome to trends explorer')
    while True:
        if not country and not place:
            print 'Available countries:'
            for i, a_country in enumerate(countries):
                print "{:<20}".format(a_country),
                if not i % 5:
                    print
            print
            print
            selected_country = raw_input("Please, select a country (empty for world wide): ")
            while selected_country not in countries:
                print 'Selected country is invalid.'
                selected_country = raw_input("Please, select a country (empty for world wide): ")
        else:
            selected_country = country
        places = sorted(list(set([(available['name'], available['placeType']['name']) for available in availables
                                                                                    if available['country'] == selected_country])))
        places_names = [a_place[0] for a_place in places]

        if not place:
            print
            print 'Available places for %s: %d' % (selected_country, len(places))
            print
            for i, (a_place, place_type) in enumerate(places):
                print a_place, "({}){:<20}".format(place_type,''),
                if i > 0 and not i % 2:
                    print
            print
            print
            selected_place = raw_input("Please, select a place: ")
            while selected_place not in places_names:
                print 'Selected place is invalid.'
                selected_place = raw_input("Please, select a place (specify name without type): ")
        else:
            selected_place = place

        selected_woeid = [selected['woeid'] for selected in availables if selected['name'] == selected_place][0]
        involved_country = [selected['country'] for selected in availables if selected['name'] == selected_place][0]
        api = basic.get_tweepy_api()

        result = api.trends_place(selected_woeid)
        result_trends = result[0]['trends']
        print_msg('Total obtained trends for %s (%s): %d' % (selected_place, involved_country, len(result_trends)))
        for trend in result_trends:
            print trend['name']
        if place:
            return 0
        print
        raw_input("Press any key to continue... ")
        print

    return 0


if __name__ == '__main__':
    sys.exit(run(sys.argv[1]) if len(sys.argv) == 2 else run())
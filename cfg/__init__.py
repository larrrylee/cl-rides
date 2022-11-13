from cfg.config import *

"""Loads map.txt into a dictionary of bitmaps for the hardcoded locations.
"""
try:
    with open(MAP_FILE, 'r') as map:
        loc = 0b1
        for line in map:
            if (line.startswith('#')):
                continue
            places = line.split(',')
            places = [place.strip() for place in places]
            for key in loc_map:
                if key in places:
                    loc_map[key] |= loc
            loc <<= 1
except:
    print(f'Unable to load ${MAP_FILE}. Location optimizations are ignored.')

"""Loads ignore_drivers.txt into a list.
"""
try:
    with open(IGNORE_DRIVERS_FILE, 'r') as nums:
        for num in nums:
            ignored_drivers.append(num.strip())
except:
    print(f'Unable to load ${IGNORE_DRIVERS_FILE}. No drivers ignored.')

"""Loads ignore_riders.txt into a list.
"""
try:
    with open(IGNORE_RIDERS_FILE, 'r') as nums:
        for num in nums:
            ignored_riders.append(num.strip())
except:
    print(f'Unable to load ${IGNORE_RIDERS_FILE}. No riders ignored.')

from enum import IntEnum
from heapq import heappop, heappush

class Clearance(IntEnum):
    NONE = 0
    RED = 1
    BLUE = 2
    GREEN = 3

def security_route(stations, segments, source, target):
    """Finds the fastest route from source station to target station.

    You start with no security clearance.
    When at a security station, you may choose to set your clearance to the same
    as that of the station.
    Each segment gives how long it takes to get from one station to another, and
    what clearance is required to be able to take that segment.

    Target Complexity: O(N lg N) in the size of the input (stations + segments).

    Args:
        stations: A list of what clearance is available at each station, or
            `NONE` if that station can not grant any clearance.
        segments: A list of `(u, v, t, c)` tuples, each representing a segment
            from `stations[u]` to `stations[v]` taking time `t` and requiring
            clearance `c` (`c` may be `NONE` if no clearance is required).
        source: The index of the station from which we start.
        target: The index of the station we are trying to reach.

    Returns:
        The minimum length of time required to get from `source` to `target`, or
        `None` if no route exists.
    """
    number_of_stations = len(stations)
    station_connections = {}
    
    for i in range(number_of_stations):
        station_connections[i] = []

    for u, v, t, c in segments:
        station_connections[u].append((v, t, c))

    priority_queue = [(0, source, Clearance.NONE)]
    visited_stations = {} 

    while priority_queue:
        current_time, station, clearance = heappop(priority_queue)

        if station == target:
            return current_time

        if (station, clearance) in visited_stations and visited_stations[(station, clearance)] <= current_time:
            continue

        visited_stations[(station, clearance)] = current_time

        for next_station, travel_time, required_clearance in station_connections[station]:
            if required_clearance == Clearance.NONE or required_clearance == clearance:
                next_station_travel_time = current_time + travel_time
                if (next_station, clearance) not in visited_stations or visited_stations[(next_station, clearance)] > next_station_travel_time:
                    heappush(priority_queue, (next_station_travel_time, next_station, clearance))

        if stations[station] != Clearance.NONE:
            new_clearance = stations[station]
            if (station, new_clearance) not in visited_stations or visited_stations[(station, new_clearance)] > current_time:
                heappush(priority_queue, (current_time, station, new_clearance))

    return None

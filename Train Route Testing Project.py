
class Union_Find:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, x):
        if self.parent.get(x, x) != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent.get(x, x)

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank.get(root_x, 0) > self.rank.get(root_y, 0):
                self.parent[root_y] = root_x
            elif self.rank.get(root_x, 0) < self.rank.get(root_y, 0):
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] = self.rank.get(root_x, 0) + 1


def trains_planes(trains, planes):
    """Find what flights can be replaced with a rail journey.

    Initially, there are no rail connections between cities. As rail connections
    become available, we are interested in knowing what flights can be replaced
    by a rail journey, no matter how indirect the route. All rail connections
    are bidirectional.

    Target Complexity: O(N lg N) in the size of the input (trains + planes).

    Args:
        trains: A list of `(date, lcity, rcity)` tuples specifying that a rail
            connection between `lcity` and `rcity` became available on `date`.
        planes: A list of `(code, date, depart, arrive)` tuples specifying that
            there is a flight scheduled from `depart` to `arrive` on `date` with
            flight number `code`.

    Returns:
        A list of flights that could be replaced by a train journey.
    """
    trains.sort(key=lambda x: x[0])
    planes.sort(key=lambda x: x[1])

    union_find = Union_Find()
    replaceable_flights = []
    
    train_index = 0
    number_of_trains = len(trains)

    for code, date, depart, arrive in planes:
        while train_index < number_of_trains and trains[train_index][0] <= date:
            _, lcity, rcity = trains[train_index]
            union_find.union(lcity, rcity)
            train_index += 1

        if union_find.find(depart) == union_find.find(arrive):
            replaceable_flights.append((code, date, depart, arrive))

    return replaceable_flights

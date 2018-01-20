from Supervisor import Supervisor
import time
from Input import *
from Strategy import Strategy

def main():
    t1 = time.time()

    # M = Model()
    # M.train([])

    """
    gasStation = GasStation()
    route = Route("../geg. Dateien/Eingabedaten/Fahrzeugrouten/Bertha Benz Memorial Route.csv")
    strategy = Strategy()
    L = [1] * 31
    route.appendPrize(L)
    print(route.route)
    t = time.clock()
    print("Executing naiveCalculate")
    print(strategy.naiveCalculate(route, gasStation))
    print("Finished naiveCalculate")
    print(route.route)
    """

    gasStation = GasStation()
    route = Route()
    strategy = Strategy()

    activeID = 1
    nearToActiveID = []
    for station in range(15000):
        route.capacity = 1
        route.route = [(100, activeID, 0, 0), (101, station, 0, 0)]
        strategy.route = route.route
        distance = strategy.consumption(0, 1) / 5.6 * 100
        if distance < 100:
            nearToActiveID.append(station)

    print("activeID", activeID, "nearToActiveID", nearToActiveID)

    #S = Supervisor()
    #S.handleHandle()

    t2 = time.time()
    print("executed in", t2 - t1, "seconds")



if __name__ == '__main__':
    main()

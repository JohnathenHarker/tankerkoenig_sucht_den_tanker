from Supervisor import Supervisor
import time
from Input import *
from Strategy import Strategy

def main():
    t1 = time.time()

    # M = Model()
    # M.train([])

    gasStation = GasStation()
    route = Route()
    route.read("../geg. Dateien/Eingabedaten/Fahrzeugrouten/Bertha Benz Memorial Route.csv")
    strategy = Strategy(gasStation)
    L = [1] * 31
    route.appendPrize(L)
    print(route.route)
    t = time.clock()
    print("Starting calculation")
    print(strategy.calculate(route))
    route.write("../geg. Dateien/Eingabedaten/Fahrzeugrouten/Bertha Benz Memorial Route.csv")
    print("Finished calculation")

    print("Starting naiveCalculate")
    print(strategy.naiveCalculate(route))
    print("Finished naiveCalculate")
    print(route.route)

    strategy = Strategy(gasStation)

    print("Starting to find gasStations next to 1")
    activeID = 1
    nearToActiveID = []
    for station in range(1, 15000):
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

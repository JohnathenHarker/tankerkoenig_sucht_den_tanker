from Supervisor import Supervisor
import time
from Input import *
from Strategy import Strategy

def main():
    t1 = time.time()

    # M = Model()
    # M.train([])
    gasStation = GasStation()
    """
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
    """
    strategy = Strategy(gasStation)
    prizeList = []
    for i in range(1,10):
        route = Route()
        file = "../geg. Dateien/Eingabedaten/Fahrzeugrouten/Route"+str(i)+"_mit_Tankstrategie.csv"
        route.read(file)
        innerPrizeList = []
        with open(file, encoding='utf-8') as routefile:
            first_line = True
            for line in routefile:
                if first_line:
                    first_line = False
                else:
                    linelist = line.split(";")
                    # (date, id, prize, amount)
                    innerPrizeList.append(int(linelist[2]))
        route.appendPrize(innerPrizeList)
        prizeList.append((i,strategy.calculate(route),strategy.naiveCalculate(route)))
    print(prizeList)

    with open("VergleichX", "w") as f:
        f.write(prizeList)



    """
    for i in range(1,15000, 100):

        activeID = i
        print("Starting to find gasStations next to", activeID)
        nearToActiveID = []
        for station in range(1, 15000):
            route.capacity = 1
            route.route = [(100, activeID, 0, 0), (101, station, 0, 0)]
            strategy.route = route.route
            distance = strategy.consumption(0, 1) / 5.6 * 100
            if distance < 100:
                nearToActiveID.append(station)

        print("activeID", activeID, "nearToActiveID", nearToActiveID)

        with open("nearFile", mode="a") as file:
            file.write("activeID: " + str(activeID) +  "nearToActiveID" + str(nearToActiveID))
    #S = Supervisor()
    #S.handleHandle()
    """
    t2 = time.time()
    print("executed in", t2 - t1, "seconds")



if __name__ == '__main__':
    main()

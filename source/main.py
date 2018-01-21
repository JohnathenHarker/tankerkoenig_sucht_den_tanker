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
    route = Route()
    route.read("../geg. Dateien/Eingabedaten/Fahrzeugrouten/Bertha Benz Memorial Route.csv")
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
	
    print("InformatiCup 2017/18 - author: T.Hinnerichs, T. John")
    S = Supervisor()
    S.handleHandle()

    t2 = time.time()
    print("executed in", t2 - t1, "seconds")



if __name__ == '__main__':
    main()

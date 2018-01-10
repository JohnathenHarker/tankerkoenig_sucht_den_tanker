from Supervisor import Supervisor
import time

def main():
    t1 = time.time()

    # M = Model()
    # M.train([])





    S = Supervisor()
    S.handleHandle()

    t2 = time.time()
    print("executed in", t2 - t1, "seconds")



if __name__ == '__main__':
    main()

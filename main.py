#!/usr/bin/env python2
import random
import time

from Regius.network import Network
from Regius.car import Car

ip = "localhost"
port = 31337



def main():
    car = Car()
    net = Network(ip, port)
    net.write(car.name)
    net.write(1<<5)

    data = net.read()
    car.initmap(data)

    net.write(0)
    car.update(net.read())

    while True:
        net.write(car.getmove())
        car.update(net.read())
        time.sleep(0.1)


if __name__ == "__main__":
    main()


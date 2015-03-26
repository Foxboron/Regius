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

    net.write(1)
    car.update(net.read())
    #net.write(1)
    #net.read()

    while True:
        s = net.read()
        if s:
            car.update(s)
            net.write(car.getmove())


if __name__ == "__main__":
    main()


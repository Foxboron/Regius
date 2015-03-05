#!/usr/bin/env python2
import random

from Regius.network import Network
from Regius.car import Car

ip = "localhost"
port = 31337

movements = {"up": 1<<0,
             "down": 1<<1,
             "left": 1<<2,
             "right": 1<<3,
             "space": 1<<4,
             "return": 1<<5}



def main():
    car = Car()
    net = Network(ip, port)
    net.write(car.name)
    net.write(movements["return"])

    data = net.read()
    car.initmap(data)

    while True:
        net.write(movements["up"])
        net.read()


if __name__ == "__main__":
    main()


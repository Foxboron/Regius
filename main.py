#!/usr/bin/env python2
import random

from Regius.network import Network

ip = "localhost"
port = 31337

movements = {"up": 1<<0,
             "down": 1<<1,
             "left": 1<<2,
             "right": 1<<3,
             "space": 1<<4,
             "return": 1<<5}



def main():
    net = Network(ip, port)
    net.write(1<<5)
    net.write(1<<0)
    while True:
        net.read()
        net.write(random.choice(movements.values()))


if __name__ == "__main__":
    main()


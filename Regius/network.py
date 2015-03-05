import socket
import sys
import json



class Network(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.soc = socket.socket()
        self.soc.connect((ip,port))
        self.block = False

    def read(self):
        data = None
        try:
            ret = self.soc.makefile().readline()
            data = json.loads(ret)
        except:
            pass

        if not self.block:
            # Just easier to handle it this way
            self.soc.setblocking(0)
            self.block = True

        return data

    def write(self, msg):
        try:
            self.soc.sendall(str(msg)+"\n")
        except:
            pass






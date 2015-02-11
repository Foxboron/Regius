import socket
import json



class Network(object):
    def __init__(ip, port):
        self.ip = ip
        self.port = port
        self.soc = socket.socket()
        self.soc.connect((ip,port))
        self.block = False

    def read(self):
        try:
            ret = sock.makefile().readline()
            data = json.loads(ret)
        except:
            pass

        if not self.block:
            # Just easier to handle it this way
            self.soc.setblocking(0)
            self.block = True
        return data

    def write(self, msg):
        self.soc.sendall(str(msg)+"\n")






import socket
import sys
import getopt
import os
import time

PI = 3.14159265359
data_size = 2**17

def clip(v, lo, hi):
    if v < lo: return lo
    elif v > hi: return hi
    else: return v

def destringify(s):
    if not s: return s
    if type(s) is str:
        try: return float(s)
        except ValueError: return s
    elif type(s) is list:
        if len(s) < 2: return destringify(s[0])
        else: return [destringify(i) for i in s]

class ServerState():
    def __init__(self):
        self.d = dict()
    def parse_server_str(self, server_string):
        self.servstr = server_string.strip()[:-1]
        sslisted = self.servstr.strip().lstrip('(').rstrip(')').split(')(')
        for i in sslisted:
            w = i.split(' ')
            self.d[w[0]] = destringify(w[1:])

class DriverAction():
    def __init__(self):
        self.d = {'accel':0.2, 'brake':0, 'clutch':0, 'gear':1, 'steer':0, 'focus':[-90,-45,0,45,90], 'meta':0}
    def clip_to_limits(self):
        self.d['steer'] = clip(self.d['steer'], -1, 1)
        self.d['brake'] = clip(self.d['brake'], 0, 1)
        self.d['accel'] = clip(self.d['accel'], 0, 1)
        self.d['gear'] = int(clip(self.d['gear'], -1, 6))
    def __repr__(self):
        self.clip_to_limits()
        out = str()
        for k, v in self.d.items():
            out += '(' + k + ' '
            out += '%.3f' % v if not type(v) is list else ' '.join([str(x) for x in v])
            out += ')'
        return out

class Client():
    def __init__(self, H='localhost', p=3001, i='SCR', e=1, t='unknown', s=3, d=False):
        self.host, self.port, self.sid = H, p, i
        self.maxSteps = 100000
        self.S, self.R = ServerState(), DriverAction()
        self.setup_connection()

    def setup_connection(self):
        try:
            self.so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.so.settimeout(1)
        except socket.error: sys.exit(-1)
        
        while True:
            initmsg = '%s(init -45 -19 -12 -7 -4 -2.5 -1.7 -1 -.5 0 .5 1 1.7 2.5 4 7 12 19 45)' % self.sid
            try:
                self.so.sendto(initmsg.encode(), (self.host, self.port))
                sockdata, addr = self.so.recvfrom(data_size)
                if '***identified***' in sockdata.decode(): break
            except socket.error: print("Waiting for TORCS server...")

    def get_servers_input(self):
        try:
            sockdata, addr = self.so.recvfrom(data_size)
            sockdata = sockdata.decode('utf-8')
            if '***shutdown***' in sockdata: self.shutdown()
            else: self.S.parse_server_str(sockdata)
        except socket.error: pass

    def respond_to_server(self):
        try:
            self.so.sendto(repr(self.R).encode(), (self.host, self.port))
        except socket.error: sys.exit(-1)

    def shutdown(self):
        if self.so: self.so.close(); self.so = None; sys.exit(0)

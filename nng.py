#!/usr/bin/python

import ctypes

from ctypes import *
from pprint import pprint

libnng = CDLL("libnng.so")

NNG_FLAG_ALLOC = 1

NNG_OPT_SUB_SUBSCRIBE = "sub:subscribe"

# all xx_open routines are: int nng_xx_open(nng_socket *result)
libnng.nng_sub0_open.argtypes = (ctypes.c_void_p,)
libnng.nng_sub0_open.restype  =  ctypes.c_int

libnng.nng_pub0_open.argtypes = (ctypes.c_void_p,)
libnng.nng_pub0_open.restype  =  ctypes.c_int

libnng.nng_req0_open.argtypes = (ctypes.c_void_p,)
libnng.nng_req0_open.restype  =  ctypes.c_int

libnng.nng_rep0_open.argtypes = (ctypes.c_void_p,)
libnng.nng_rep0_open.restype  =  ctypes.c_int

libnng.nng_pair0_open.argtypes = (ctypes.c_void_p,)
libnng.nng_pair0_open.restype  =  ctypes.c_int

libnng.nng_pair1_open.argtypes = (ctypes.c_void_p,)
libnng.nng_pair1_open.restype  =  ctypes.c_int

libnng.nng_bus0_open.argtypes = (ctypes.c_void_p,)
libnng.nng_bus0_open.restype  =  ctypes.c_int

#                                 socket        char **buf                size_t *sz                flags
libnng.nng_recv.argtypes      = (ctypes.c_uint, POINTER(ctypes.c_void_p), POINTER(ctypes.c_size_t), ctypes.c_int)
libnng.nng_recv.restype       =  ctypes.c_int
libnng.nng_send.argtypes      = (ctypes.c_uint, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int)
libnng.nng_send.restype       =  ctypes.c_int

#                                 socket        url              handler*         flags
libnng.nng_listen.argtypes    = (ctypes.c_uint, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_int)
libnng.nng_listen.restype     =  ctypes.c_int
libnng.nng_dial.argtypes      = (ctypes.c_uint, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_int)
libnng.nng_dial.restype       =  ctypes.c_int

# misc

libnng.nng_setopt.argtypes    = (ctypes.c_uint, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t)
libnng.nng_setopt.restype     =  ctypes.c_int

libnng.nng_strerror.argtypes  = (ctypes.c_int,)
libnng.nng_strerror.restype   =  ctypes.c_char_p

libnng.nng_close.argtypes     = (ctypes.c_uint,)
libnng.nng_close.restype      =  ctypes.c_int

libnng.nng_free.argtypes      = (ctypes.c_void_p, ctypes.c_size_t)

class Error(Exception):

    errcode = 0
    message = ''

    def __init__(self, errcode):

        self.errcode = errcode
        self.message = libnng.nng_strerror(errcode)
        super(Error, self).__init__(self.message)

class BaseSocket(object):

    sock = -1
    raise_exception = True

    def __init__(self, openfunc):

        s = c_uint()
        n = openfunc(byref(s))
        self.ok(n)
        if n == 0:
            self.sock = s.value;

    def __del__(self):

        if self.sock < 0: return
        n = libnng.nng_close(self.sock)
        self.sock = -1
        return self.ok(n)

    def ok(self, rv):

        if not rv: return rv
        if not self.raise_exception: return rv
        raise Error(rv)

    def send(self, buf, flags=0):

        if not isinstance(buf, str):
            buf = str(buf)
        buf = self.enc(buf)
        return self.ok(libnng.nng_send(self.sock, buf, len(buf), flags))

    def recv(self, flags=NNG_FLAG_ALLOC):

        p  = c_void_p()
        sz = c_size_t()

        n = libnng.nng_recv(self.sock, byref(p), byref(sz), flags)
        self.ok(n)
        if not p.value:
            return None

        data = ctypes.POINTER(ctypes.c_char).from_buffer(p)[:sz.value]
        self.ok(libnng.nng_free(p, sz))
        return data.decode('utf-8')

    def enc(self, str):
        return str.encode('utf-8')

class ServerSocket(BaseSocket):
    def listen (self, url, handler=None, flags=0):  return self.ok(libnng.nng_listen(self.sock, self.enc(url), handler, flags))
class ClientSocket(BaseSocket):
    def connect(self, url, handler=None, flags=0):  return self.ok(libnng.nng_dial  (self.sock, self.enc(url), handler, flags))
class Socket(BaseSocket):
    def listen (self, url, handler=None, flags=0):  return self.ok(libnng.nng_listen(self.sock, self.enc(url), handler, flags))
    def connect(self, url, handler=None, flags=0):  return self.ok(libnng.nng_dial  (self.sock, self.enc(url), handler, flags))

class Request   (ClientSocket):
    def __init__(self):        super(Request,    self).__init__(libnng.nng_req0_open)
class Reply     (ServerSocket):
    def __init__(self):        super(Reply,      self).__init__(libnng.nng_rep0_open)
class Pair0     (Socket):
    def __init__(self):        super(Pair0,      self).__init__(libnng.nng_pair0_open)
class Pair1     (Socket):
    def __init__(self):        super(Pair1,      self).__init__(libnng.nng_pair1_open)
class Bus       (Socket):
    def __init__(self):        super(Bus,        self).__init__(libnng.nng_bus0_open)
class Publisher (ServerSocket):
    def __init__(self):        super(Publisher,  self).__init__(libnng.nng_pub0_open)
class Subscriber(ClientSocket):
    def __init__(self):        super(Subscriber, self).__init__(libnng.nng_sub0_open)
    def subscribe(self):
        return self.ok(libnng.nng_setopt(self.sock, self.enc(NNG_OPT_SUB_SUBSCRIBE), "", 0));

if __name__ == "__main__":
    x = libnng.nng_strerror(2)
    print("Quick and dirty self test: ENOMEM = " + x)

## END ##

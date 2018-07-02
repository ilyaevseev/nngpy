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

#                                 socket        char **buf       size_t *sz       flags
libnng.nng_recv.argtypes      = (ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)
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

class Buffer:
    pass

class Exception(Exception):
    pass

class Socket:

    sock = -1

    def __del__(self):
        if self.sock < 0: return
        n = libnng.nng_close(sock)
        sock = -1
        return n

    def send(self, buf, flags=0):
        return libnng.nng_send(self.sock, bytes(buf), len(buf), flags)

    def recv(self):
        pass

class Publisher(Socket):
    def listen(self, url):
        return libnng.nng_listen(self.sock, url, None, 0)

class Subscriber(Socket):
    def connect(self, url):
        libnng.nng_dial(self.sock, url, None, 0)

class Request(Socket):
    def connect(url):
        libnng.nng_dial(self.sock, url, None, 0)

class Reply(Socket):
    def listen(url):
        pass

if __name__ == "__main__":
    x = libnng.nng_strerror(2)
    print(x)

## END ##

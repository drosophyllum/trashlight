#!/usr/bin/env python

import time

nlights=150
RED=0xFF0000
GREEN=0x00FF00
BLUE=0x0000FF

def makecolor(clist):
    r, g, b = clist
    red = int(0xFF*r)
    green = int(0xFF*g)
    blue = int(0xFF*b)
    return int((red<<16) | (green<<8) | (blue))

def printlights(lightlist):
    print '('+','.join(map(lambda x:str(x), lightlist))+',)'

def stringy(speed):
    def rotate(l, n):
        return l[-n:] + l[:-n]
    leds=[0]*nlights
    stamp=time.time()*speed
    delta=0.0
    clist=[0.1,0.0,0.0]
    i=0
    while True:
        while (i<nlights):
            now=time.time()*speed
            delta=now-stamp
            if delta<=1.0:
                continue
            stamp=now
            slot = int(now) % nlights
            leds[slot]=makecolor(clist)
            printlights(leds)
            i+=1
        i=0
        clist = rotate(clist, 1)

if __name__ == '__main__':
    stringy(10)

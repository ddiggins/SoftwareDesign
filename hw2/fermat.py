# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 15:24:07 2014

@author: ddiggins
"""

def check_fermat(x, y, z, n):
    x = int(x)
    y = int(y)
    z = int(z)
    n = int(n)
    if n > 2:
        if x**n + y**n == z**n:
            print "Holy smokes, Fermat was wrong!"
        else:
            print "No, that doesn't work."
    else:
        print "N is less than or equal to 2, so we don't care."
        
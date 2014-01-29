# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 23:06:16 2014

@author: ddiggins
"""

def is_triangle(x, y, z):
    x = int(x)
    y = int(y)
    z = int(z)
    if z < (x+y):
        if y <(x+z):
            if x <(y+z):
                print 'Yes'
            else:
                print 'No'
        else:
            print 'No'
    else:
        print 'No'
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:34:57 2014

@author: pruvolo and ddiggins
"""

# you do not have to use these particular modules, but they may help
#(The are super helpful)


from random import *
import Image
from math import *


def build_random_function(min_depth, max_depth):
    """Takes a minimum and maximum nesting depth and returns a randomly
    generated function comprised of sin_pi, cos_pi, prod, sqr, avg, x, and y"""
    
    xylist = ["x", "y"] #Creates a list of just x and y for use if max_depth <= 1
    
    if max_depth <= 1:
        return xylist[randint(0,1)] #Jumps right to x and y values of max_depth has been reached or somehow exceeded
    
    recurse1 = build_random_function(min_depth-1, max_depth-1) #a and b are assigned values for nesting
    recurse2 = build_random_function(min_depth-1, max_depth-1)
    
    product = ["prod",recurse1,recurse2] #Calculates the product of two values
    sin = ["sin_pi",recurse1] #Calculates the sine in radians of a value times pi
    cos = ["cos_pi",recurse1] #Calculates the cosine in radians of a value times pi
    square = ["sqr",recurse1] #Calculates the square of a signle value
    cube = ["cube",recurse2] #Calculates the average of two values
    x = recurse1 #Inserts a single value
    y = recurse2 #Inserts a single value
    
    functions = [product, sin, cos, square, cube, x, y] #groups above functions into a readable list
    
    if min_depth > 1:  #If min_depth has not been reached, x and y cannot be called
        lists = functions[randrange(0, 4)]
    elif min_depth <= 1: #x and y can be called randomly after min_depth has been reached
        lists = functions[randrange(0, len(functions))]
    
    return lists #returns the big function list

builtfunc = build_random_function(3, 7)

def evaluate_random_function(builtfunction, x, y):
    """Evaluates the random function generated in build_random_function.
    f = the input function from build_random_function
    [x, y] = floats in the range of [-1, 1]
    """
    
    xylist = [x, y] #Creates a smilar list to build_random_function, but uses the actual x and y values
    
    #There are just so many if statements
    
    if builtfunction[0] == 'prod':
        return evaluate_random_function(builtfunction[1], x, y)*evaluate_random_function(builtfunction[2], x, y) #Computes the product of the next two values if the first value in the list indicates a product
    
    elif builtfunction[0] == 'sin_pi':
        return sin(pi * evaluate_random_function(builtfunction[1], x, y)) #Computes sine(pi * a) where a is the next value in the built function
   
    elif builtfunction[0] == 'cos_pi':
        return cos(pi * evaluate_random_function(builtfunction[1], x, y)) #Compues cos(pi * a) where a is the next value in the built function

    elif builtfunction[0] == 'sqr':
        return evaluate_random_function(builtfunction[1], x, y)**2 #Returns the square of the next value of the built function

    elif builtfunction[0] == 'cube':
        return (evaluate_random_function(builtfunction[1], x, y)**3) #Returns the cube of the next value of built function if the first is 'cube'

    elif builtfunction[0] == 'x':
        return xylist[0] #Returns the value of x at the maximum depth of builtfunction

    elif builtfunction[0] == 'y':
        return xylist[1] #Returns the value of y at the maximum depth of builtfunction
    
evalfunc = evaluate_random_function(builtfunc, -.02435, .93425)

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval [input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).
    
        The output of the function is determined by calculatioing the ratio between the 
        first interval and the distance from the interval start to val. This ratio is
        multiplied by the length of the second interval and added to the value of the output interval's
        starting value.
    """
    
    length = input_interval_end-input_interval_start #Calculates difference between start and end of input interval
    
    dist_from_start = val - input_interval_start #Calculates distance between val and start of input interval
    
    ratio = dist_from_start/float(length) #Establishes a ratio of this 
    
    length2 = output_interval_end - output_interval_start #Multiplies this ratio by the length of the output interval
    
    value = output_interval_start + length2 * ratio #Calculates a value by multiplying length2 by ratio and adding the start value of the output interval
    
    return value

#print remap_interval(evalfunc, -1, 1, 0, 255)

def draw_picture():
    """Calling build_random_function, evaluate_random_function, and remap_interval,
    creates and saves an image produced by mapping RGB values to individual pixels in an image.
    """
    im = Image.new("RGB", (350, 350),"black") #Creates a 350px square image
    
    pixels = im.load() #Creates a pixel array
    
    red = build_random_function(6, 15) #Builds RGB functions from build_random_functions
    blue = build_random_function(1, 7) #I chose these depth values because they made me happy
    green = build_random_function(5, 10) #OverlyHonestMethods
    

    for xpixel in range(0, 349):
        for ypixel in range(0, 349): #Traverses every xpixel and ypixel
                xpix = remap_interval(xpixel, 0, 349, -1, 1) #Remaps x and y pixels to a -1, 1 range for use in evaluate_random_function
                ypix = remap_interval(ypixel, 0, 349, -1, 1)
                
                redchannel = evaluate_random_function(red, xpix, ypix) #Determines x and y values of functions from xpix and ypix
                bluechannel = evaluate_random_function(blue, xpix, ypix)
                greenchannel = evaluate_random_function(green, xpix, ypix)
                
                redchannel = int(remap_interval(redchannel, -1, 1, 0, 255)) #Converts channels to inegers for plotting
                bluechannel = int(remap_interval(bluechannel, -1, 1, 0, 255))
                greenchannel = int(remap_interval(greenchannel, -1, 1, 0, 255))
                
                pixels[xpixel, ypixel] = (redchannel, bluechannel, greenchannel) #Plots tuple for every pixel
    
    im.save("Image9.png") #Ka-save!

draw_picture() #I am sorry that my comments got less serious as I got more tired
    
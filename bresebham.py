
def bresenham_line((x,y),(x2,y2)):
    """Brensenham line algorithm"""
    steep = 0
    coords = []
    dx = abs(x2 - x)
    if (x2 - x) > 0: sx = 1
    else: sx = -1
    dy = abs(y2 - y)
    if (y2 - y) > 0: sy = 1
    else: sy = -1
    if dy > dx:
    steep = 1
    x,y = y,x
    dx,dy = dy,dx
    sx,sy = sy,sx
    d = (2 * dy) - dx
    for i in range(0,dx):
    if steep: coords.append((y,x))
    else: coords.append((x,y))
    while d >= 0:
    y = y + sy
    d = d - (2 * dx)
    x = x + sx
    d = d + (2 * dy)
    coords.append((x2,y2))
    return coords

'''
Bresenham's Line Algorithm in Python

See Wikipedia for the psuedocode from which this was implemented.

!/usr/bin/env python

""" This module has an implementation of the Bresenham Algorithm. """

import sys

def irange(start, finish):

"""
This is a naive inclusive range function.

>>> irange(1, 1)
[1]
>>> irange(1, 4)
[1, 2, 3, 4]
>>> irange(4, 1)
[4, 3, 2, 1]
"""
if start == finish:
    return [start]
if start < finish:
    return range(start, finish + 1)
if start > finish:
    return range(start, finish - 1, -1)

def line((x0, y0), (x1, y1)):

"""
Returns all the points between it's arguments.

Check some lines...
>>> line((0, 0), (4, 4))
[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
>>> line((0, 0), (3, 5))
[(0, 0), (1, 1), (1, 2), (2, 3), (2, 4), (3, 5)]
>>> line((1, 1), (4, 6))
[(1, 1), (2, 2), (2, 3), (3, 4), (3, 5), (4, 6)]

Test lines go from start to finish.
>>> line((-1, -1), (-6, -4))
[(-1, -1), (-2, -2), (-3, -2), (-4, -3), (-5, -3), (-6, -4)]
>>> line((-6, -4), (-1, -1))
[(-6, -4), (-5, -3), (-4, -3), (-3, -2), (-2, -2), (-1, -1)]

Test that the same points are generated in the opposite direction.
>>> a = line((0, 0), (29, 43))
>>> b = line((0, 0), (-29, -43))
>>> b = [(-x, -y) for (x, y) in b]
>>> a == b
True

Test that the the same points are generated when the line is mirrored
on the x=y line.
>>> c = line((0, 0), (43, 29))
>>> c = [(y, x) for (x, y) in c]
>>> a == c
True
"""
points = []
orig_x0 = x0
orig_y0 = y0

if abs(y1 - y0) > abs(x1 - x0):
    steep = True
else:
    steep = False

if steep:
    x0, y0 = y0, x0
    x1, y1 = y1, x1
if x0 > x1:
    x0, x1 = x1, x0
    y0, y1 = y1, y0

deltax = x1 - x0
deltay = abs(y1 - y0)
error = deltax / 2
y = y0
if y0 < y1:
    ystep = 1 
else:
     ystep = -1
for x in irange(x0,x1):
    if steep:
        points.append((y,x))
    else:
        points.append((x,y))
    error = error - deltay
    if error < 0:
        y = y + ystep
        error = error + deltax

# If the points go in the wrong direction, reverse them.
if points[0] != (orig_x0, orig_y0):
    points.reverse()

return points

def _test():

"""
This method is responsible for running tests, replace it with whatever
test framework you're using.
"""

import doctest
failures, x = doctest.testmod()

# It's important in some situations (e.g. buildbot) that test failures
# return a non-zero exit code.
if failures > 0:
    sys.exit(1)

This is run if this script is executed, rather than imported.

if name == 'main':

_test()

Posted on 28 August 2009.
'''

import bpy
from math import pi

def deselect_all(context):
    for o in context.scene.objects:
        o.select = False
        
def fret_spacer(fretNumber, scaleLength):
    return scaleLength - (scaleLength/(2**(fretNumber / 12)))

def float_range(start = 0.0, end = 1.0, step = 1.0):
    r = start
    while r < end:
        yield r
        r += step
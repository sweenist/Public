import bpy
import luthiHelpers as helper

def add_fret_board():
    verts = []
    faces = []
    
def add_nut(width):    
    """returns the vertices and face components of the nut mesh"""
    verts = []
    faces = []
    for x in helper.float_range(-width/2.00, ((width/2.00) + (width/4.00)), width/4.00):
        verts.append((x, 0.00, 0.25))
        verts.append((x, 0.00, 0.00))
        verts.append((x, 0.20, 0.00))

    for i in range(4):
        faces.append((i*3, i*3 + 1, (i+1)*3 + 1, (i+1)* 3))
        faces.append(((i*3) + 1, (i*3) + 2, (i+1)*3 + 2, (i+1)*3 + 1))
        
    return verts, faces

def add_bridge(width, length):
    """returns the vertices and face components of the Bridge mesh"""
    verts = []
    faces = []
    for x in helper.float_range(-width/2.00, ((width/2.00) + (width/4.00)), width/4.00):
        verts.append((x, 0.00, 0.45))
        verts.append((x, 0.00, 0.20))
        verts.append((x, -.50, 0.20))

    for i in range(4):
        faces.append((i*3, i*3 + 1, (i+1)*3 + 1, (i+1)* 3))
        faces.append(((i*3) + 1, (i*3) + 2, (i+1)*3 + 2, (i+1)*3 + 1))
        
    return verts, faces

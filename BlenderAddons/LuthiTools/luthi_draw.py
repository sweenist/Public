import bpy
import bmesh
import luthi_helper as helper
from math import pi, sqrt, sin, cos

FB_THICKNESS = 0.1875

def add_fret(width, depth, height):
    x = width/2.00
    y = depth/2.00
    z = height
    
    verts = [(x,-y,-0.00),
            (-x,-y, 0.00),
            ( x, y,-0.00),
            (-x, y, 0.00),
            ( x/5.00,-y*0.75, z*0.65),
            ( x*0.60,-y*0.75, z*0.65),
            (-x*0.99,-y*0.75, z*0.65),
            ( x*0.99,-y*0.75, z*0.65),
            ( x*0.60, y,-0.00),
            ( x/5.00, y,-0.00),
            (-x*0.975,-0.00,z),
            ( x*0.975,-0.00,z),
            ( x*0.60,-y,-0.00),
            ( x/5.00,-y,-0.00),
            (-x/5.00, y, 0.00),
            (-x*0.60, y, 0.00),
            (-x*0.99, y*0.75, z*0.65),
            ( x*0.99, y*0.75, z*0.65),
            (-x*0.60,-y, 0.00),
            (-x/5.00,-y, 0.00),
            ( x, 0.00, 0.00),
            (-x, 0.00, 0.00),
            (-x/5.00,-y*0.75, z*0.65),
            (-x*0.60,-y*0.75, z*0.65),
            ( x*0.60,-0.00, z),
            ( x/5.00,-0.00, z),
            (-x/5.00,-0.00, z),
            (-x*0.60,-0.00, z),
            ( x*0.60, y*0.75, z*0.65),
            ( x/5.00, y*0.75, z*0.65),
            (-x/5.00, y*0.75, z*0.65),
            (-x*0.60, y*0.75, z*0.65),
            ( x*0.60, 0.00, 0.00),
            ( x/5.00, 0.00, 0.00),
            (-x/5.00, 0.00, 0.00),
            (-x*0.60, 0.00, 0.00),
            (-x*0.99,-0.00, z*0.65),
            ( x*0.99,-0.00, z*0.65,)]
            
    faces = [(23,27,10, 6),
             ( 4,25,26,22),
             (11,17,28,24),
             (27,31,16,10),
             (31,15, 3,16),
             (22,26,27,23),
             ( 5,24,25, 4),
             (24,28,29,25),
             ( 7,11,24, 5),
             ( 8, 2,20,32),
             (18, 1,21,35),
             (12, 0, 7, 5),
             (25,29,30,26),
             (26,30,31,27),
             (17, 2, 8,28),
             (28, 8, 9,29),
             (29, 9,14,30),
             (30,14,15,31),
             ( 3,15,35,21),
             (15,14,34,35),
             (14, 9,33,34),
             ( 9, 8,32,33),
             ( 0,12,32,20),
             (12,13,33,32),
             (13,19,34,33),
             (19,18,35,34),
             ( 1,18,23, 6),
             (18,19,22,23),
             (19,13, 4,22),
             (13,12, 5, 4),
             (16, 3,21,36),
             (36,21, 1, 6),
             (10,16,36),
             (10,36, 6),
             ( 7, 0,20,37),
             (37,20, 2,17),
             (11,37,17),
             (11, 7,37)]
    
    return verts, faces

def add_fret_board(fret_count, scale_length, min_width, max_width, curve_radius = None, overhang = True):

    verts = [( min_width / 2.0, 0.00, 0.00),    #1
             (-min_width / 2.0, 0.00, 0.00),    #2
             ( min_width / 2.0, 0.00, helper.FB_THICKNESS), #3
             (-min_width / 2.0, 0.00, helper.FB_THICKNESS)  #4
    ]
    faces = []
        
    #Add bottom vertices at the last fret or overhang. Negligible but...
    if overhang:
        overhang_y = helper.fret_spacer(scale_length, fret_count + 1)
    else:
        overhang_y = helper.fret_spacer(scale_length, fret_count)

    #Add Fretboard vertices
    verts.append(( max_width / 2.0, overhang_y, 0.00))  #5
    verts.append((-max_width / 2.0, overhang_y, 0.00))  #6
    verts.append(( max_width / 2.0, overhang_y, helper.FB_THICKNESS))   #7
    verts.append((-max_width / 2.0, overhang_y, helper.FB_THICKNESS))   #8
    
    #Add curvature
    if curve_radius:
        #use the fretboard_curve_face(radius width) function here
        min_z1, min_z2, min_x1, min_x2 = helper.fretboard_curve_face(curve_radius, min_width)
        max_z1, max_z2, max_x1, max_x2 = helper.fretboard_curve_face(curve_radius, max_width)
        
        verts.append(( min_x1, 0.00, min_z1))   #9
        verts.append((-min_x1, 0.00, min_z1))   #10
        verts.append(( min_x2, 0.00, min_z2))   #11
        verts.append((-min_x2, 0.00, min_z2))   #12
        verts.append(( max_x1, overhang_y, max_z1))  #13
        verts.append((-max_x1, overhang_y, max_z1))  #14
        verts.append(( max_x2, overhang_y, max_z2))  #15
        verts.append((-max_x2, overhang_y, max_z2))  #16

        verts.append(( max_x1, overhang_y, 0.00))  #17
        verts.append((-max_x1, overhang_y, 0.00))  #18
        verts.append(( max_x2, overhang_y, 0.00))  #19
        verts.append((-max_x2, overhang_y, 0.00))  #20
        
    #append faces
    if curve_radius:
        faces.extend([
            ( 3, 9,11, 1),
            ( 0,10, 8, 3),
            ( 0, 1,11,10),
            ( 3, 1, 5, 7),
            ( 7, 5,17,13),
            (13,17,19,15),
            (19,18,14,15),
            (14,18,16,12),
            (12,16, 4, 6),
            ( 4, 0, 2, 6),
            ( 2, 8,12, 6),
            (12, 8,10,14),
            (10,11,15,14),
            (15,11, 9,13),
            ( 9, 3, 7,13)
            ]
        )
    #flat fretboard
    else:
        faces.extend([
            ( 0, 2, 3, 1),
            ( 7, 5, 4, 6),
            ( 1, 3, 7, 5),
            ( 3, 7, 6, 2),
            ( 2, 6, 4, 0)
            ]
        )

    return verts, faces

def add_nut(width):    
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

import bpy
import bmesh
import luthi_helper as helper
from math import pi, sqrt, sin, cos

FB_THICKNESS = 0.1875

def add_fret(width, depth, height, radius=None):
    x = width/2.00
    y = depth/2.00
    z = height
    z_mid = height * 0.70
    
    if radius:
        z1, z2, x1, x2 = helper.fretboard_curve_face(radius, width, 0.00)
    else:
        z1 = z2 = 0.00
        x1 = x*0.60
        x2 = x / 5.0
        
    #print("At %.2f width, the z values are %.3f, %.3f" % (width, z1, z2))
    verts = [(x,-y,0.00000),
			(-x,-y,0.00000),
			(x,y,0.00000),
			(-x,y,0.00000),
			(x2,-y*0.75,z_mid + z2),
			(x1,-y*0.75,z_mid + z1),
			(-x*0.99,-y*0.75,z_mid),
			(x*0.99,-y*0.75,z_mid),
			(x1,y,z1),
			(x2,y,z2),
			(-x*0.972,y*0.24,z),
			(x*0.972,y*0.24,z),
			(x1,-y,z1),
			(x2,-y,z2),
			(-x2,y,z2),
			(-x1,y,z1),
			(-x*0.99,y*0.75,z_mid),
			(x*0.99,y*0.75,z_mid),
			(-x1,-y,z1),
			(-x2,-y,z2),
			(-x2,-y*0.75,z_mid + z2),
			(-x1,-y*0.75,z_mid + z1),
			(x1,y*0.24,z + z1),
			(x2,y*0.24,z + z2),
			(-x2,y*0.24,z + z2),
			(-x1,y*0.24,z + z1),
			(x1,y*0.75,z_mid + z1),
			(x2,y*0.75,z_mid + z2),
			(-x2,y*0.75,z_mid + z2),
			(-x1,y*0.75,z_mid + z1),
			(-x*0.99,y*0.24,z_mid),
			(x*0.99,y*0.24,z_mid),
			(-x2,-y*0.24,z + z2),
			(x1,-y*0.24,z + z1),
			(-x1,-y*0.24,z + z1),
			(-x*0.972,-y*0.24,z),
			(x2,-y*0.24,z + z2),
			(x*0.972,-y*0.24,z),
			(-x*0.99,-y*0.24,z_mid),
			(x*0.99,-y*0.24,z_mid)
            ]
            
    faces = [(34,25,10,35),
            (36,23,24,32),
            (11,17,26,22),
            (25,29,16,10),
            (29,15,3,16),
            (32,24,25,34),
            (33,22,23,36),
            (22,26,27,23),
            (37,11,22,33),
            (12,13,9,8),
            (2,17,31,39,7,0),
            (12,0,7,5),
            (23,27,28,24),
            (24,28,29,25),
            (17,2,8,26),
            (26,8,9,27),
            (27,9,14,28),
            (28,14,15,29),
            (13,19,14,9),
            (3,15,18,1),
            (19,18,15,14),
            (1,18,21,6),
            (18,19,20,21),
            (19,13,4,20),
            (13,12,5,4),
            (10,16,30),
            (35,38,6),
            (11,31,17),
            (37,7,39),
            (21,34,35,6),
            (4,36,32,20),
            (20,32,34,21),
            (5,33,36,4),
            (7,37,33,5),
            (1,6,38,30,16,3),
            (0,12,8,2),
            (11,37,39,31),
            (10,30,38,35)]
    
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

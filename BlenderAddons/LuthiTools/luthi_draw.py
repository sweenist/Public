import bpy
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
            
    faces = [(24,28,11, 7),
             ( 5,26,27,23),
             (12,18,29,25),
             (28,32,17,11),
             (32,16, 4,17),
             (23,27,28,24),
             (6 ,25,26, 5),
             (25,29,30,26),
             ( 8,12,25, 6),
             ( 9, 3,21,33),
             (19, 2,22,36),
             (13, 1, 8, 6),
             (26,30,31,27),
             (27,31,32,28),
             (18, 3, 9,29),
             (29, 9,10,30),
             (30,10,15,31),
             (31,15,16,32),
             ( 4,16,36,22),
             (16,15,35,36),
             (15,10,34,35),
             (10, 9,33,34),
             ( 1,13,33,21),
             (13,14,34,33),
             (14,20,35,34),
             (20,19,36,35),
             ( 2,19,24, 7),
             (19,20,23,24),
             (20,14, 5,23),
             (14,13, 6, 5),
             (17, 4,22,37),
             (37,22, 2, 7),
             (11,17,37),
             (11,37, 7),
             ( 8, 1,21,38),
             (38,21, 3,18),
             (12,38,18),
             (12, 8,38)]
    
    return verts, faces

def add_fret_board(fret_count, scale_length, min_width, max_width, curve_radius = None, overhang = True):

    verts = [( min_width / 2.0, 0.00, 0.00),    #0
             (-min_width / 2.0, 0.00, 0.00),    #1
             ( min_width / 2.0, 0.00, helper.FB_THICKNESS), #2
             (-min_width / 2.0, 0.00, helper.FB_THICKNESS)  #3
    ]
    faces = []
    frets = []
    
    for i in range(fret_count + 1):
        frets.append(helper.fret_spacer(scale_length, i))
        
    #Add bottom vertices at the last fret or overhang. Negligible but...
    if overhang:
        overhang_y = helper.fret_spacer(scale_length, fret_count + 1)
    else:
        overhang_y = frets[-1]
    
    #Add Fretboard vertices
    verts.append(( max_width / 2.0, overhang_y, 0.00))  #4
    verts.append((-max_width / 2.0, overhang_y, 0.00))  #5
    verts.append(( max_width / 2.0, overhang_y, helper.FB_THICKNESS))   #6
    verts.append((-max_width / 2.0, overhang_y, helper.FB_THICKNESS))   #7
    
    #Add curvature
    if curvature:
        #use the fretboard_curve_face(radius width) function here
        min_z1, min_z2, min_x1, min_x2 = helper.fretboard_curve_face(curve_radius, min_width)
        max_z1, max_z2, max_x1, max_x2 = helper.fretboard_curve_face(curve_radius, max_width)
        
        verts.append(( min_x1, 0.00, min_z1))   #8
        verts.append((-min_x1, 0.00, min_z1))   #9
        verts.append(( min_x2, 0.00, min_z2))   #10
        verts.append((-min_x2, 0.00, min_z2))   #11
        verts.append(( max_x1, frets[-1], max_z1))  #12
        verts.append((-max_x1, frets[-1], max_z1))  #13
        verts.append(( max_x2, frets[-1], max_z2))  #14
        verts.append((-max_x2, frets[-1], max_z2))  #15

    if fret_count > 5:
        #get fret 5 width
        f5_width = get_fret_width(min_width, max_width, overhang_y, frets[5])
        #add verts around fret 5
        verts.append(( mid_width / 2.0, frets[5], 0.00))    #16, #8 w/o cur
        verts.append((-mid_width / 2.0, frets[5], 0.00))    #17, #9
        verts.append(( mid_width / 2.0, frets[5], helper.FB_THICKNESS)) #18, #10
        verts.append((-mid_width / 2.0, frets[5], helper.FB_THICKNESS)) #19, #11
        
        if curvature:
            f5_z1, f5_z2, f5_x1, f5_x2 = fretboard_curve_face(curve_radius, f5_width)
            
            verts.append(( f5_x1, frets[5], f5_z1)) #20
            verts.append((-f5_x1, frets[5], f5_z1)) #21
            verts.append(( f5_x2, frets[5], f5_z2)) #22
            verts.append((-f5_x2, frets[5], f5_z2)) #23

    if fret_count > 12:
        mid_width = get_fret_width(min_width, max_width, overhang_y, frets[12])
        verts.append(( mid_width / 2.0, frets[12], 0.00))   #24, #12 w/o cur
        verts.append((-mid_width / 2.0, frets[12], 0.00))   #25, #13
        verts.append(( mid_width / 2.0, frets[12], helper.FB_THICKNESS)) #26, #14
        verts.append((-mid_width / 2.0, frets[12], helper.FB_THICKNESS)) #27, #15

        if curvature:
            mid_z1, mid_z2, mid_x1, mid_x2 = fretboard_curve_face(curve_radius, mid_width)
            
            verts.append(( mid_x1, frets[12], mid_z1))  #28
            verts.append((-mid_x1, frets[12], mid_z1))  #29
            verts.append(( mid_x2, frets[12], mid_z2))  #30
            verts.append((-mid_x2, frets[12], mid_z2))  #31
        
    #append faces. This is tricky. Options are:
    #   Curvature > 12 frets
    #   Curvature > 5 < 12 frets
    #   Curvature < 5  Who would do this? Not going to limit anyone but still...
    #   Flat      > 12 frets    Exclude 28 - 31
    #   Flat      > 5 < 12 frets
    #   Flat      < 5 frets
    faces.append()
        
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

# ##### BEGIN GPL LICENSE BLOCK #####
# 
#   LuthiTools - Add Guitar Objects to Blender's 3D View
#    Copyright (C) 2015  Ryan Sweeney
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import bmesh
from . import luthi_helper
from math import sqrt

FB_THICKNESS = 0.1875

def add_fret(width, depth, height, radius=None):
    x = width/2.00
    y = depth/2.00
    z = height
    z_mid = height * 0.70
    
    if radius:
        z1, z2, x1, x2 =  luthi_helper.fretboard_curve_face(radius, width, 0.00)
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

    verts = []
    faces = []
    frets = []
        
    #get y values of fret medians
    for i in range(fret_count + 1):
        frets.append( luthi_helper.fret_spacer(scale_length, i))
        
    #Add bottom vertices at the last fret or overhang.
    if overhang:
        frets.append( luthi_helper.fret_spacer(scale_length, fret_count + 1))

    #Add Fretboard vertices
    if curve_radius:
        for fret_y in frets:        
            cur_width =  luthi_helper.get_fret_width(min_width, max_width,frets[-1],fret_y)
            z1, z2, x1, x2 =  luthi_helper.fretboard_curve_face(curve_radius, cur_width)
            
            verts.append((-cur_width / 2.0, fret_y, 0.00))          #0
            verts.append((-cur_width / 2.0, fret_y, FB_THICKNESS))  #1
            verts.append((-x1, fret_y, z1))                         #2
            verts.append((-x2, fret_y, z2))                         #3
            verts.append(( x2, fret_y, z2))                         #4
            verts.append(( x1, fret_y, z1))                         #5
            verts.append(( cur_width / 2.0, fret_y, FB_THICKNESS))  #6
            verts.append(( cur_width / 2.0, fret_y, 0.00))          #7

        #build the end face on the fretboard
        z1, z2, x1, x2 =  luthi_helper.fretboard_curve_face(curve_radius, min_width)
        verts.append(( x1, frets[-1], 0.00))
        verts.append(( x2, frets[-1], 0.00)) 
        verts.append((-x2, frets[-1], 0.00)) 
        verts.append((-x1, frets[-1], 0.00)) 

    else:   #Flat Board
        for fret_y in frets:
            cur_width =  luthi_helper.get_fret_width(min_width, max_width,frets[-1],fret_y)
            verts.append((-cur_width / 2.0, fret_y, 0.00))
            verts.append((-cur_width / 2.0, fret_y, FB_THICKNESS))
            verts.append(( cur_width / 2.0, fret_y, FB_THICKNESS))
            verts.append(( cur_width / 2.0, fret_y, 0.00))            
        
    #append faces
    if curve_radius:
        frets.pop()
        for i in range(len(frets)):
            offset = i * 8
            for j in range(7):
                faces.append(( 1 + offset, 0 + offset, 8 + offset, 9 + offset))
                offset += 1

        #fill bottom faces
        offset = len(frets) * 8
        faces.extend([(offset, 11 + offset, 2 + offset, 1 + offset),
                      (11 + offset, 10 + offset, 3 + offset, 2 + offset),
                      (10 + offset, 9 + offset, 4 + offset, 3 + offset),
                      (9 + offset, 8 + offset, 5 + offset, 4 + offset),
                      (8 + offset, 7 + offset, 6 + offset, 5 + offset)
                    ]
                )
     
    #flat fretboard
    else:
        frets.pop()
        for i in range(len(frets)):
            offset = i * 4
            for j in range(3):
                faces.append(( 1 + offset, 0 + offset, 4 + offset, 5 + offset))
                offset += 1

        #fill bottom faces
        offset = len(verts) - 4
        faces.extend([(offset, 3 + offset, 2 + offset, 1 + offset)])

    return verts, faces

def add_nut(width):    
    verts = []
    faces = []
    
    for x in  luthi_helper.float_range(-width/2.00, ((width/2.00) + (width/4.00)), width/4.00):
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
    for x in  luthi_helper.float_range(-width/2.00, ((width/2.00) + (width/4.00)), width/4.00):
        verts.append((x, 0.00, 0.45))
        verts.append((x, 0.00, 0.20))
        verts.append((x, -.50, 0.20))

    for i in range(4):
        faces.append((i*3, i*3 + 1, (i+1)*3 + 1, (i+1)* 3))
        faces.append(((i*3) + 1, (i*3) + 2, (i+1)*3 + 2, (i+1)*3 + 1))
        
    return verts, faces

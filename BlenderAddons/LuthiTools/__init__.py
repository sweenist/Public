# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Luthier Tool",
    "author": "Ryan Sweeney",
    "version": (0, 0),
    "blender": (2, 72, 0),
    "location": "View3D > Add > Mesh > FretBoard",
    "description": "Adds a scaleable fretboard Mesh Object",
    "warning": "Still a work in progress",
    "wiki_url": "http://sweenist.wordpress.com",
    "category": "Add Mesh"
}

import luthi_helper as helper
from luthi_draw import *
import os

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, BoolProperty, IntProperty, EnumProperty

class AddFretBoard(Operator):
    """Add a Fretboard! Includes contact space for the nut and the bridge."""
    bl_idname = "mesh.custom_fretboard_add"
    bl_label = "Add Fretboard"
    bl_options = {'REGISTER', 'UNDO'}
    bl_space_type = 'VIEW_3D'
    
    expand_fret = BoolProperty(default=True)
    expand_fretboard = BoolProperty(default=True)
    expand_fretboard_width = BoolProperty(default=True)
    
    fret_count = IntProperty(
        name = "Fret Count",
        description = "The number of frets. Choose 0 for fretless",
        min = 0,
        max = 32,
        default = 22
    )    
    scale_length = FloatProperty(
        name = "Scale Length",
        description = "The length between the nut and the bridge",
        min = 1.414,
        max = 100.0,
        default = 25.5,
        precision = 3
    )    
    fret_radius = FloatProperty(
        name = "Fretboard Radius",
        description = "Fretboard curvature/falloff. Uncheck Flatten for classical flat fretboard",
        min = 2.50,
        max = 50.00,
        default = 12.00,
        precision = 3
    )    
    isFlat = BoolProperty(
        name = "Flatten",
        description = "Uncheck this to have a classical flat fretboard",
        default = False
    )
    fb_bottom_width = FloatProperty(
        name = "FB Bottom Width",
        description = "Width of fret board at the last fret. Used to determine taper",
        min = 1.625,
        max = 2.50,        
        default = 2.125,
        precision = 3
    )
    fb_overhang = BoolProperty(
        name = "FB Overhang",
        description = "check if fretboard extends past last fret",
        default = True
    )
    nut_width = FloatProperty(
        name = "Nut Width",
        description = "Width of nut",
        min = 0.005,
        max = 10.000,
        default = 1.625,
        precision = 3
    )    
    bridge_width = FloatProperty(
        name = "Bridge Width",
        description = "Width of guitar bridge",
        min = 0.005,
        max = 12.000,
        default = 2.500,
        precision = 3
    )    
    #fret dimensions
    fret_depth = FloatProperty(
        name = "Fret Depth",
        description = "Fret length from bottom to top in Y",
        default = 0.125,
        min = 0.01,
        max = 1.00,
        precision = 3
    )
    fret_height = FloatProperty(
        name = "Fret Height",
        description = "Fret height from fretboard toward string",
        default = 0.02325,
        min = 0.005,
        max = 1.25,
        precision = 6
    )
    #Inlays
    #add enum proprties
    
    def draw(self, context):
        layout = self.layout
                
        #Fret Properties Box
        box = layout.box()
        row = box.row(align=True)
        row.alignment = 'LEFT'
        row.prop(self, 'expand_fret', text="Fret Properties",
                icon="TRIA_DOWN" if self.expand_fret else "TRIA_RIGHT",
                icon_only=True,emboss=False
                )
        if self.expand_fret:
            row = box.row()
            row.label(text="Fret Count:")
            row.prop(self, 'fret_count', text="")

            row = box.row()
            row.label(text="Fret Depth:")
            row.prop(self, 'fret_depth', text="")

            row = box.row()
            row.label(text="Fret Height:")
            row.prop(self, 'fret_height', text="")
            
        #Fretboard Properties Box
        box = layout.box()
        row = box.row(align=True)

        row.alignment = 'LEFT'
        row.prop(self, 'expand_fretboard', text="Fretboard Properties",
                icon="TRIA_DOWN" if self.expand_fretboard else "TRIA_RIGHT",
                icon_only=True,emboss=False
                )
        if self.expand_fretboard:
            row = box.row()
            row.label(text="Scale Length:")
            row.prop(self,'scale_length',text='')
            
            row = box.row()
            row.label(text="Fretboard Contour:")
            row.enabled = not self.isFlat
            row.prop(self, 'fret_radius', text="")
            
            row = box.row()
            row.label(text="Flatten Fretboard:")
            row.prop(self, 'isFlat', text="")
            
            row = box.row()
            row.label(text="Fretboard Overhang:")
            row.prop(self, 'fb_overhang', text="")
            
            box.separator()
            row = box.row(align=True)
            row.alignment="LEFT"
            row.prop(self, "expand_fretboard_width", text="Fretboard Widths",
                    icon="TRIA_DOWN" if self.expand_fretboard_width else "TRIA_RIGHT",
                    icon_only=True, emboss=False
                    )
            if self.expand_fretboard_width:
                row = box.row()
                row.label(text="Nut Width:")
                row.prop(self, 'nut_width', text="")
                
                row = box.row()
                row.label(text="Fretboard Bottom Width:")
                row.prop(self, 'fb_bottom_width', text="")

                row = box.row()
                row.label(text="Bridge Width:")
                row.prop(self, 'bridge_width', text="")
                        
    def execute(self, context):        
        #Build the Nut Object
        nut_v, nut_f = add_nut(self.nut_width)        
        helper.build_mesh(context, "Nut_mesh", "Nut", nut_v, nut_f)
        
        #Build the Bridge Mesh
        bridge_v, bridge_f = add_bridge(self.bridge_width, self.scale_length)
        helper.build_mesh(context, "Bridge_mesh", "Bridge", bridge_v, bridge_f, (0, -self.scale_length, 0))
        
        #Build the fretboard
        if self.isFlat:
            fb_v, fb_f = add_fret_board(self.fret_count, self.scale_length, self.nut_width, self.fb_bottom_width, overhang = self.fb_overhang)
        else:
            fb_v, fb_f = add_fret_board(self.fret_count, self.scale_length, self.nut_width, self.fb_bottom_width, curve_radius = self.fret_radius, overhang = self.fb_overhang)
        helper.build_mesh(context, "FB_mesh", "FretBoard", fb_v, fb_f)        

        #Build the frets
        for i in range(1, self.fret_count + 1):
            if self.fb_overhang:
                max_fb_y = helper.fret_spacer(self.scale_length, self.fret_count + 1)
            else:
                max_fb_y = helper.fret_spacer(self.scale_length, self.fret_count)
            #determine some important widths and lengths for following tasks    
            fret_y_pos = helper.fret_spacer(self.scale_length, i)
            fret_width = helper.get_fret_width(self.nut_width, self.fb_bottom_width, max_fb_y, fret_y_pos)
            #Make the mesh!
            if not self.isFlat:
                f_v, f_f = add_fret(fret_width, self.fret_depth, self.fret_height, self.fret_radius)
            else:
                f_v, f_f = add_fret(fret_width, self.fret_depth, self.fret_height)
            helper.build_mesh(context, "fret_mesh_" + str(i), "Fret_" + str(i), f_v, f_f, (0.0, fret_y_pos, helper.FB_THICKNESS))
            
        return {'FINISHED'}
    
class INFO_MT_fretboard_add(bpy.types.Menu):
    #add to the "Add Mesh" menu
    bl_idname = "INFO_MT_fretboard_add"
    bl_label = "Guitar Objects"
    
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.custom_fretboard_add", text="Fretboard")

def menu_func(self, context):
    self.layout.menu("INFO_MT_fretboard_add", text="Fretboard")
    
def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
    
if __name__ == "__main__":    
    register()
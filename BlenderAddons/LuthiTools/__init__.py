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
from bpy.types import Operator, Panel
from bpy.props import FloatProperty, BoolProperty, IntProperty, EnumProperty
from mathutils import Vector

class AddFretBoard(Operator):
    """Add a Fretboard! Includes contact space for the nut and the bridge."""
    bl_idname = "mesh.custom_fretboard_add"
    bl_label = "Add Fretboard"
    bl_options = {'REGISTER', 'UNDO'}
    bl_space_type = 'VIEW_3D'
    
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
        default = 25.5
    )    
    fret_radius = FloatProperty(
        name = "Fretboard Radius",
        description = "Fretboard curvature/falloff. Uncheck Flatten for classical flat fretboard",
        min = 2.50,
        max = 50.00,
        default = 12.00,
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
        max = 2.5,
        default = 2.125
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
        max = 10.00,
        default = 1.625
    )    
    bridge_width = FloatProperty(
        name = "Bridge Width",
        description = "Width of guitar bridge",
        min = 0.005,
        max = 12.00,
        default = 2.5,
    )    
    #fret dimensions
    fret_depth = FloatProperty(
        name = "Fret Depth",
        description = "Fret length from bottom to top in Y",
        default = 0.125,
        min = 0.01,
        max = 1.00
    )
    fret_height = FloatProperty(
        name = "Fret Height",
        description = "Fret height from fretboard toward string",
        default = 0.02325,
        min = 0.005,
        max = 1.25
    )
    #Inlays
    #add enum proprties
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        col.label(text="Number of Frets:")
        col.prop(self, 'fret_count', text="")
        
        #Fret Properties Box
        box = layout.box()
        #depth
        row = box.row()
        row.prop(self, 'fret_depth')
        #height
        row = box.row()
        row.prop(self, 'fret_height')
        
        #Scale Length
        col = layout.column(align=True)
        col.label(text="Scale Length")
        col.prop(self, 'scale_length',text="")
        layout.separator()
        
        #Fret Curvature
        box = layout.box()
        box.label("Fretboard Curvature:")
        row = box.row(align=True)      
        row.alignment = 'RIGHT'
        row.prop(self, 'isFlat')
                
        row = box.row(align=True)
        row.alignment = 'RIGHT'
        row.label(text="Fretboard Contour:")
        
        row.enabled = not self.isFlat
        row.prop(self, 'fret_radius', text="")
        
        #varying widths
        box = layout.box()        
        box.label(text="Wideness")
        #Nut Width
        row = box.row()
        row.label(text="Nut:")
        row.prop(self, 'nut_width', text="Width")
        
        #Fretboard bottom Width
        row = box.row()
        row.label(text="Fretboard Bottom")
        row.prop(self, 'fb_bottom_width', text="Width")
        #Bridge Width
        row = box.row()
        row.label(text="Bridge:")
        row.prop(self, 'bridge_width', text="Width")
        
        #Fretboard extension past last fret
        row = layout.row()
        row.prop(self, 'fb_overhang')
        
    def execute(self, context):        
        #Build the Nut Mesh
        nut_v, nut_f = add_nut(self.nut_width)        
        nut_mesh = bpy.data.meshes.new("Nut_mesh")
        nut_mesh.from_pydata(nut_v, [], nut_f)
        nut_mesh.update()
        
        #Build the Bridge Mesh
        bridge_v, bridge_f = add_bridge(self.bridge_width, self.scale_length)
        bridge_mesh = bpy.data.meshes.new("Bridge_Mesh")
        bridge_mesh.from_pydata(bridge_v, [], bridge_f)
        bridge_mesh.update()
        
        #Build the fretboard
        if self.isFlat:
            fb_v, fb_f = add_fret_board(self.fret_count, self.scale_length, self.nut_width, self.fb_bottom_width, overhang = self.fb_overhang)
        else:
            fb_v, fb_f = add_fret_board(self.fret_count, self.scale_length, self.nut_width, self.fb_bottom_width, curve_radius = self.fret_radius, overhang = self.fb_overhang)
        fb_mesh = bpy.data.meshes.new("FB_Mesh")
        fb_mesh.from_pydata(fb_v, [], fb_f)
        fb_mesh.update()

        #Build the frets... hot damn, this is messy
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
            fret_mesh = bpy.data.meshes.new("fret_" + str(i))
            fret_mesh.from_pydata(f_v, [], f_f)
            fret_mesh.update()
            fret_object = bpy.data.objects.new("Fret_" + str(i), fret_mesh)
            context.scene.objects.link(fret_object)
            #move the mesh
            helper.deselect_all(context)
            fret_object.select = True            
            bpy.ops.transform.translate(value=(0.0, fret_y_pos, helper.FB_THICKNESS), constraint_axis=(False, False, False))
        
        #Create objects from the mesh and link to scene
        nut_object      = bpy.data.objects.new("Nut", nut_mesh)
        bridge_object   = bpy.data.objects.new("Bridge", bridge_mesh)
        fb_object       = bpy.data.objects.new("FretBoard", fb_mesh)
        context.scene.objects.link(nut_object)
        context.scene.objects.link(bridge_object)
        context.scene.objects.link(fb_object)
        
        #place Bridge scale length away from Nut
        helper.deselect_all(context)
        bridge_object.select = True
        bpy.ops.transform.translate(value=(0, -self.scale_length, 0), constraint_axis=(False, True, False))
        
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
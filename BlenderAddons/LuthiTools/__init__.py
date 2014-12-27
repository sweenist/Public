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
    "warning": "",
    "wiki_url": "http://sweenist.wordpress.com",
    "category": "Add Mesh"}

if "bpy" in locals():
    import imp
    imp.reload(luthiHelpers)
    imp.reload(luthiDraw)
    print("Reloaded LuthiTools Files")
else:
    #from . 
    import luthiHelpers as helper
    from luthiDraw import *
    print("Imported LuthiTools Files")

import bpy
from bpy.types import Operator, Panel
from bpy.props import FloatProperty, BoolProperty, IntProperty
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
        min = 2.5,
        max = 50.0,
        default = 12.0
    )    
    isFlat = BoolProperty(
        name = "Flatten",
        description = "Uncheck this to have a classical flat fretboard",
        default = False
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
        default = 2.188
    )
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        col.label(text="Number of Frets:")
        col.prop(self, 'fret_count', text="")
        
        col = layout.column(align=True)
        col.label(text="Scale Length")
        col.prop(self, 'scale_length',text="")
        layout.separator()
        
        #Fret Curvature
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.label(text="Fret Curvature:")
        row.prop(self, 'isFlat')
        
        col = layout.column(align=True)
        col.enabled = not self.isFlat
        col.prop(self, 'fret_radius', text="")
        layout.separator()
        
        #Nut Width
        col = layout.column(align=True)
        col.label(text="Nut Width:")
        col.prop(self, 'nut_width', text="")
        
        #Bridge Width
        col = layout.column(align=True)
        col.label(text="Bridge Width:")
        col.prop(self, 'bridge_width', text="")
        
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
        
        #Create objects from the mesh and link to scene
        nut_object      = bpy.data.objects.new("Nut", nut_mesh)
        bridge_object   = bpy.data.objects.new("Bridge", bridge_mesh)
        context.scene.objects.link(nut_object)
        context.scene.objects.link(bridge_object)
        
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
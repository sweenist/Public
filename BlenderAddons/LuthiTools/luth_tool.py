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
    "blender": (2, 71, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a scaleable fretboard Mesh Object",
    "warning": "",
    "wiki_url": "http://sweenist.wordpress.com",
    "category": "Add Mesh"}

import bpy
from bpy.types import Operator, Panel
from bpy.props import FloatProperty, BoolProperty, IntProperty
from mathutils import Vector

def add_fret_board():
    pass



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
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        col.label(text="Number of Frets:")
        col.prop(self, 'fret_count', text="")
        
        col = layout.column(align=True)
        col.label(text="Scale Length")
        col.prop(self, 'scale_length',text="")
        
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.label(text="Fret Curvature:")
        row.prop(self, 'isFlat')
        
        col = layout.column(align=True)
        col.enabled = not self.isFlat
        col.prop(self, 'fret_radius', text="")
        
    def execute(self, context):
        print(context.scene.cursor_location)
        return {'FINISHED'}
    
class INFO_MT_fretboard_add(bpy.types.Menu):
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
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
#Copyright 2014 Ryan Sweeney

bl_info = {
    "name": "3D Cursor LMB Toggle",
    "author": "Ryan Sweeney",
    "version": (1, 0),
    "blender": (2, 72, 0),
    "location": "View3D > Properties Panel > 3D Cursor",
    "description": "Adds a toggle to the 3D Cursor in the properties tab.",
    "warning": "",
    "wiki_url": "http://sweenist.wordpress.com/2014/12/22/blender-add-on-3d-cursor-toggle/",
    "category": "3D View"}

import bpy
from bpy.types import Panel
from bpy.props import BoolProperty
    
def draw_item(self, context):
    wm = context.window_manager
    keymaps = wm.keyconfigs['Blender User'].keymaps['3D View'].keymap_items
    cursor_key = keymaps['view3d.cursor3d']
    layout = self.layout
    
    col = layout.column()
    col.prop(wm, "toggle_3DKey")
    cursor_key.active = wm.toggle_3DKey

def register():
    bpy.types.VIEW3D_PT_view3d_cursor.append(draw_item)
    bpy.types.WindowManager.toggle_3DKey = BoolProperty(name="Toggle LMB", description="Controls whether the 3D cursor moves on left mouse click", default=True)
        
def unregister():
    bpy.types.VIEW3D_PT_view3d_cursor.remove(draw_item)
    del bpy.types.WindowManager.toggle_3DKey
    
if __name__ == "__main__":
    register()

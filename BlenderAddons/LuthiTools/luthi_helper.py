import bpy
from math import pi, sqrt, cos, sin

FB_THICKNESS = 0.1875
RULE_CONST   = 17.817

def deselect_all(context):
    for o in context.scene.objects:
        o.select = False
        
def fret_spacer(scale_length, fret_number):
    return -(scale_length - (scale_length/(2**(fret_number / 12))))

def float_range(start = 0.0, end = 1.0, step = 1.0):
    r = start
    while r < end:
        yield r
        r += step
        
def fretboard_curve_face(radius, width, z_offset=FB_THICKNESS):
    #returns 2 absolute values for vertices along the x-axis of fretbpard face
    #make the fretboard curve according to the supplied radius
    #a radius of 12" (30cm) is typical for most electric guitars
    #   x1 = 3/5th between middle and outer edge
    #   x2 - 1/5th between middle and outer edge
    # outer egde z will be equal to 0.1875 (3/16). This is a constant
    
    #determine the offset
    x0 = width / 2.0    #Outer Edge
    z0 = sqrt((radius**2) - (x0**2))
    offset = z0 - z_offset
    
    x1 = width * 0.30
    x2 = width * 0.10
        
    z1 = (sqrt((radius**2) - (x1**2))) - offset
    z2 = (sqrt((radius**2) - (x2**2))) - offset
    
    return z1, z2, x1, x2

def get_fret_width(min_width, max_width, max_length, current_length):
    #return the width of the fretboard at the specified fret
    variance = max_width - min_width
    current_width = min_width + (variance * (current_length/max_length))
    return current_width

def build_mesh(context, mesh_name, object_name, verts, faces, translate=None):
    _mesh = bpy.data.meshes.new(mesh_name)
    _mesh.from_pydata(verts, [], faces)
    _mesh.update()
    
    _object = bpy.data.objects.new(object_name, _mesh)
    context.scene.objects.link(_object)
    
    if translate:
        deselect_all(context)
        _object.select = True
        bpy.ops.transform.translate(value=translate)
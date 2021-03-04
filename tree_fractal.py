import bpy
import math
from mathutils import Vector, Matrix
from math import sin, cos, radians
import numpy as np

def get_gpencil(gpencil='GPencil'):
    if gpencil not in bpy.context.scene.objects:
        bpy.ops.object.gpencil_add(location=(0,0,0), type='EMPTY')
        bpy.context.scene.objects[-1].name = gpencil
    return bpy.context.scene.objects[gpencil]

def get_gpencil_layer(gpencil, layer_name='GP_Layer', clear_layer=False):
    if gpencil.data.layers and layer_name in gpencil.data.layers:
        gpencil_layer = gpencil.data.layers[layer_name]
    else:
        gpencil_layer = gpencil.data.layers.new(layer_name, set_active=True)
    if clear_layer:
        gpencil_layer.clear()
        
    return gpencil_layer

def init_gpencil(gpencil='GPencil', layer='GP_Layer', clear_layer=True):
    gpencil_obj = get_gpencil(gpencil)
    gpencil_layer = get_gpencil_layer(gpencil_obj, layer, clear_layer=clear_layer)
    return gpencil_layer


def _line(c1=[0,0,0], c2=[2,2,2]):
    newpoints = []
    newpoints.append(c1)
    newpoints.append(c2)
    return newpoints

def draw_shape(gp_frame, verts):
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'
    gp_stroke.points.add(count = len(verts))
    for i in range(len(verts)):
        gp_stroke.points[i].co = verts[i]
    return gp_stroke


def tree(x, y, angle, depth, gp_frame, delta):
    a = radians(angle)
    if depth:
        x1 = x + int(cos(a) * depth * 10.0)
        y1 = y + int(sin(a) * depth * 10.0)
        
        verts = _line([x, y, 0], [x1, y1, 0])
        stroke = draw_shape(gp_frame,verts)
        stroke.line_width = depth * 30
        tree(x1, y1, angle - delta, depth - 1, gp_frame, delta)
        tree(x1, y1, angle + delta, depth - 1, gp_frame, delta)
      

gp_layer = init_gpencil()

n_frames = 100
depth = 9
for frame in range(n_frames):
    delta = (frame / n_frames) * 90
    gp_frame = gp_layer.frames.new(frame)
    tree(0, 0, 90, depth, gp_frame, delta)

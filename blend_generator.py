import bpy
import bmesh
import os
import sys
from mathutils import Matrix, Vector
import numpy as np
import math

class ModelParameters:
    def __init__(self, radius, num_segs, num_rings, wid_joi, dep_joi, len_seg, 
                 key_stone_small_arc, key_stone_large_arc, floor_height, 
                 platform_height, platform_width, platform_depth, platform_side, 
                 rail_width, rail_height, rail_spacing):
        self.r = radius
        self.num_segs = num_segs
        self.num_rings = num_rings
        self.wid_joi = wid_joi
        self.dep_joi = dep_joi
        self.len_seg = len_seg
        self.key_stone_small_arc = key_stone_small_arc
        self.key_stone_large_arc = key_stone_large_arc
        self.floor_height = floor_height
        self.platform_height = platform_height
        self.platform_width = platform_width
        self.platform_depth = platform_depth
        self.platform_side = platform_side
        self.rail_width = rail_width
        self.rail_height = rail_height
        self.rail_spacing = rail_spacing
        self.rail_coords = np.array([[-rail_width/2 * 1.7, -len_seg/2, -r + floor_height],
                    [rail_width/2 * 1.7, -len_seg/2, -r + floor_height],
                    [rail_width/2 * 0.3, -len_seg/2, -r + floor_height + rail_height * 0.2],
                    [rail_width/2 * 0.3, -len_seg/2, -r + floor_height + rail_height * 0.7],
                    [rail_width/2, -len_seg/2, -r + floor_height + rail_height * 0.9],
                    [rail_width/2 * 0.5, -len_seg/2, -r + floor_height + rail_height],
                    [-rail_width/2 * 0.5, -len_seg/2, -r + floor_height + rail_height],
                    [-rail_width/2, -len_seg/2, -r + floor_height + rail_height * 0.9],
                    [-rail_width/2 * 0.3, -len_seg/2, -r + floor_height + rail_height * 0.7],
                    [-rail_width/2 * 0.3, -len_seg/2, -r + floor_height + rail_height * 0.2]])
    

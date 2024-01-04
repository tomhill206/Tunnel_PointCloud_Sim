import bpy
import bmesh
import os
import sys
from mathutils import Matrix, Vector
import numpy as np
import math

# Need to add project directory so Blender can access project files 
dir = '/Users/tomhill/Documents/Tunnel_PointCloud_Sim/'
if not dir in sys.path:
    sys.path.append(dir)

from utils.dictionary_maker import generate_pc
from utils.process_csv import remove_first_set_and_save

class ModelParameters:
    def __init__(self, r, num_segs, num_rings, wid_joi, dep_joi, len_seg, 
                 key_stone_small_arc, key_stone_large_arc, floor_height, 
                 platform_height, platform_width, platform_depth, platform_side, 
                 rail_width, rail_height, rail_spacing):
        self.r = r
        self.num_segs = int(num_segs)
        self.num_rings = int(num_rings)
        self.wid_joi = wid_joi
        self.dep_joi = dep_joi
        self.len_seg = len_seg
        self.key_stone_small_arc = key_stone_small_arc * np.pi/180 # Convert to radians
        self.key_stone_large_arc = key_stone_large_arc * np.pi/180 # Convert to radians
        self.floor_height = floor_height
        self.platform_height = platform_height
        self.platform_width = platform_width
        self.platform_depth = platform_depth
        self.platform_side = ['L', 'R'][int(platform_side)]
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

        self.curve_res = 32

class BlendGenerator(ModelParameters):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.floor_arc = self.calculate_chord_arc(self.r, self.floor_height)
    
    def generate_ring_edges(self):
        
        # Create dictionary defining all edges and vertices for all segments in a ring
        all_segment_data = generate_pc(self.num_segs, self.len_seg, self.r, self.wid_joi, self.dep_joi, self.key_stone_small_arc, self.key_stone_large_arc)
        
        for i in range(self.num_segs):

            obj_name = f"seg{i}"
            mesh_data = bpy.data.meshes.new(f"{obj_name}_data")
            mesh_obj = bpy.data.objects.new(obj_name, mesh_data)
            bpy.context.scene.collection.objects.link(mesh_obj)
            bm = bmesh.new()

            # Select the dict values for current segment in ring
            segment_data = all_segment_data[obj_name]

            # Add all the vertices to the mesh
            for vert in segment_data["corners"]: 
                bm.verts.new(vert)

            # Refresh mesh (avoids errors)
            bm.verts.ensure_lookup_table()
            
            # Add all edges
            for c_edge in segment_data["c_edges"]:
                self.add_circular_edge(bm, *c_edge)

            for s_edge in segment_data["s_edges"]:
                self.add_straight_edge(bm, s_edge)

            # Update the BMesh to the mesh
            bm.to_mesh(mesh_data)

            # Update the mesh with the new data
            mesh_data.update()

            bm.free()
    
    def process_objects(self, scene):
        # Iterate through all objects in the scene
        for obj in bpy.data.objects:
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')

            # Select the current object
            obj.select_set(True)

            # Set the active object to the current object
            bpy.context.view_layer.objects.active = obj

            # Call the create_faces() function
            self.create_faces()

            # Add the material to the object
            self.add_material(obj)
        
        bpy.ops.object.select_all(action='DESELECT')
        
    def create_faces(self):
        # Object has been selected already
        obj = bpy.context.active_object
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the mesh data
        mesh = bpy.context.object.data
        bm = bmesh.from_edit_mesh(mesh)
        
        all_edge_indices = self.generate_all_edge_indices()

        for i in range(6):
            edge_indices_to_select = all_edge_indices[i]

            for edge_index1, edge_index2 in zip(*edge_indices_to_select):
                bm.edges.ensure_lookup_table()
                
                bm.edges[edge_index1].select_set(True)
                bm.edges[edge_index2].select_set(True)

                bmesh.update_edit_mesh(mesh)

                bpy.ops.mesh.edge_face_add()
                
                bm.edges.ensure_lookup_table()

                # Deselect edges
                # Deselect all edges
                for edge in bm.edges:
                    edge.select_set(False)

                bmesh.update_edit_mesh(mesh)
                
        bpy.ops.object.mode_set(mode='OBJECT')
        
    def add_circular_edge(self, bm, vertex_indices, radius, center_location):
        # Get the coordinates of the specified vertices
        vertex_vectors = [bm.verts[index].co for index in vertex_indices]
        vertex_coords = [(vertex_vector.x, vertex_vector.y, vertex_vector.z) for vertex_vector in vertex_vectors]

        # Calculate start angle
        start_angle = self.angle_of_vector(vertex_coords[0])
        end_angle = self.angle_of_vector(vertex_coords[1])
        
        if end_angle < start_angle:
            end_angle += 2 * np.pi
            
        angle_between = end_angle - start_angle
        
        angles = np.linspace(start_angle, start_angle + angle_between, self.curve_res + 1)
        # Add the curved edge vertices to the mesh
        for ang in angles:
            x = center_location[0] + radius * math.sin(ang)
            y = center_location[1]
            z = center_location[2] + radius * math.cos(ang)

            # Create a new vertex at the calculated position
            new_vert = bm.verts.new((x, y, z))
            
            bm.verts.ensure_lookup_table()
            
            # Connect the new vertex to the previous one (except for the first iteration)
            if ang > start_angle:
                bm.edges.new([bm.verts[-2], new_vert])
    
    def add_straight_edge(self, bm, vertex_indices):
        bm.edges.new((bm.verts[vertex_indices[0]], bm.verts[vertex_indices[1]]))
    
    def generate_all_edge_indices(self):
        curve_res = self.curve_res
        all_edge_indices = []
        
        # To simplify
        indices_01 = [i for i in range(curve_res)]
        indices_23 = [curve_res + i for i in range(curve_res)]
        indices_45 = [2*curve_res + i for i in range(curve_res)]
        indices_67 = [3*curve_res + i for i in range(curve_res)]
        index_02 = [4*curve_res]
        index_13 = [4*curve_res + 1]
        index_46 = [4*curve_res + 2]
        index_57 = [4*curve_res + 3]
        index_04 = [4*curve_res + 4]
        index_15 = [4*curve_res + 5]
        index_26 = [4*curve_res + 6]
        index_37 = [4*curve_res + 7]
        
        # 6 faces on all the shapes
        for i in range(6):
            # Outer curve
            if i == 0:
                edge_indices_to_select = (indices_01[::-1], indices_23[::-1])
                
            # Inner curve
            elif i == 1:
                edge_indices_to_select = (indices_45[::-1], indices_67[::-1])
            
            # Front
            elif i == 2:
                edge_indices_to_select = (indices_01[::-1], indices_45[::-1])
                
            # Back
            elif i == 3:
                edge_indices_to_select = (indices_23[::-1], indices_67[::-1])
            
            # Left  
            elif i == 4:
                edge_indices_to_select = (index_02, index_46)
            
            # Right
            else:
                edge_indices_to_select = (index_13, index_57)
            
            all_edge_indices.append(edge_indices_to_select)
        
        return all_edge_indices
            
    def angle_of_vector(self, vector):

        # Convert input vectors to NumPy arrays
        vector = np.array(vector)
        
        theta_radians = 0
        vector[1] = 0
                
        # Calculate the dot product
        dot_product = np.dot((0, 0, 1), vector)
        
        # Calculate the magnitudes
        magnitude1 = np.linalg.norm((0, 0, 1))
        magnitude2 = np.linalg.norm(vector)
        
        # Calculate the cosine of the angle
        cosine_theta = dot_product / (magnitude1 * magnitude2)
        
        # Calculate the angle in radians using arccosine
        theta_radians = np.arccos(cosine_theta) 
        
        if vector[0] < 0:
            theta_radians = 2 * np.pi - theta_radians

        return theta_radians
    
    def add_material(self, obj):
        # Check if the material already exists in the scene
        material_name = "MyMaterial"
        material = bpy.data.materials.get(material_name)

        if material is None:
            # Create a new material if it doesn't exist
            material = bpy.data.materials.new(name=material_name)

        # Assign the material to the object
        if obj.data.materials:
            # If the object already has materials, replace the first one
            obj.data.materials[0] = material
        else:
            # If the object has no materials, add the material
            obj.data.materials.append(material)

    def delete_all_objects(self):
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        bpy.ops.object.select_by_type(type='MESH')    # Select all mesh objects
        bpy.ops.object.delete()
        bpy.ops.object.select_by_type(type='LIGHT')   # Select all light objects
        bpy.ops.object.delete()
        bpy.ops.object.select_by_type(type='CAMERA')  # Select the camera
        bpy.ops.object.delete()

    def rotate_all_objects(self, angle, axis):

        # Iterate through all objects in the scene
        for obj in bpy.context.scene.objects:
            # Select the current object
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)

            # Rotate the object around the specified axis
            bpy.ops.transform.rotate(value=angle, orient_axis=axis)

            # Deselect the object
            obj.select_set(False)
    
    def duplicate_and_stack_objects(self, iterations, translation, stagger_angle=0):
        # Store the original selection
        bpy.ops.object.select_all(action='SELECT')
        original_selection = bpy.context.selected_objects.copy()
        bpy.ops.object.select_all(action='DESELECT')
        
        for i in range(iterations):
            
            total_translation =  tuple(x * (i + 1) for x in translation)
            
            # Duplicate and stack the original selection
            for obj in original_selection:
                # Select the current object
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)

                # Duplicate the object with the specified translation and rotation
                bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
                bpy.ops.transform.translate(value=total_translation)

                # Stagger the rotation for each duplicated ring
                stagger_factor = 1 if i % 2 == 0 else -1
                bpy.ops.transform.rotate(value=stagger_factor * stagger_angle, orient_axis='Y')
                # Deselect the duplicated object
                bpy.context.active_object.select_set(False)

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        
        # Rotate the original ring
        for obj in original_selection:
                # Select the current object
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                
                bpy.ops.transform.rotate(value= -1 * stagger_angle, orient_axis='Y')
                
                # Deselect the duplicated object
                bpy.context.active_object.select_set(False)
        
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        
    def insert_camera(self):
        bpy.ops.object.camera_add(location=(0, 15, 0), rotation=(np.pi/2, 0, 0))
        bpy.context.scene.camera = bpy.context.object
        bpy.context.object.name = "Scanner"

    def add_custom_properties(self):
        for i, obj in enumerate(bpy.data.objects):
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')

            # Select the current object
            obj.select_set(True)

            # Set the active object to the current object
            bpy.context.view_layer.objects.active = obj

            # Add custom properties (objects are selected in groups of increasing segment number)
            obj["categoryID"] = i%self.num_rings
            obj["partID"] = i//self.num_rings
        
        bpy.ops.object.select_all(action='DESELECT')
        
    def create_prism(self, base_shape_coords, extrude_length, extrude_axis, object_name):
        """
        Create a prism in Blender.

        Args:
        - base_shape_coords: List of tuples representing the coordinates of the base shape.
        - extrude_length: Length of the prism extrusion.
        - extrude_axis: Axis along which to extrude ('X', 'Y', or 'Z').
        - object_name: Name of the new object.
        """
        
        # Convert tuples to Vectors
        base_shape_vectors = [Vector(coord) for coord in base_shape_coords]

        # Create a new BMesh
        bm = bmesh.new()

        # Add vertices to the BMesh
        vertices = [bm.verts.new(coord) for coord in base_shape_vectors]

        # Ensure the vertices form a loop for the face
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()

        # Create the base face
        base_face = bm.faces.new(vertices)

        # Extrude the base face
        if extrude_axis == 'X':
            direction = Vector((extrude_length, 0, 0))
        elif extrude_axis == 'Z':
            direction = Vector((0, 0, extrude_length))
        else:  # Default to Y if axis is not recognized
            direction = Vector((0, extrude_length, 0))

        bmesh.ops.extrude_face_region(bm, geom=[base_face])
        for v in base_face.verts:
            v.co += direction

        # Create a new mesh, add it to the scene
        mesh = bpy.data.meshes.new(object_name)
        bm.to_mesh(mesh)
        bm.free()

        obj = bpy.data.objects.new(object_name, mesh)
        bpy.context.collection.objects.link(obj)
        
        self.add_material(obj)
        
        obj["categoryID"] = -1
        obj["partID"] = -1
        
    def calculate_floor_coords(self):
        r = self.r
        len_seg = self.len_seg
        height = self.floor_height

        coords = []
        coords.append((0, -len_seg/2, -r))
        l = np.sqrt(r**2 - (r - height)*(r - height))
        coords.append((l, -len_seg/2, -r + height))
        coords.append((-l, -len_seg/2, -r + height))
        return coords

    def calculate_platform_coords(self):
        r = self.r
        len_seg = self.len_seg
        platform_height = self.platform_height
        platform_width = self.platform_width
        platform_depth = self.platform_depth
        side = self.platform_side

        coords = []

        l_top = np.sqrt(r**2 - (r - platform_height)*(r - platform_height))
        l_bottom = np.sqrt(r**2 - (r - platform_height + platform_depth)*(r - platform_height + platform_depth))
        
        if side == 'R':
            coords.append((l_top, -len_seg/2, -r + platform_height))
            coords.append((l_top - platform_width, -len_seg/2, -r + platform_height))
            coords.append((l_top - platform_width, -len_seg/2, -r + platform_height - platform_depth))
            coords.append((l_bottom, -len_seg/2, -r + platform_height - platform_depth))
        
        else:
            coords.append((-l_top, -len_seg/2, -r + platform_height))
            coords.append((-(l_top - platform_width), -len_seg/2, -r + platform_height))
            coords.append((-(l_top - platform_width), -len_seg/2, -r + platform_height - platform_depth))
            coords.append((-l_bottom, -len_seg/2, -r + platform_height - platform_depth))
            
        return coords

    def calculate_chord_arc(self, r, height):
        l = np.sqrt(np.sqrt(r**2 - (r - height)*(r - height)))
        theta = 2 * np.arcsin(l/r)
        return theta

    def generate_random_tube_coords(self):
        r = self.r
        floor_arc = self.floor_arc
        len_seg = self.len_seg

        bounds = [-np.pi/2 + floor_arc/2 + np.pi/16, 3/2 * np.pi - floor_arc/2 - np.pi/16]
        angle = np.random.uniform(bounds[0], bounds[1])
        tube_radius = np.random.uniform(0.05, 0.15)
        wall_offset = np.random.uniform(0.01, 0.2)
        
        centre_radius = r - tube_radius - wall_offset
        centre_coords = np.array([centre_radius * np.cos(angle), -len_seg/2, centre_radius * np.sin(angle)])
        
        coords = []
        for prof_ang in np.linspace(0, 2*np.pi, 20):
            x_coord = centre_coords[0] + tube_radius * np.cos(prof_ang)
            y_coord = centre_coords[1]  
            z_coord = centre_coords[2] + tube_radius * np.sin(prof_ang)

            point_coords = np.array([x_coord, y_coord, z_coord])
            coords.append(point_coords)

        return np.array(coords) 

    def add_furniture(self):

        tunnel_length = self.num_rings * self.len_seg

        # Add floor
        floor_coords = self.calculate_floor_coords()
        self.create_prism(floor_coords, tunnel_length, 'Y', 'Floor')

        # Add platform
        platform_coords = self.calculate_platform_coords()
        self.create_prism(platform_coords, tunnel_length, 'Y', 'Platform')

        # Add rails
        self.create_prism(self.rail_coords - np.array([self.rail_spacing/2, 0, 0]), tunnel_length, 'Y', 'Rail1')
        self.create_prism(self.rail_coords + np.array([self.rail_spacing/2, 0, 0]), tunnel_length, 'Y', 'Rail2')

        # Add random tubes
        for i in range(10):
            tube_coords = self.generate_random_tube_coords()
            self.create_prism(tube_coords, tunnel_length, 'Y', f'Tube{i+1}')
            
    
    def export_blend(self, file_name):
        file_path = f'/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/blender/{file_name}'
        bpy.ops.wm.save_as_mainfile(filepath=file_path)


if __name__ == "__main__":

        # Load first parameter set and remove it from the array
        parameter_sets = np.load('/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/numpy/parameter_sets.npy')

        current_parameters = parameter_sets[0]
        remove_first_set_and_save('/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/numpy/parameter_sets.npy')

        print(current_parameters)

        blend = BlendGenerator(*current_parameters)
        blend.delete_all_objects()
        blend.generate_ring_edges()
        blend.process_objects(bpy.context.scene)

        #___STAGGERING_NEEDS_TO_BE_ADDED_TO_PARAMS___

        # Rotate original ring to the centre position
        blend.rotate_all_objects(blend.key_stone_large_arc/2, 'Y')

        # Duplicate the ring with a given stagger angle
        blend.duplicate_and_stack_objects(blend.num_rings - 1, (0, blend.len_seg, 0), stagger_angle=blend.key_stone_large_arc/2)

        blend.add_custom_properties()

        blend.add_furniture()
    
        blend.insert_camera()

        blend.export_blend(f'tunnel.blend')
    

                

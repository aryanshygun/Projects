################################################################
# ADDING LIBRARIES
################################################################

import random
import math
import bpy


# Activating the previously created obj
def activate_object():
    return bpy.context.active_object

################################################################
# ADDING CAMERA
################################################################

def create_camera():
    # Create cam
    bpy.ops.object.camera_add(location=(0, 0, 10))
    
    # Essentially shortening 'bpy.context.active_object.data' to 'cam'
    cam = activate_object().data
    
    # Setting cam attributes
    cam.lens = 80
    cam.dof.use_dof = True
    # creating an empty at the world origin point and setting it to the focus point
    bpy.ops.object.empty_add()
    cam.dof.focus_object = bpy.data.objects["Empty"]
    cam.dof.aperture_fstop = 0.3
    
################################################################
# RANDOM COLORS / SELECTED COLORS
################################################################

def random_colors():
    
    random_colors_list = []
    
    # Creating 20 random colors
    for i in range(20):
        # random.random() gives a random float between 0 and 1 which is the entire color spectrum
        # we limit the float to only 5 digit long
        r_random = float("{:.5f}".format(random.random()))
        g_random = float("{:.5f}".format(random.random()))
        b_random = float("{:.5f}".format(random.random()))
        
        # The list includes sublists of 4 variables RGBA (Alpha) which is set to 1 for brightest colors
        random_colors_list.append([r_random, g_random, b_random, 1])
    
    # random.choice() randomly selects a sublist from the created list and returns it
    return random.choice(random_colors_list)

def selected_colors():
    
    # Using chat gpt to come up with a bunch of saturated pastellic colors 
    selected_colors_list = [
    (1.0, 0.2, 0.5, 1),
    (1.0, 0.6, 0.2, 1),
    (1.0, 0.9, 0.1, 1),
    (0.1, 0.8, 1.0, 1),
    (0.8, 0.2, 1.0, 1),
    (0.2, 1.0, 0.3, 1),
    (1.0, 0.5, 0.0, 1),
    (1.0, 0.0, 0.2, 1),
    (0.7, 0.3, 0.3, 1),
    (1.0, 0.1, 0.1, 1),
    (1.0, 0.8, 0.2, 1),
    (0.3, 0.7, 1.0, 1),
    (0.8, 0.2, 1.0, 1),
    (0.3, 0.7, 0.7, 1),
    (1.0, 0.4, 0.4, 1),
    (0.2, 1.0, 0.2, 1),
    (0.2, 0.6, 1.0, 1),
    (0.8, 1.0, 1.0, 1),
    (0.7, 0.1, 0.1, 1),
    (0.8, 1.0, 1.0, 1)
    ]

    return random.choice(selected_colors_list)

################################################################
# CREATING A SINGLE LAYER
################################################################

def create_layer(vertex_count, radius, location, rotation):
    
    # Adding a single 'cylinder'
    bpy.ops.mesh.primitive_cylinder_add(vertices = vertex_count, radius = radius, depth = 0.1)
    
    # Refering to the already selected object by 'obj' (easier to address instead of bpy.context.active_object)
    obj = activate_object()
    
    # Calling the attributes to the obj
    obj.location = location
    obj.rotation_euler = rotation
    

    # Adding colors
    mat = bpy.data.materials.new(name="color")
    mat.use_nodes = True
    mat.node_tree.nodes[0].inputs["Base Color"].default_value = selected_colors()
    obj.data.materials.append(mat)
    
    bpy.ops.object.modifier_add(type="BEVEL")
    obj.modifiers["Bevel"].width = 0.09
    bpy.context.object.modifiers["Bevel"].segments = 4
    bpy.ops.object.shade_smooth()


    return obj

################################################################
# CREATING ALL THE LAYERS
################################################################

def create_shape():

    # Default location/rotaion/radius & the variation factors
    location_base = (0, 0, 0)
    location_z_step = -0.1
    location_space_gap = -0.05
    
    rotation_base = (0.0, 0.0, 0.0)
    degree = 5
    rotation_z_step = math.radians(degree)
    
    radius_base = 1
    radius_step = 0.1

    
    # Number of vertices
    vertex_count = 5
    
    # Number of layers
    layer_count = int(360/degree)
    
    # Creating the shape (finally!)
    for i in range(layer_count):
        
        # Adjusting the variables for each layer depending on the value of i
        location_base = (0, 0, i * location_z_step)
        rotation_base = (0.0, 0.0, i * rotation_z_step)
 
        radius_base += radius_step
        location_space_gap += 0.1
        
        
        
        # Calling the create_layer function with the provided attributes
        layer_obj = create_layer(vertex_count, radius_base, location_base, rotation_base)
        layer_obj.keyframe_insert("rotation_euler", frame=1)
        
        
################################################################
# CALLING THE FUNCTIONS IN MAIN
################################################################


def main():
    
    #context = setup_scene()
    create_camera()        
    create_shape()


if __name__ == "__main__":
    main()
"""
How to use this script:

- First of all make sure the right layers (camera and the stuff you need) are selected.
- Rotate the Empty, so that the camera is in a 45 degree position
- Edit the parameters down there as you need them
- Run the script
"""

import bpy
import os
import os.path
from math import pi

# For buildings: 4 rotations (45, 135, 225, 315)
BUILDING = range(45, 360, 90)
# For units: 8 rotations (0, 45, 90, 135, 180, 225, 270, 315)
UNIT = range(0, 360, 45)

ANIM_KINDS = (
    NO_ANIMATION,  # No animation, static 0.png in every rotation
    FRAME_BASED,   # Frame-based animation
    LAYER_BASED,   # Layer-based animation (bottom layers (11-20)
) = range(3)

########## Parameters to edit: ##########
##########

# Whether the model rendered is a BUILDING or UNIT.
BUILDING_OR_UNIT = BUILDING

# What kind of animation to render: NO_ANIMATION, FRAME_BASED or LAYER_BASED.
ANIM_KIND = NO_ANIMATION

# Starting at 0.png (for ANIM_COUNT = 0), how many files to create.
ANIM_COUNT = 4

# How many frames to jump each step (1 = render every frame).
ANIM_STEP_SIZE = 1

# Number of frame used for the first image (0.png unless START_COUNT is set).
ANIM_START_FRAME = 0

# Add this value as offset to name of the first file:
# Start at 1.png instead of 0.png if START_COUNT = 1.
START_COUNT = 0

# Name of directory to save files in.
# Common names are "idle", "idle_full" and "work".
DIR_NAME = "idle"

# Path to the rendered output directory.
# Starting with // means relative to .blend file location.
DIR_PATH = "//final/"

##########
########## You should not need to edit anything from here on. ##########


def create_paths():
    real_path = bpy.path.abspath(DIR_PATH)
    work_path = real_path + DIR_NAME + "/"

    if not os.path.exists(real_path):
        os.mkdir(real_path)
    if not os.path.exists(work_path):
        os.mkdir(work_path)

    return work_path


def start_rendering(where):
    for rotation in BUILDING_OR_UNIT:
        final_path = where + str(rotation) + "/"
        if not os.path.exists(final_path):
            os.mkdir(final_path)

        # Don't confuse the layer index if START_COUNT is not 0
        layer_i = 0
        i = START_COUNT
        current_frame = ANIM_START_FRAME

        if ANIM_KIND == LAYER_BASED:
            bpy.context.scene.layers[0] = True
            for x in range(1, 19):
                bpy.context.scene.layers[x] = False
            bpy.context.scene.layers[10] = True

        while True:
            bpy.ops.render.render()
            result = bpy.context.blend_data.images['Render Result']
            result.save_render(final_path+str(i)+".png")
            layer_i += 1
            i += 1
            if i > ANIM_COUNT:
                break
            if ANIM_KIND == FRAME_BASED:
                current_frame += ANIM_STEP_SIZE
                bpy.context.scene.frame_set(current_frame)
            elif ANIM_KIND == LAYER_BASED:
                bpy.context.scene.layers[layer_i+10] = True
                bpy.context.scene.layers[layer_i+9] = False

        # Our Empty that will rotate the camera must be named 'Empty'.
        bpy.context.scene.objects['Empty'].rotation_euler[2] -= pi / 2


where = create_paths()
start_rendering(where)

# Undo the rotation
bpy.context.scene.objects['Empty'].rotation_euler[2] += 2 * pi

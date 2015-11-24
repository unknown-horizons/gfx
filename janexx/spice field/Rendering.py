"""
How to use this script:

- First of all make sure the right layers (camera and the stuff you need) are selected.
- Rotate the Empty, so that the camera is in a 45 grade position
- Edit the parameters down there as you need them
- Run the script
"""


import bpy
import os, math


ANIM_KIND = 0 # No animation
#ANIM_KIND = 1 # Frame based
#ANIM_KIND = 2 # layer based (bottom layers (11-20)

ANIM_COUNT = 4 #Will make files: 0.png, 1.png, ... (0= only 0.png)
ANIM_STEP_SIZE = 1 #Frames to jump (1=every frame)
ANIM_START_FRAME = 0 #Frames for the first image (0.png)
START_COUNT=0 #Will add this value to the first file (if f.e. 1: 0.png -> 1.png)
DIR_NAME = "idle" #dir to safe in
#DIR_NAME = "idle_full"
#DIR_NAME = "work"
DIR_PATH = "//final/" #Path to the rendered output



#DO some path creation stuff
real_path = bpy.path.abspath(DIR_PATH)

if not os.path.exists(real_path):
    os.mkdir(real_path)
    
work_path = real_path + DIR_NAME + "/"
   
if not os.path.exists(work_path):
    os.mkdir(work_path)


#START RENDERING



#we need 4 directions (for buildings)
for round in range(0,4):
    current_rotation=45+(round*90) # get right direction
    
    final_path = work_path + str(current_rotation) + "/"
    
    if not os.path.exists(final_path):
        os.mkdir(final_path)
    
    layer_i = 0 # don't confuse the layer stuff if anouther start_count
    i = START_COUNT;
    current_frame = ANIM_START_FRAME
    
    if ANIM_KIND==2:
        bpy.context.scene.layers[0] = True
        for x in range(1,19):
            bpy.context.scene.layers[x] = False
        bpy.context.scene.layers[10] = True

    while True:
        bpy.ops.render.render()
        bpy.context.blend_data.images['Render Result'].save_render(final_path+str(i)+".png")
        layer_i += 1
        i += 1
        if i > ANIM_COUNT:
            break
        if ANIM_KIND==1:
            current_frame += ANIM_STEP_SIZE
            bpy.context.scene.frame_set(current_frame)
        if ANIM_KIND==2:
            bpy.context.scene.layers[layer_i+10] = True
            bpy.context.scene.layers[layer_ti+9] = False
    
    #Our Empty that will rotate the camera must be named 'Empty'
    bpy.context.scene.objects['Empty'].rotation_euler[2]-=math.pi/2
    
#undo the rotation 
bpy.context.scene.objects['Empty'].rotation_euler[2]+=math.pi*2
from vray.utils import *
import maya.cmds as cmds
import os

# Get the current workspace and scene information
ws = cmds.workspace(q=True, act=True)
scene_path = cmds.file(q=True, sn=True)
scene_name = os.path.basename(scene_path)

# Check the currently active render layer
current_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)

# Remove 'rs_' prefix from the current layer name if it exists
if current_layer.startswith('rs_'):
    current_layer = current_layer[3:]

# Set the output directory based on the modified layer name
if current_layer != 'defaultRenderLayer':
    rd = f'{ws}/images/{current_layer}/deep/'
else:
    rd = f'{ws}/images/deep/'

# Generate the file path
if current_layer != 'defaultRenderLayer':
    fn = f'{scene_name}_{current_layer}_deep.exr'
else:
    fn = f'{scene_name}_deep.exr'
o = os.path.join(rd, fn)

# Create the directory if it does not exist
if not os.path.exists(rd):
    os.makedirs(rd)

# Create and set the OutputDeepWriter
odw = create('OutputDeepWriter', 'vrayOutputDeepWriter')
odw.set('file', str(o))

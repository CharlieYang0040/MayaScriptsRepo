import maya.cmds as cmds
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check if the node is a file node
def is_file_node(node_name):
    try:
        node_type = cmds.nodeType(node_name)
        return node_type == "file"
    except:
        return False

# to selected files or all files
confirmRange = cmds.confirmDialog(
                title='Confirmation', 
                message=f'Do you want to make the changes to the selected or all file nodes?',
                button=['Selected', 'All'], 
                defaultButton='Yes', 
                cancelButton='No', 
                dismissString='No'
                )
if confirmRange == 'Selected':
    selected_nodes = cmds.ls(sl = True)
else:
    selected_nodes = cmds.ls()

# Find all file nodes
texture_filenames = []
fileNodeList = []
for node in selected_nodes:
    is_file = is_file_node(node)
    if is_file:
        fileNodeList.append(node)
fileNodeList = list(set(fileNodeList))
logging.info("FileNodeList: %s", fileNodeList)

# Set the wrong texture path
default_texture_path = "C:/Users/PRO/Documents/"
wrong_texture_path = input(f"Enter the wrong texture path (default: {default_texture_path}): ") or default_texture_path
if wrong_texture_path == "" or wrong_texture_path == None:
    wrong_texture_path = default_texture_path

# Set the project path
yes_all = False
scene_project_path = cmds.workspace(q=True, rd=True)

# Set texture filename
for file_node in fileNodeList:
    if file_node:
        texture_filename = cmds.getAttr(file_node + ".fileTextureName")
        texture_filenames.append(texture_filename)
        logging.info("Texture filename: %s", texture_filename)
    else:
        logging.warning("No file node found for node: %s", file_node)
    # Replace the wrong texture path with the project path
    for texture_filename in texture_filenames:
        modified_texture_filename = texture_filename.replace(wrong_texture_path, scene_project_path)
    logging.info("Modified texture filename: %s", modified_texture_filename)
    # Confirm the changes
    if texture_filename != modified_texture_filename:
        if not yes_all:
            confirm = cmds.confirmDialog(
                title='Confirmation', 
                message=f'Do you want to make the changes?\nOriginal Path:\n{texture_filename}\n=>\nModified Project Path:\n{modified_texture_filename}', 
                button=['Yes', 'YesAll', 'No', 'Cancel'], 
                defaultButton='Yes', 
                cancelButton='Cancel', 
                dismissString='No'
                )
            if confirm == 'YesAll':
                yes_all = True
        if confirm == 'Yes' or yes_all:
            # Set the new texture path
            cmds.setAttr(file_node + ".fileTextureName", modified_texture_filename, type="string")
        if confirm == 'No':
            logging.info("Changes not made.")
        if confirm == 'Cancel':
            logging.info("Changes cancelled by user.")
            break

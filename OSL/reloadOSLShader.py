import maya.cmds as cmds
import vray.utils

def reload_vray_osl_shader(shader_name):
    """
    Reload the specified V-Ray OSL shader node.
    
    :param shader_name: The name of the VRayOSL node in Maya.
    """
    # Find the VRayOSL node
    if not cmds.objExists(shader_name):
        print(f"Node {shader_name} does not exist.")
        return
    
    # Get the current OSL file path
    osl_file_path = cmds.getAttr(f"{shader_name}.shaderFile")
    
    # Reload the OSL shader
    if osl_file_path:
        print(f"Reloading OSL shader from: {osl_file_path}")
        vray.utils.loadOSO(osl_file_path)
        print(f"OSL shader {shader_name} reloaded successfully.")
    else:
        print(f"No OSL shader file path found for node {shader_name}.")

# Example usage:
reload_vray_osl_shader("VRayOSL1")

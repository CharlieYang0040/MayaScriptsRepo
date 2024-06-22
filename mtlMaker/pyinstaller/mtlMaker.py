import os
import re
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore

class MtlMakerUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MtlMakerUI, self).__init__(parent)
        self.setWindowTitle('mtlMaker by CGUSLAB')
        self.resize(300, 500)
        self.setup_ui()
        self.project_path = cmds.workspace(q=True, rd=True) + 'sourceimages/'

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.log = QtWidgets.QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.search_btn = QtWidgets.QPushButton('Search')
        self.search_btn.clicked.connect(self.populate_list)
        layout.addWidget(self.search_btn)

        self.folder_list = QtWidgets.QListWidget()
        self.folder_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        layout.addWidget(self.folder_list)

        self.make_btn = QtWidgets.QPushButton('Make')
        self.make_btn.clicked.connect(self.create_materials)
        layout.addWidget(self.make_btn)

        self.help_btn = QtWidgets.QPushButton('Help')
        self.help_btn.clicked.connect(self.open_help)
        layout.addWidget(self.help_btn)

    def log_message(self, message):
        self.log.append(message)

    def populate_list(self):
        self.log_message("Searching for folders...")
        self.folder_list.clear()
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.exr', '.tif', '.tiff', '.tx')):
                    self.folder_list.addItem(root.replace(self.project_path, ''))
                    break
        self.log_message("Folders loaded.")

    def create_materials(self):
        selected_folders = self.folder_list.selectedItems()
        if not selected_folders:
            self.log_message("No folder selected.")
            return
        for item in selected_folders:
            self.log_message(f"Processing folder: {item.text()}")
            full_path = os.path.join(self.project_path, item.text())
            textures = self.find_textures(full_path)
            self.connect_textures(textures, item.text())
        self.log_message("Material creation completed.")

    def find_textures(self, path):
        texture_types = {
            'BaseColor': ['BaseColor', 'Diffuse'],
            'Roughness': ['Roughness', 'Glossiness'],
            'Metallic': ['Metallic', 'Specular'],
            'Normal': ['Normal']
        }
        textures = {key: None for key in texture_types.keys()}
        for file in os.listdir(path):
            file_lower = file.lower()
            for key, aliases in texture_types.items():
                for alias in aliases:
                    if alias.lower() in file_lower and not textures[key]:
                        textures[key] = os.path.join(path, file)
                        break
        return textures

    def connect_textures(self, textures, asset_name):
        self.log_message("Creating VRayMtl node...")
        vrayMtl_node = cmds.shadingNode('VRayMtl', asShader=True, name=f'{asset_name}_vrayMtl')
        sg = cmds.sets(name=f"{vrayMtl_node}SG", empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr(f"{vrayMtl_node}.outColor", f"{sg}.surfaceShader")

        for texture_type, texture_path in textures.items():
            if texture_path:
                file_node = cmds.shadingNode('file', asTexture=True)
                place2d_node = cmds.shadingNode('place2dTexture', asUtility=True)
                self.connect_place2d(file_node, place2d_node)
                cmds.setAttr(f"{file_node}.fileTextureName", texture_path, type="string")

                if re.search(r'\.[0-9]{4}\.', texture_path):
                    cmds.setAttr(f"{file_node}.uvTilingMode", 3)  # UDIM 모드 설정

                self.log_message(f"Connecting {texture_type} texture...")
                if texture_type == 'BaseColor':
                    cmds.connectAttr(f"{file_node}.outColor", f"{vrayMtl_node}.color")
                elif texture_type == 'Roughness':
                    cmds.connectAttr(f"{file_node}.outAlpha", f"{vrayMtl_node}.reflectionGlossiness")
                elif texture_type == 'Metallic':
                    if 'specular' in texture_path.lower():
                        cmds.connectAttr(f"{file_node}.outColor", f"{vrayMtl_node}.reflectionColor")
                        cmds.setAttr(f"{vrayMtl_node}.metalness", 0)
                        cmds.setAttr(f"{vrayMtl_node}.useRoughness", 0)
                    else:
                        cmds.connectAttr(f"{file_node}.outAlpha", f"{vrayMtl_node}.metalness")
                        cmds.setAttr(f"{vrayMtl_node}.reflectionColor", 1, 1, 1, type='double3')
                        cmds.setAttr(f"{vrayMtl_node}.useRoughness", 1)
                elif texture_type == 'Normal':
                    cmds.connectAttr(f"{file_node}.outColor", f"{vrayMtl_node}.bumpMap")
                    cmds.setAttr(f"{vrayMtl_node}.bumpMapType", 1)  # Normal map in tangent space

        self.log_message(f"VRayMtl node for {asset_name} completed.")

    def open_help(self):
        url = "https://github.com/CharlieYang0040/MayaScriptsRepo/tree/main/mtlMaker"  # Replace with your actual URL
        cmds.launch(webBrowser=url)

    def connect_place2d(self, file_node, place2d_node):
        attrs = [
            "coverage", "translateFrame", "rotateFrame", "mirrorU", "mirrorV",
            "stagger", "wrapU", "wrapV", "repeatUV", "offset", "rotateUV",
            "noiseUV", "vertexUvOne", "vertexUvTwo", "vertexUvThree", "vertexCameraOne"
        ]
        for attr in attrs:
            cmds.connectAttr(f"{place2d_node}.{attr}", f"{file_node}.{attr}", f=True)
        cmds.connectAttr(f"{place2d_node}.outUV", f"{file_node}.uvCoord", f=True)
        cmds.connectAttr(f"{place2d_node}.outUvFilterSize", f"{file_node}.uvFilterSize", f=True)

def show_ui():
    global mtl_maker_ui
    try:
        mtl_maker_ui.close()
        mtl_maker_ui.deleteLater()
    except:
        pass
    mtl_maker_ui = MtlMakerUI()
    mtl_maker_ui.show()

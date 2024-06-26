import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore

class RenamerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RenamerUI, self).__init__(parent)
        self.setWindowTitle("Renamer by CGUSLAB")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setup_ui()
        self.rename_button.clicked.connect(self.rename_nodes)

    def setup_ui(self):
        """Setup the UI layout and widgets."""
        self.mode_label = QtWidgets.QLabel("Mode:")
        self.all_nodes_radio = QtWidgets.QRadioButton("All Nodes")
        self.selected_nodes_radio = QtWidgets.QRadioButton("Selected Nodes")
        self.hierarchy_radio = QtWidgets.QRadioButton("Hierarchy")
        self.selected_nodes_radio.setChecked(True)
        
        self.find_label = QtWidgets.QLabel("Find:")
        self.find_text = QtWidgets.QLineEdit()
        
        self.replace_label = QtWidgets.QLabel("Replace:")
        self.replace_text = QtWidgets.QLineEdit()
        
        self.rename_button = QtWidgets.QPushButton("Rename")
        self.log_text = QtWidgets.QTextEdit(readOnly=True)

        self.help_btn = QtWidgets.QPushButton('Help')
        self.help_btn.clicked.connect(self.open_help)
        
        layout = QtWidgets.QVBoxLayout()
        mode_layout = QtWidgets.QHBoxLayout()
        mode_layout.addWidget(self.mode_label)
        mode_layout.addWidget(self.all_nodes_radio)
        mode_layout.addWidget(self.selected_nodes_radio)
        mode_layout.addWidget(self.hierarchy_radio)
        
        find_layout = QtWidgets.QHBoxLayout()
        find_layout.addWidget(self.find_label)
        find_layout.addWidget(self.find_text)
        
        replace_layout = QtWidgets.QHBoxLayout()
        replace_layout.addWidget(self.replace_label)
        replace_layout.addWidget(self.replace_text)
        
        layout.addLayout(mode_layout)
        layout.addLayout(find_layout)
        layout.addLayout(replace_layout)
        layout.addWidget(self.rename_button)
        layout.addWidget(self.log_text)
        layout.addWidget(self.help_btn)
        
        self.setLayout(layout)

    def open_help(self):
        url = "https://github.com/CharlieYang0040/MayaScriptsRepo/tree/main/renamer"
        cmds.launch(webBrowser=url)

    def collect_and_sort_nodes(self, mode):
        """Collect nodes based on the selected mode and sort them by depth."""
        if mode == "all":
            nodes = cmds.ls(long=True)
        elif mode == "selected":
            nodes = cmds.ls(selection=True, long=True)
        elif mode == "hierarchy":
            nodes = []
            for node in cmds.ls(selection=True, long=True):
                nodes.extend(cmds.listRelatives(node, allDescendents=True, fullPath=True) or [])
            nodes.extend(cmds.ls(selection=True, long=True))
        nodes.sort(key=lambda x: x.count('|'))
        return nodes

    def rename_nodes(self):
        """Rename nodes based on the user inputs and selected mode."""
        mode = "all" if self.all_nodes_radio.isChecked() else "selected" if self.selected_nodes_radio.isChecked() else "hierarchy"
        nodes = self.collect_and_sort_nodes(mode)
        
        while nodes:
            current_max_depth = max(node.count('|') for node in nodes)
            current_layer_nodes = [node for node in nodes if node.count('|') == current_max_depth]
            nodes = [node for node in nodes if node.count('|') != current_max_depth]
            
            for node in current_layer_nodes:
                if self.process_node(node):
                    self.log_text.append(f"Renamed: {node}")
                else:
                    self.log_text.append(f"Skipped: {node}")
            self.log_text.append("Completed processing for the current layer.")
        
        self.log_text.append("Renaming process completed.")

    def process_node(self, node):
        """Process individual node for renaming."""
        node_type = cmds.nodeType(node)
        if node_type == 'mesh':
            return False
        
        path_parts = node.split('|')
        last_part = path_parts[-1]
        new_part = last_part.replace(self.find_text.text(), self.replace_text.text().replace(" ", "_"))
        
        if new_part != last_part:
            full_new_name = '|'.join(path_parts[:-1] + [new_part])
            if not cmds.objExists(full_new_name):
                try:
                    cmds.rename(node, new_part)
                    return True
                except RuntimeError as e:
                    self.log_text.append(f"Failed to rename: {node} due to {str(e)}")
            else:
                self.log_text.append(f"Name clash avoided: {node} not renamed to {full_new_name}")
        return False

def show_ui():
    global renamer_ui
    try:
        renamer_ui.close()
        renamer_ui.deleteLater()
    except:
        pass
    renamer_ui = RenamerUI()
    renamer_ui.show()

if __name__ == "__main__":
    show_ui()

import os, sys, re, subprocess, webbrowser, logging
import maya.standalone
import maya.cmds as cmds
from PySide2.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QComboBox, QDoubleSpinBox, QMessageBox, QTextEdit, QListWidget, QListWidgetItem, QProgressBar
)
from PySide2.QtGui import QIcon, QColor
from PySide2.QtCore import Qt, QTimer

class QTextEditLogger(logging.Handler):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        msg = self.format(record)
        self.text_edit.append(msg)

class BatchScriptGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupLogging()

    def setupLogging(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        text_edit_logger = QTextEditLogger(self.logTextBox)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        text_edit_logger.setFormatter(formatter)
        self.logger.addHandler(text_edit_logger)

    def initUI(self):
        self.setWindowTitle('V-Ray Batch Script Generator for Maya by CGUSLAB')
        self.setGeometry(300, 300, 800, 600)

        mainLayout = QHBoxLayout()
        leftLayout = QVBoxLayout()

        # Read me button
        self.readMeBtn = QPushButton('Read me', self)
        self.readMeBtn.clicked.connect(self.openReadMe)
        leftLayout.addWidget(self.readMeBtn)

        # Scene file input
        self.sceneFileLabel = QLabel('Scene File:', self)
        leftLayout.addWidget(self.sceneFileLabel)
        self.sceneFileInput = QLineEdit(self)
        leftLayout.addWidget(self.sceneFileInput)
        self.sceneFileBtn = QPushButton('Browse...', self)
        self.sceneFileBtn.clicked.connect(self.browseSceneFile)
        leftLayout.addWidget(self.sceneFileBtn)

        # Project path input
        self.projectPathLabel = QLabel('Project Path:', self)
        leftLayout.addWidget(self.projectPathLabel)
        self.projectPathInput = QLineEdit(self)
        self.projectPathInput.setReadOnly(False)
        leftLayout.addWidget(self.projectPathInput)

        # Output directory input
        self.outputDirLabel = QLabel('Output Directory:', self)
        leftLayout.addWidget(self.outputDirLabel)
        self.outputDirInput = QLineEdit(self)
        self.outputDirInput.setReadOnly(False)
        leftLayout.addWidget(self.outputDirInput)

        # Open Scene File button
        self.openSceneBtn = QPushButton('Open Scene File', self)
        self.openSceneBtn.clicked.connect(self.openSceneFile)
        leftLayout.addWidget(self.openSceneBtn)

        # Progress bar for loading scene
        self.progressBar = QProgressBar(self)
        leftLayout.addWidget(self.progressBar)

        # Image format
        self.imageFormatLabel = QLabel('Image Format:', self)
        leftLayout.addWidget(self.imageFormatLabel)
        self.imageFormatInput = QComboBox(self)
        self.imageFormatInput.addItems(["default", "exr", "png", "jpg", "tif", "tiff"])
        self.imageFormatInput.setCurrentText("default")
        leftLayout.addWidget(self.imageFormatInput)

        # Resolution
        self.resolutionLabel = QLabel('Resolution:', self)
        leftLayout.addWidget(self.resolutionLabel)
        self.resolutionInput = QComboBox(self)
        self.resolutionInput.addItems(["default", "HD 1080 (1920x1080)", "HD 720 (1280x720)", "4K (3840x2160)", "Custom"])
        self.resolutionInput.setCurrentText("default")
        leftLayout.addWidget(self.resolutionInput)
        resLayout = QHBoxLayout()
        self.xResInput = QDoubleSpinBox(self)
        self.xResInput.setRange(1, 9999)
        self.yResInput = QDoubleSpinBox(self)
        self.yResInput.setRange(1, 9999)
        resLayout.addWidget(QLabel('X:'))
        resLayout.addWidget(self.xResInput)
        resLayout.addWidget(QLabel('Y:'))
        resLayout.addWidget(self.yResInput)
        leftLayout.addLayout(resLayout)
        self.resolutionInput.currentIndexChanged.connect(self.updateResolution)

        # Animation frames
        self.startFrameLabel = QLabel('Start Frame:', self)
        leftLayout.addWidget(self.startFrameLabel)
        self.startFrameInput = QDoubleSpinBox(self)
        self.startFrameInput.setRange(0, 9999)
        leftLayout.addWidget(self.startFrameInput)
        self.endFrameLabel = QLabel('End Frame:', self)
        leftLayout.addWidget(self.endFrameLabel)
        self.endFrameInput = QDoubleSpinBox(self)
        self.endFrameInput.setRange(0, 9999)
        leftLayout.addWidget(self.endFrameInput)

        # Render layers
        self.renderLayersLabel = QLabel('Render Layers:', self)
        leftLayout.addWidget(self.renderLayersLabel)
        self.renderLayersList = QListWidget(self)
        self.renderLayersList.setSelectionMode(QListWidget.MultiSelection)
        leftLayout.addWidget(self.renderLayersList)

        # Generate script button
        self.generateBtn = QPushButton('Generate Batch Script', self)
        self.generateBtn.clicked.connect(self.generateScript)
        leftLayout.addWidget(self.generateBtn)

        # Execute script button
        self.executeBtn = QPushButton('Execute Batch Script', self)
        self.executeBtn.clicked.connect(self.executeScript)
        leftLayout.addWidget(self.executeBtn)

        # Log Text Box
        self.logTextBox = QTextEdit(self)
        self.logTextBox.setReadOnly(True)
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(QLabel('Log:', self))
        rightLayout.addWidget(self.logTextBox)

        # Set main layout
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        self.setLayout(mainLayout)

        # Customizing the UI with dark mode and pastel tones
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
            }
            QLabel {
                font-size: 11px;
                font-weight: bold;
                color: #f8f9fa;
            }
            QPushButton {
                background-color: #4f83cc;
                color: white;
                font-size: 11px;
                border: none;
                border-radius: 3px;
                padding: 6px 12px;
                margin: 2px 1px;
            }
            QLineEdit, QComboBox, QDoubleSpinBox, QListWidget, QTextEdit {
                background-color: #3e3e3e;
                border: 1px solid #4f4f4f;
                border-radius: 3px;
                padding: 4px;
                font-size: 11px;
                color: #f8f9fa;
            }
            QPushButton:hover {
                background-color: #3e6cae;
            }
            #openSceneBtn {
                background-color: #70a56e;
            }
            #openSceneBtn:hover {
                background-color: #5d8c5a;
            }
            #readMeBtn {
                background-color: #f4a261;
                color: black;
            }
            #readMeBtn:hover {
                background-color: #e69044;
            }
        """)

        # Set special object names for specific buttons
        self.openSceneBtn.setObjectName("openSceneBtn")
        self.readMeBtn.setObjectName("readMeBtn")

    def openReadMe(self):
        webbrowser.open("https://github.com/CharlieYang0040/MayaScriptsRepo/tree/main/vrayBatchScriptGenUI")

    def browseSceneFile(self):
        sceneFile, _ = QFileDialog.getOpenFileName(self, 'Select Scene File', '', 'Maya Files (*.ma *.mb)')
        if sceneFile:
            self.logger.debug(f'Selected scene file: {sceneFile}')
            self.sceneFileInput.setText(sceneFile)
            self.initializeProjectAndOutput(sceneFile)

    def initializeProjectAndOutput(self, sceneFile):
        # Set project path
        projectPath = os.path.dirname(os.path.dirname(sceneFile))
        self.logger.debug(f'Setting project path: {projectPath}')
        self.projectPathInput.setText(projectPath)

        # Set output directory
        outputDir = os.path.join(projectPath, "images")
        self.logger.debug(f'Setting output directory: {outputDir}')
        self.outputDirInput.setText(outputDir)

    def openSceneFile(self):
        sceneFile = self.sceneFileInput.text()
        if not sceneFile:
            QMessageBox.warning(self, 'Input Error', 'Please provide a scene file path.')
            return

        self.logger.debug(f'Opening scene file: {sceneFile}')
        # Initialize Maya and open the scene file
        self.progressBar.setValue(0)
        QTimer.singleShot(100, lambda: self.updateProgress(10, "Initializing Maya standalone"))
        maya.standalone.initialize(name='python')

        QTimer.singleShot(200, lambda: self.updateProgress(30, "Opening scene file"))
        cmds.file(sceneFile, open=True, force=True)

        # Get image format
        QTimer.singleShot(300, lambda: self.updateProgress(50, "Getting image format"))
        image_format = cmds.getAttr('vraySettings.imageFormatStr')
        format_map = {
            "exr": "exr",
            "png": "png",
            "jpg": "jpg",
            "tif": "tiff",
            "tiff": "tiff",
        }
        ext = format_map.get(image_format, 'default')
        idx = self.imageFormatInput.findText(ext)
        if idx != -1:
            self.logger.debug(f'Setting image format: {ext}')
            self.imageFormatInput.setCurrentIndex(idx)

        # Get resolution
        QTimer.singleShot(400, lambda: self.updateProgress(70, "Getting resolution"))
        width = cmds.getAttr("defaultResolution.width")
        height = cmds.getAttr("defaultResolution.height")
        self.logger.debug(f'Setting resolution: {width}x{height}')
        self.xResInput.setValue(width)
        self.yResInput.setValue(height)

        # Get start and end frames
        QTimer.singleShot(500, lambda: self.updateProgress(80, "Getting frame range"))
        startFrame = cmds.getAttr("defaultRenderGlobals.startFrame")
        endFrame = cmds.getAttr("defaultRenderGlobals.endFrame")
        self.logger.debug(f'Setting start frame: {startFrame}')
        self.logger.debug(f'Setting end frame: {endFrame}')
        self.startFrameInput.setValue(startFrame)
        self.endFrameInput.setValue(endFrame)

        # Get render layers
        QTimer.singleShot(600, lambda: self.updateProgress(90, "Getting render layers"))
        render_layers = cmds.ls(type='renderLayer')
        render_layers = [layer for layer in render_layers if cmds.getAttr(layer + ".renderable")]
        self.logger.debug(f'Found render layers: {render_layers}')
        self.renderLayersList.clear()
        for layer in render_layers:
            item = QListWidgetItem(layer)
            self.renderLayersList.addItem(item)

        QTimer.singleShot(700, lambda: self.updateProgress(100, "Scene file loaded"))

    def updateProgress(self, value, message):
        self.progressBar.setValue(value)
        self.logger.debug(message)

    def updateResolution(self):
        preset = self.resolutionInput.currentText()
        if preset == "HD 1080 (1920x1080)":
            self.xResInput.setValue(1920)
            self.yResInput.setValue(1080)
        elif preset == "HD 720 (1280x720)":
            self.xResInput.setValue(1280)
            self.yResInput.setValue(720)
        elif preset == "4K (3840x2160)":
            self.xResInput.setValue(3840)
            self.yResInput.setValue(2160)
        elif preset == "Custom":
            self.xResInput.setValue(0)
            self.yResInput.setValue(0)

    def generateScript(self):
        projectPath = self.projectPathInput.text()
        sceneFile = self.sceneFileInput.text()
        outputDir = self.outputDirInput.text()
        imageFormat = self.imageFormatInput.currentText()
        xRes = int(self.xResInput.value())
        yRes = int(self.yResInput.value())
        startFrame = int(self.startFrameInput.value())
        endFrame = int(self.endFrameInput.value())
        selectedLayers = [item.text() for item in self.renderLayersList.selectedItems()]

        if not projectPath or not sceneFile or not outputDir:
            QMessageBox.warning(self, 'Input Error', 'Please provide all necessary inputs.')
            return
        
        # Maya version check
        base_path = 'C:\\Program Files\\Autodesk'
        version_pattern = re.compile(r'Maya(\d{4})')
        maya_versions = []
        for entry in os.listdir(base_path):
            match = version_pattern.search(entry)
            if match:
                maya_versions.append(match.group(1))
        highest_version = max(maya_versions, key=int)

        renderCommand = f'"C:\\Program Files\\Autodesk\\Maya{highest_version}\\bin\\Render.exe" -r vray -proj "{projectPath}" '
        renderCommand += f'-rd "{outputDir}" '

        if imageFormat != "default":
            renderCommand += f'-of "{imageFormat}" '
        if self.resolutionInput.currentText() != "default":
            renderCommand += f'-x {xRes} -y {yRes} '

        if startFrame or endFrame:
            renderCommand += f'-s {startFrame} -e {endFrame} '

        if selectedLayers:
            renderCommand += f'-rl {",".join(selectedLayers)} '

        renderCommand += f'"{sceneFile}"\npause'

        # Save the script to the project path
        self.script_path = os.path.join(projectPath, 'batch_render_script.bat')

        try:
            with open(self.script_path, 'w') as file:
                file.write(renderCommand)
            self.logger.debug(f'Script saved at: {self.script_path}')
            QMessageBox.information(self, 'Script Generated', f'Batch render script has been generated successfully at {self.script_path}!')
        except Exception as e:
            self.logger.error(f'Error saving script: {e}')
            QMessageBox.critical(self, 'Error', f'Failed to save script: {e}')

    def executeScript(self):
        if hasattr(self, 'script_path') and os.path.isfile(self.script_path):
            try:
                subprocess.Popen(f'start cmd /k {self.script_path}', shell=True)
                self.logger.debug(f'Executed script: {self.script_path}')
            except Exception as e:
                self.logger.error(f'Error executing script: {e}')
                QMessageBox.critical(self, 'Error', f'Failed to execute script: {e}')
        else:
            QMessageBox.warning(self, 'Execution Error', 'No script found to execute. Please generate the script first.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BatchScriptGenerator()
    ex.show()
    sys.exit(app.exec_())

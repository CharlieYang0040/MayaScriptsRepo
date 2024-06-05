import os
import subprocess
import re

try:
    import vrayBatchScriptGenUI
except ImportError:
    pass

def find_maya_path():
    base_path = r'C:\Program Files\Autodesk'
    if not os.path.exists(base_path):
        print(f"Cannot find Autodesk directory at {base_path}")
        return None

    maya_dirs = [d for d in os.listdir(base_path) if re.match(r'Maya\d{4}', d)]
    if not maya_dirs:
        print("Cannot find any Maya installation in the Autodesk directory.")
        return None

    # 최신 버전의 Maya 디렉토리를 선택
    maya_dirs.sort(reverse=True)
    maya_dir = maya_dirs[0]
    mayapy_path = os.path.join(base_path, maya_dir, 'bin', 'mayapy.exe')

    if not os.path.exists(mayapy_path):
        print(f"Cannot find mayapy.exe at {mayapy_path}")
        return None
    
    return mayapy_path

def run_script_with_mayapy(mayapy_path, script_path):
    subprocess.run([mayapy_path, script_path])

if __name__ == "__main__":
    mayapy_path = find_maya_path()
    if mayapy_path:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_to_run = os.path.join(current_dir, 'vrayBatchScriptGenUI.py')
        run_script_with_mayapy(mayapy_path, script_to_run)

import os, sys
import shutil
import getpass
from pathlib import Path

def find_semicolon_outside_strings(lines):
    semicolon_positions = []
    in_string = False
    escape = False
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '\\' and not escape:
                escape = True
                continue
            if char in ('"', "'") and not escape:
                in_string = not in_string
            if char == ';' and not in_string:
                semicolon_positions.append((i, j))
            escape = False
    return semicolon_positions

def add_or_replace_shelf_button(mel_file_path, button_code, label):
    # 읽기 모드로 파일 열기
    with open(mel_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 기존의 -label "mtlMaker" 버튼을 찾기
    start_index = None
    end_index = None
    semicolon_positions = find_semicolon_outside_strings(lines)
    for i, line in enumerate(lines):
        if label in line:
            start_index = i - 15
            # 버튼 블록의 끝(;) 찾기
            for pos in semicolon_positions:
                if pos[0] >= start_index:
                    end_index = pos[0]
                    break
            break

    # 기존 버튼 블록 제거
    if start_index is not None and end_index is not None:
        del lines[start_index:end_index+1]

    # global proc shelf_Custom block의 끝을 찾기
    insert_index = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == '}':
            insert_index = i
            break

    if insert_index is None:
        print("global proc shelf_Custom block not found.")
        return

    # 새로운 버튼 코드를 지정된 위치에 삽입
    lines.insert(insert_index, f"    {button_code}\n")

    # 수정된 내용을 파일에 쓰기
    with open(mel_file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    print("Button code added or replaced successfully.")

def copy_script_file(src, dest):
    try:
        shutil.copy(src, dest)
        print(f"{os.path.basename(src)} copied to {dest}")
    except IOError as e:
        print(f"Unable to copy file. {e}")

def main():
    user_name = getpass.getuser()
    maya_versions = [d for d in os.listdir(f'C:\\Users\\{user_name}\\Documents\\maya') if d.isdigit()]
    
    button_code = '''
    shelfButton
        -enableCommandRepeat 1
        -flexibleWidthType 3
        -flexibleWidthValue 32
        -enable 1
        -width 35
        -height 34
        -manage 1
        -visible 1
        -preventOverride 0
        -annotation "Run renamer.show_ui" 
        -enableBackground 0
        -backgroundColor 0 0 0 
        -highlightColor 0.321569 0.521569 0.65098 
        -align "center" 
        -label "renamer" 
        -labelOffset 0
        -rotation 0
        -flipX 0
        -flipY 0
        -useAlpha 1
        -font "plainLabelFont" 
        -imageOverlayLabel "renamer"
        -overlayLabelColor 0.8 0.8 0.8 
        -overlayLabelBackColor 0 0 0 0.5 
        -image "namespaceEditor.png" 
        -image1 "namespaceEditor.png" 
        -style "iconOnly" 
        -marginWidth 0
        -marginHeight 1
        -command "python(\\"import renamer; renamer.show_ui()\\")" 
        -sourceType "mel" 
        -commandRepeatable 1
        -flat 1
    ;'''

    label = '-label "renamer"'

    for version in maya_versions:
        mel_file_path = f'C:\\Users\\{user_name}\\Documents\\maya\\{version}\\prefs\\shelves\\shelf_Custom.mel'
        if os.path.exists(mel_file_path):
            add_or_replace_shelf_button(mel_file_path, button_code.strip(), label)

        scripts_path = f'C:\\Users\\{user_name}\\Documents\\maya\\{version}\\scripts'
        if not os.path.exists(scripts_path):
            os.makedirs(scripts_path)

        src_script_path = Path(sys._MEIPASS) / 'renamer.py'
        copy_script_file(src_script_path, scripts_path)

if __name__ == "__main__":
    main()

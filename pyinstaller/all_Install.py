import os, sys
import shutil
import getpass
from pathlib import Path

def read_mel_content(mel_file_path):
    with open(mel_file_path, 'r', encoding='utf-8') as file:
        return file.read()

def ensure_correct_bracing(pre_button_content):
    content = pre_button_content.strip()
    if not content.startswith("global proc shelf_Custom () {\n"):
        content = "global proc shelf_Custom () {\n" + content
    if content.endswith("}"):
        content = content.rstrip("}").rstrip()
    return content

def find_pre_button_content(mel_content):
    button_start_index = mel_content.find("shelfButton")
    return mel_content[:button_start_index] if button_start_index != -1 else mel_content

def parse_shelf_buttons(mel_content):
    buttons = []
    in_string = False
    current_quote = None
    button_start_index = mel_content.find("shelfButton")

    if button_start_index == -1:
        return buttons

    i = button_start_index
    while i < len(mel_content):
        if mel_content[i] in ("'", '"') and (i == 0 or mel_content[i-1] != '\\'):
            if not in_string:
                in_string = True
                current_quote = mel_content[i]
            elif current_quote == mel_content[i]:
                in_string = False
                current_quote = None
        elif mel_content[i] == ';' and not in_string:
            button_end_index = i + 1
            button_data = mel_content[button_start_index:button_end_index]
            buttons.append(button_data)
            button_start_index = mel_content.find("shelfButton", button_end_index)
            if button_start_index == -1:
                break
            i = button_start_index - 1
        i += 1

    return buttons

def update_buttons(existing_buttons, new_button, button_label):
    updated_buttons = [button for button in existing_buttons if button_label not in button]
    updated_buttons.append(new_button)
    return updated_buttons

def write_updated_mel_file(mel_file_path, pre_button_content, updated_buttons):
    with open(mel_file_path, 'w', encoding='utf-8') as file:
        print(f"updated_buttons2: {updated_buttons}")
        file.write(pre_button_content)
        for button in updated_buttons:
            print(f"writing button: {button}")
            file.write(f"{button}\n")
        file.write("}\n")

def copy_script_file(src, dest):
    try:
        shutil.copy(src, dest)
        print(f"{os.path.basename(src)} copied to {dest}")
    except IOError as e:
        print(f"Unable to copy file. {e}")

def main():
    user_name = getpass.getuser()
    maya_versions = [d for d in os.listdir(f'C:\\Users\\{user_name}\\Documents\\maya') if d.isdigit()]
    plugins = [
        {
            "name": "renamer",
            "image": "namespaceEditor.png",
            "command": "import renamer; renamer.show_ui()"
        },
        {
            "name": "mtlMaker",
            "image": "materialEditor.png",
            "command": "import mtlMaker; mtlMaker.show_ui()"
        },
        {
            "name": "texturePathReplacer",
            "image": "copyUV.png",
            "command": "import texturePathReplacer; texturePathReplacer.create_ui()"
        }
    ]

    for version in maya_versions:
        mel_file_path = f'C:\\Users\\{user_name}\\Documents\\maya\\{version}\\prefs\\shelves\\shelf_Custom.mel'
        if not os.path.exists(mel_file_path):
            with open(mel_file_path, 'w') as file:
                file.write('global proc shelf_Custom () {\n    global string $gBuffStr;\n    global string $gBuffStr0;\n    global string $gBuffStr1;\n\n    ;\n}\n')
            print(f"Created new shelf_Custom.mel at {mel_file_path}")

        for plugin in plugins:
            new_button_code = f'''
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
                -annotation "Run {plugin["command"]}" 
                -enableBackground 0
                -backgroundColor 0 0 0 
                -highlightColor 0.321569 0.521569 0.65098 
                -align "center" 
                -label "{plugin["name"]}" 
                -labelOffset 0
                -rotation 0
                -flipX 0
                -flipY 0
                -useAlpha 1
                -font "plainLabelFont" 
                -imageOverlayLabel "{plugin["name"]}"
                -overlayLabelColor 0.8 0.8 0.8 
                -overlayLabelBackColor 0 0 0 0.5 
                -image "{plugin["image"]}" 
                -image1 "{plugin["image"]}" 
                -style "iconOnly" 
                -marginWidth 0
                -marginHeight 1
                -command "python(\\"{plugin["command"]}\\")" 
                -sourceType "mel" 
                -commandRepeatable 1
                -flat 1
            ;'''

            mel_content = read_mel_content(mel_file_path)
            mel_content = ensure_correct_bracing(mel_content)
            pre_button_content = find_pre_button_content(mel_content)
            existing_buttons = parse_shelf_buttons(mel_content)
            button_label = f'-label "{plugin["name"]}"'
            updated_buttons = update_buttons(existing_buttons, new_button_code.strip(), button_label)
            write_updated_mel_file(mel_file_path, pre_button_content, updated_buttons)

        scripts_path = f'C:\\Users\\{user_name}\\Documents\\maya\\{version}\\scripts'
        if not os.path.exists(scripts_path):
            os.makedirs(scripts_path)
        
        for plugin in plugins:
            src_script_path = Path(sys._MEIPASS) / f'{plugin["name"]}.py'
            copy_script_file(src_script_path, scripts_path)

if __name__ == "__main__":
    main()
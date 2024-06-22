import os
import shutil

def get_maya_paths(maya_version):
    user_profile = os.path.expanduser('~')
    maya_script_path = os.path.join(user_profile, 'Documents', 'maya', maya_version, 'scripts')
    maya_shelf_path = os.path.join(user_profile, 'Documents', 'maya', maya_version, 'prefs', 'shelves')
    return maya_script_path, maya_shelf_path

def copy_plugin_file(source_file, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    shutil.copy(source_file, destination_folder)
    print(f"Copied {source_file} to {destination_folder}")

def update_shelf_script(shelf_file_path, plugin_name):
    # Read the existing shelf file content
    with open(shelf_file_path, 'r') as file:
        lines = file.readlines()

    # Identify if the shelf button for the plugin already exists
    button_exists = False
    new_lines = []
    inside_target_block = False

    for line in lines:
        if f'-label "{plugin_name}"' in line:
            button_exists = True
            inside_target_block = True
        if inside_target_block and line.strip() == ';':
            inside_target_block = False
            continue
        if not inside_target_block:
            new_lines.append(line)

    # Add the new plugin button if it doesn't exist
    if not button_exists:
        shelf_script_content = f"""
shelfButton
    -parent "MyCustomShelf"
    -label "{plugin_name}"
    -annotation "Launch {plugin_name}"
    -command "python(\\"import {plugin_name}; {plugin_name}.create_ui()\\")"
    -image1 "commandButton.png"
    -style "iconOnly";
"""
        new_lines.insert(len(new_lines) - 1, shelf_script_content)

    # Write the updated content back to the shelf file
    with open(shelf_file_path, 'w') as file:
        file.writelines(new_lines)
    print(f"Updated shelf script at {shelf_file_path}")

def main():
    maya_version = input("Maya 버전을 입력해주세요 (예: 2018, 2023 등): ")
    plugin_name = 'texturePathReplacer'  # 플러그인 이름
    current_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_file = os.path.join(current_dir, f'{plugin_name}.py')  # 플러그인 파일의 전체 경로
    
    maya_script_path, maya_shelf_path = get_maya_paths(maya_version)
    
    # 플러그인 파일 복사
    copy_plugin_file(plugin_file, maya_script_path)
    
    # 쉘프 파일 업데이트
    shelf_file_path = os.path.join(maya_shelf_path, 'shelf_Custom.mel')
    if os.path.exists(shelf_file_path):
        update_shelf_script(shelf_file_path, plugin_name)
    else:
        print(f"Error: {shelf_file_path} does not exist.")
    
    print("Installation complete.")

if __name__ == "__main__":
    main()

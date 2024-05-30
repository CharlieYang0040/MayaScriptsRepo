import maya.cmds as cmds
import logging
import os, shutil, re, glob, webbrowser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 경로 수정 함수
def fix_path_separators(path):
    return path.replace("\\", "/")

# 시스템 사용자 이름을 가져옴
user_name = os.getlogin()

# 로그 출력 함수
def log_message(message, level=logging.INFO):
    logging.log(level, message)
    cmds.scrollField('logScrollField', edit=True, insertText=message + '\n')

# GitHub 링크 함수
def open_github_link(*args):
    webbrowser.open("https://github.com/CharlieYang0040/MayaScriptsRepo/blob/main/texturePathReplacer.py")

# 잘못된 텍스처 경로를 자동으로 설정하는 함수
def get_auto_wrong_texture_path(selected_node):
    if selected_node:
        texture_path = fix_path_separators(cmds.getAttr(selected_node + ".fileTextureName"))
        return os.path.dirname(texture_path) + "/"
    else:
        cmds.warning("Please select at least one node from the list to auto detect the path.")
        return None

# file 노드를 검색하여 필터링하는 함수
def search_file_nodes():
    file_nodes = cmds.ls(type='file')
    scene_project_path = fix_path_separators(cmds.workspace(q=True, rd=True))
    invalid_file_nodes = [node for node in file_nodes if not fix_path_separators(cmds.getAttr(node + ".fileTextureName")).startswith(scene_project_path)]
    return invalid_file_nodes

# 파일 노드 리스트를 갱신하는 함수
def populate_file_nodes_list(*args):
    invalid_file_nodes = search_file_nodes()
    cmds.textScrollList('fileNodesList', edit=True, removeAll=True)
    for node in invalid_file_nodes:
        cmds.textScrollList('fileNodesList', edit=True, append=node)
    log_message("File nodes list updated.")

# 파일 경로 생성 함수
def create_group_folder(dst):
    filename = os.path.basename(dst)
    group_name = filename.split('_')[0]
    group_folder = os.path.join(os.path.dirname(dst), group_name)
    if not os.path.exists(group_folder):
        os.makedirs(group_folder)
    return fix_path_separators(os.path.join(group_folder, filename))

# 텍스처 경로를 수정하는 함수
def modify_texture_path(texture_filename, wrong_texture_path, scene_project_path):
    modified_texture_filename = texture_filename.replace(wrong_texture_path, scene_project_path)
    if "sourceimages" not in modified_texture_filename:
        modified_texture_filename = scene_project_path + "sourceimages/" + os.path.basename(modified_texture_filename)
    return modified_texture_filename

# 파일 복사 함수
def copy_file(src, dst):
    try:
        final_dst = create_group_folder(dst)
        shutil.copy(src, final_dst)
        log_message(f"File copied to: {final_dst}")
        return final_dst
    except Exception as e:
        log_message(f"Failed to copy file: {str(e)}", logging.ERROR)
        cmds.warning(f"Failed to copy file: {str(e)}")
        return None

# UDIM 방식 파일 복사 함수
def copy_udim_files(src_pattern, dst_pattern):
    try:
        src_files = glob.glob(re.sub(r'\.\d{4}\.', '.*.', src_pattern))
        copied_paths = []
        for src in src_files:
            src = fix_path_separators(src)
            dst = src.replace(find_base_path(src_pattern), find_base_path(dst_pattern))
            final_dst = create_group_folder(dst)
            shutil.copy(src, final_dst)
            log_message(f"File copied to: {final_dst}")
            copied_paths.append(final_dst)
        return copied_paths
    except Exception as e:
        log_message(f"Failed to copy UDIM files: {str(e)}", logging.ERROR)
        cmds.warning(f"Failed to copy UDIM files: {str(e)}")
        return []

# 정규 표현식을 사용하여 숫자 네자리를 찾는 함수
def find_base_path(filepath):
    filepath = fix_path_separators(filepath)
    match = re.search(r'(.*?)(\.\d{4}\.)', filepath)
    if match:
        return match.group(1)
    else:
        return None

# 파일 경로를 수정하고 복사하는 함수
def handle_texture_path(file_node, wrong_texture_path, scene_project_path, copy_files, yes_all_copy):
    texture_filename = fix_path_separators(cmds.getAttr(file_node + ".fileTextureName"))
    modified_texture_filename = modify_texture_path(texture_filename, wrong_texture_path, scene_project_path)

    # UV Tiling Mode가 설정되어 있는지 확인
    uv_tiling_mode = cmds.getAttr(file_node + ".uvTilingMode")
    if uv_tiling_mode != 0:
        src_pattern = fix_path_separators(texture_filename)
        dst_pattern = fix_path_separators(modified_texture_filename)
        if copy_files:
            if not yes_all_copy:
                confirm_copy = cmds.confirmDialog(
                    title='Copy Confirmation', 
                    message=f'Are you sure you want to copy the UDIM files?\nOriginal Path Pattern:\n{src_pattern}\n=>\nNew Path Pattern:\n{dst_pattern}', 
                    button=['Yes', 'Yes All', 'No', 'Cancel'], 
                    defaultButton='Yes', 
                    cancelButton='Cancel', 
                    dismissString='No'
                )
                if confirm_copy == 'Yes All':
                    yes_all_copy = True
                if confirm_copy == 'Cancel':
                    log_message("Copy operation cancelled by user.")
                    return modified_texture_filename, yes_all_copy
                if confirm_copy in ['Yes', 'Yes All']:
                    copied_paths = copy_udim_files(src_pattern, dst_pattern)
                    if copied_paths:
                        modified_texture_filename = copied_paths[0]
            else:
                copied_paths = copy_udim_files(src_pattern, dst_pattern)
                if copied_paths:
                    modified_texture_filename = copied_paths[0]
    else:
        if copy_files:
            if not yes_all_copy:
                confirm_copy = cmds.confirmDialog(
                    title='Copy Confirmation', 
                    message=f'Are you sure you want to copy the file?\nOriginal Path:\n{texture_filename}\n=>\nNew Path:\n{modified_texture_filename}', 
                    button=['Yes', 'Yes All', 'No', 'Cancel'], 
                    defaultButton='Yes', 
                    cancelButton='Cancel', 
                    dismissString='No'
                )
                if confirm_copy == 'Yes All':
                    yes_all_copy = True
                if confirm_copy == 'Cancel':
                    log_message("Copy operation cancelled by user.")
                    return modified_texture_filename, yes_all_copy
                if confirm_copy in ['Yes', 'Yes All']:
                    copied_path = copy_file(texture_filename, modified_texture_filename)
                    if copied_path:
                        modified_texture_filename = copied_path
            else:
                copied_path = copy_file(texture_filename, modified_texture_filename)
                if copied_path:
                    modified_texture_filename = copied_path

    return texture_filename, modified_texture_filename, yes_all_copy

# 선택한 노드의 텍스처 경로를 수정하는 함수
def replace_texture_paths(wrong_texture_path, nodes, copy_files=False, individual_paths=False):
    def is_file_node(node_name):
        return cmds.nodeType(node_name) == "file"

    use_scene_path = cmds.checkBox('useScenePathCheckbox', query=True, value=True)
    if use_scene_path:
        scene_project_path = fix_path_separators(cmds.workspace(q=True, rd=True))
    else:
        scene_project_path = fix_path_separators(cmds.textField('customScenePathField', query=True, text=True))

    if not wrong_texture_path:
        wrong_texture_path = f"C:/Users/{user_name}/Documents/maya/projects/default"
    wrong_texture_path = fix_path_separators(wrong_texture_path)

    yes_all = False
    yes_all_copy = False
    fileNodeList = [node for node in nodes if is_file_node(node)]

    for file_node in fileNodeList:
        if individual_paths:
            wrong_texture_path = get_auto_wrong_texture_path(file_node)

        texture_filename, modified_texture_filename, yes_all_copy = handle_texture_path(file_node, wrong_texture_path, scene_project_path, copy_files, yes_all_copy)
        if texture_filename != modified_texture_filename:
            if not yes_all:
                confirm = cmds.confirmDialog(
                    title='Confirmation', 
                    message=f'Are you sure you want to change the path?\nOriginal Path:\n{texture_filename}\n=>\nNew Path:\n{modified_texture_filename}', 
                    button=['Yes', 'Yes All', 'No', 'Cancel'], 
                    defaultButton='Yes', 
                    cancelButton='Cancel', 
                    dismissString='No'
                )
                if confirm == 'Yes All':
                    yes_all = True
                if confirm == 'Cancel':
                    log_message("Operation cancelled by user.")
                    return
            if confirm in ['Yes', 'Yes All']:
                cmds.setAttr(file_node + ".fileTextureName", modified_texture_filename, type="string")
                log_message(f"Texture path changed for node: {file_node}")
            else:
                log_message("Changes not made.")

# 선택된 노드가 없을 때 오류 메시지 표시
def replace_texture_paths_for_selected(wrong_texture_path, selected_nodes, copy_files):
    if not selected_nodes:
        cmds.warning("Please select at least one node from the list.")
    else:
        individual_paths = cmds.checkBox('individualPathsCheckbox', query=True, value=True)
        replace_texture_paths(wrong_texture_path, selected_nodes, copy_files, individual_paths)

# UI 생성 함수
def create_ui():
    if cmds.window("textureReplacerWindow", exists=True):
        cmds.deleteUI("textureReplacerWindow")

    window = cmds.window("textureReplacerWindow", title="Texture Path Replacer", widthHeight=(600, 1100))
    main_layout = cmds.columnLayout(adjustableColumn=True)
    
    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 400), (2, 200)], parent=main_layout)
    
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.button(label="Texture Path Replacer (open help)", command=open_github_link)

    cmds.separator(height=20, style='in')

    cmds.text(label="Enter the wrong texture path:")
    path_field = cmds.textField('pathField')
    
    cmds.button('autoPathCheckbox', label='Detect wrong texture path', command=lambda *args: get_auto_wrong_texture_path(
        cmds.textScrollList('fileNodesList', query=True, selectItem=True)[0]))
    
    cmds.checkBox('individualPathsCheckbox', label='Auto detect wrong texture paths', value=True)

    cmds.separator(height=10, style='in')
    
    cmds.checkBox('useScenePathCheckbox', label='Use Scene Project Path', value=True)
    cmds.text(label="Or enter a custom scene project path:")
    custom_scene_path_field = cmds.textField('customScenePathField')
    
    cmds.separator(height=10, style='in')
    
    cmds.button(
        label="Search File Nodes", 
        command=populate_file_nodes_list,
        backgroundColor=(0.35, 0.5, 0.65),
    )

    cmds.textScrollList('fileNodesList', numberOfRows=8, allowMultiSelection=True)
    
    cmds.separator(height=10, style='in')

    cmds.button(label="Replace Texture Paths for All Nodes", command=lambda *args: replace_texture_paths(
        cmds.textField(path_field, query=True, text=True), 
        search_file_nodes(),
        cmds.checkBox('copyFilesCheckbox', query=True, value=True)
    ))
    
    cmds.button(label="Replace Texture Paths for Selected Nodes", command=lambda *args: replace_texture_paths_for_selected(
        cmds.textField(path_field, query=True, text=True), 
        cmds.textScrollList('fileNodesList', query=True, selectItem=True),
        cmds.checkBox('copyFilesCheckbox', query=True, value=True)
    ))

    cmds.button(label="Replace Texture Paths for Selected Nodes in Maya", command=lambda *args: replace_texture_paths(
        cmds.textField(path_field, query=True, text=True),
        cmds.ls(selection=True),
        cmds.checkBox('copyFilesCheckbox', query=True, value=True)
    ))

    cmds.checkBox('copyFilesCheckbox', label='Copy files to new path', value=True)
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='in')
    
    cmds.columnLayout(adjustableColumn=True, width=200)
    cmds.text(label="Log")
    log_scroll_field = cmds.scrollField('logScrollField', editable=False, wordWrap=True, height=300)

    cmds.separator(height=10, style='out')
    
    cmds.showWindow(window)

create_ui()

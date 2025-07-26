import maya.cmds as cmds
import logging
import os, shutil, re, glob, webbrowser

# 로깅 기본 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 경로 구분자를 슬래시(/)로 통일하는 함수
def fix_path_separators(path):
    """경로의 백슬래시를 슬래시로 변환합니다."""
    return path.replace("\\", "/")

# 시스템 사용자 이름을 가져옴
user_name = os.getlogin()

# UI의 로그 필드에 메시지를 출력하는 함수
def log_message(message, level=logging.INFO):
    """지정된 레벨로 로깅하고 UI의 로그 필드에 메시지를 추가합니다."""
    logging.log(level, message)
    # UI가 존재할 때만 업데이트 시도
    if cmds.scrollField('logScrollField', query=True, exists=True):
        cmds.scrollField('logScrollField', edit=True, insertText=message + '\n')

# GitHub 도움말 링크를 여는 함수
def open_github_link(*args):
    """스크립트의 GitHub 저장소 페이지를 엽니다."""
    webbrowser.open("https://github.com/CharlieYang0040/MayaScriptsRepo/tree/main/texturePathReplacer")

# 선택된 노드에서 잘못된 텍스처 경로를 자동으로 감지하는 함수
def get_auto_wrong_texture_path(selected_node):
    """선택된 파일 노드의 텍스처 경로에서 디렉토리 부분을 추출하여 반환합니다."""
    if selected_node:
        texture_path = fix_path_separators(cmds.getAttr(selected_node + ".fileTextureName"))
        wrong_path = os.path.dirname(texture_path) + "/"
        # UI의 경로 필드에 자동으로 채워넣기
        if cmds.textField('pathField', query=True, exists=True):
            cmds.textField('pathField', edit=True, text=wrong_path)
        log_message(f"Detected path: {wrong_path}")
        return wrong_path
    else:
        cmds.warning("Please select at least one node from the list to auto detect the path.")
        return None

# file 노드를 검색하여 필터링하는 함수 (체크박스 기능 추가)
def search_file_nodes():
    """씬에서 file 노드를 검색합니다. 체크박스 상태에 따라 프로젝트 외부 경로만 필터링하거나 모든 노드를 반환합니다."""
    # '프로젝트 내 파일 노드 포함' 체크박스의 상태를 가져옴
    include_all = cmds.checkBox('includeProjectFilesCheckbox', query=True, value=True)
    
    file_nodes = cmds.ls(type='file')

    if include_all:
        # 체크박스가 선택된 경우, 모든 file 노드를 반환
        log_message(f"Found {len(file_nodes)} total file nodes (including nodes within the project).")
        return file_nodes
    else:
        # 체크박스가 해제된 경우, 기존 로직대로 프로젝트 외부 경로를 가진 노드만 필터링
        scene_project_path = fix_path_separators(cmds.workspace(q=True, rd=True))
        invalid_file_nodes = [node for node in file_nodes if not fix_path_separators(cmds.getAttr(node + ".fileTextureName")).startswith(scene_project_path)]
        log_message(f"Found {len(invalid_file_nodes)} file nodes with paths outside the project.")
        return invalid_file_nodes

# 파일 노드 리스트를 UI에 채우는 함수
def populate_file_nodes_list(*args):
    """search_file_nodes 함수를 호출하여 UI의 리스트를 갱신합니다."""
    file_nodes_to_list = search_file_nodes()
    cmds.textScrollList('fileNodesList', edit=True, removeAll=True)
    for node in file_nodes_to_list:
        cmds.textScrollList('fileNodesList', edit=True, append=node)
    log_message("File nodes list updated.")

# 텍스처 이름 기반으로 하위 폴더를 생성하는 함수
def create_group_folder(dst):
    """파일 이름의 접두사를 기반으로 그룹 폴더를 생성하고 최종 파일 경로를 반환합니다."""
    filename = os.path.basename(dst)
    try:
        group_name = filename.split('_')[0]
        group_folder = os.path.join(os.path.dirname(dst), group_name)
        if not os.path.exists(group_folder):
            os.makedirs(group_folder)
        return fix_path_separators(os.path.join(group_folder, filename))
    except IndexError:
        # 파일 이름에 '_'가 없는 경우, 상위 폴더에 바로 저장
        return dst


# 텍스처 경로를 새 경로로 수정하는 함수
def modify_texture_path(texture_filename, wrong_texture_path, scene_project_path):
    """잘못된 경로를 새 프로젝트 경로로 교체합니다."""
    modified_texture_filename = texture_filename.replace(wrong_texture_path, scene_project_path)
    # 경로에 'sourceimages'가 없으면 추가
    if "sourceimages" not in modified_texture_filename.lower():
        modified_texture_filename = os.path.join(scene_project_path, "sourceimages", os.path.basename(modified_texture_filename))
    return fix_path_separators(modified_texture_filename)

# 단일 파일을 복사하는 함수
def copy_file(src, dst):
    """소스 경로의 파일을 목적지 경로로 복사합니다."""
    try:
        final_dst = create_group_folder(dst)
        # 복사할 폴더가 없으면 생성
        os.makedirs(os.path.dirname(final_dst), exist_ok=True)
        shutil.copy(src, final_dst)
        log_message(f"File copied to: {final_dst}")
        return final_dst
    except Exception as e:
        log_message(f"Failed to copy file: {str(e)}", logging.ERROR)
        cmds.warning(f"Failed to copy file: {str(e)}")
        return None

# UDIM 파일을 복사하는 함수
def copy_udim_files(src_pattern, dst_pattern):
    """UDIM 패턴을 가진 모든 파일을 찾아 복사합니다."""
    try:
        # <UDIM> 태그를 와일드카드 숫자로 변환
        udim_regex = re.sub(r'<udim>', r'[0-9]{4}', src_pattern, flags=re.IGNORECASE)
        src_files = glob.glob(udim_regex)
        
        if not src_files:
            log_message(f"No UDIM files found for pattern: {udim_regex}", logging.WARNING)
            return []

        copied_paths = []
        base_src_path = os.path.dirname(src_pattern)
        base_dst_path = os.path.dirname(dst_pattern)

        for src in src_files:
            src = fix_path_separators(src)
            # 원본 경로의 기본 부분을 대상 경로의 기본 부분으로 교체
            dst = src.replace(base_src_path, base_dst_path)
            final_dst = create_group_folder(dst)
            # 복사할 폴더가 없으면 생성
            os.makedirs(os.path.dirname(final_dst), exist_ok=True)
            shutil.copy(src, final_dst)
            log_message(f"UDIM file copied to: {final_dst}")
            copied_paths.append(final_dst)
        return copied_paths
    except Exception as e:
        log_message(f"Failed to copy UDIM files: {str(e)}", logging.ERROR)
        cmds.warning(f"Failed to copy UDIM files: {str(e)}")
        return []

# 텍스처 경로 처리 및 복사를 담당하는 메인 핸들러 함수
def handle_texture_path(file_node, wrong_texture_path, scene_project_path, copy_files, yes_all_copy):
    """텍스처 경로를 수정하고, 필요 시 파일 복사를 수행합니다."""
    texture_filename = fix_path_separators(cmds.getAttr(file_node + ".fileTextureName"))
    modified_texture_filename = modify_texture_path(texture_filename, wrong_texture_path, scene_project_path)
    
    original_path_for_dialog = texture_filename
    new_path_for_dialog = modified_texture_filename

    # UV Tiling Mode (UDIM/Mari 등)가 설정되어 있는지 확인
    uv_tiling_mode = cmds.getAttr(file_node + ".uvTilingMode")
    is_udim = uv_tiling_mode != 0

    if is_udim:
        # 대화상자에 표시될 경로를 <UDIM> 태그로 교체하여 명확하게 보여줌
        original_path_for_dialog = re.sub(r'\d{4}', '<UDIM>', texture_filename, 1)
        new_path_for_dialog = re.sub(r'\d{4}', '<UDIM>', modified_texture_filename, 1)

    if copy_files:
        if not yes_all_copy:
            copy_msg = (f'UDIM 파일들을 복사하시겠습니까?\n' if is_udim else f'파일을 복사하시겠습니까?\n') + \
                       f'원본: {original_path_for_dialog}\n' + \
                       f'=>\n' + \
                       f'새 경로: {new_path_for_dialog}'
            
            confirm_copy = cmds.confirmDialog(
                title='파일 복사 확인', 
                message=copy_msg, 
                button=['Yes', 'Yes All', 'No', 'Cancel'], 
                defaultButton='Yes', 
                cancelButton='Cancel', 
                dismissString='No'
            )
            if confirm_copy == 'Yes All':
                yes_all_copy = True
            if confirm_copy == 'Cancel':
                log_message("Copy operation cancelled by user.")
                return texture_filename, modified_texture_filename, yes_all_copy # 복사 안해도 경로는 바꿀 수 있으므로 수정된 경로 반환
            if confirm_copy not in ['Yes', 'Yes All']:
                return texture_filename, modified_texture_filename, yes_all_copy
        
        # 실제 파일 복사 실행
        if is_udim:
            copied_paths = copy_udim_files(texture_filename, modified_texture_filename)
            if copied_paths:
                # setAttr을 위해 첫 번째 복사된 파일 경로를 사용
                modified_texture_filename = re.sub(r'\d{4}', '<UDIM>', copied_paths[0], 1)
        else:
            copied_path = copy_file(texture_filename, modified_texture_filename)
            if copied_path:
                modified_texture_filename = copied_path

    return texture_filename, modified_texture_filename, yes_all_copy

# 텍스처 경로를 실제로 교체하는 함수
def replace_texture_paths(wrong_texture_path, nodes, copy_files=False, individual_paths=False):
    """주어진 노드들의 텍스처 경로를 교체합니다."""
    def is_file_node(node_name):
        return cmds.nodeType(node_name) == "file"

    use_scene_path = cmds.checkBox('useScenePathCheckbox', query=True, value=True)
    if use_scene_path:
        scene_project_path = fix_path_separators(cmds.workspace(q=True, rd=True))
    else:
        scene_project_path = fix_path_separators(cmds.textField('customScenePathField', query=True, text=True))

    if not scene_project_path:
        cmds.warning("Scene project path is not set. Please set a project or provide a custom path.")
        return

    if not wrong_texture_path and not individual_paths:
        cmds.warning("Wrong texture path is not specified. Please enter a path or use the auto-detect options.")
        return
        
    wrong_texture_path = fix_path_separators(wrong_texture_path)

    yes_all_change = False
    yes_all_copy = False
    fileNodeList = [node for node in nodes if is_file_node(node)]

    for file_node in fileNodeList:
        current_wrong_path = wrong_texture_path
        if individual_paths:
            current_wrong_path = os.path.dirname(fix_path_separators(cmds.getAttr(file_node + ".fileTextureName"))) + "/"

        original_texture_filename, modified_texture_filename, yes_all_copy = handle_texture_path(file_node, current_wrong_path, scene_project_path, copy_files, yes_all_copy)
        
        # 경로가 실제로 변경되었는지 확인
        if original_texture_filename.lower() != modified_texture_filename.lower():
            if not yes_all_change:
                confirm = cmds.confirmDialog(
                    title='경로 변경 확인', 
                    message=f'경로를 변경하시겠습니까?\n원본: {original_texture_filename}\n=>\n새 경로: {modified_texture_filename}', 
                    button=['Yes', 'Yes All', 'No', 'Cancel'], 
                    defaultButton='Yes', 
                    cancelButton='Cancel', 
                    dismissString='No'
                )
                if confirm == 'Yes All':
                    yes_all_change = True
                if confirm == 'Cancel':
                    log_message("Operation cancelled by user.")
                    return
                if confirm not in ['Yes', 'Yes All']:
                    log_message(f"Skipping path change for node: {file_node}")
                    continue

            # 경로 변경 실행
            try:
                cmds.setAttr(file_node + ".fileTextureName", modified_texture_filename, type="string")
                log_message(f"Texture path changed for node: {file_node}")
            except Exception as e:
                log_message(f"Failed to set texture path for {file_node}: {str(e)}", logging.ERROR)
        else:
            log_message(f"Path for node {file_node} is already correct or no changes were made.")


# 리스트에서 선택된 노드들의 경로를 교체하는 함수
def replace_texture_paths_for_selected(wrong_texture_path, selected_nodes, copy_files):
    """UI 리스트에서 선택된 노드들에 대해 경로 교체를 실행합니다."""
    if not selected_nodes:
        cmds.warning("Please select at least one node from the list.")
        return
    
    individual_paths = cmds.checkBox('individualPathsCheckbox', query=True, value=True)
    replace_texture_paths(wrong_texture_path, selected_nodes, copy_files, individual_paths)

# UI 생성 함수
def create_ui():
    """스크립트의 메인 UI를 생성합니다."""
    if cmds.window("textureReplacerWindow", exists=True):
        cmds.deleteUI("textureReplacerWindow")

    window = cmds.window("textureReplacerWindow", title="Texture Path Replacer by CGUSLAB", widthHeight=(600, 750))
    # *** FIX: columnLayout에서 marginWidth, marginHeight 제거 ***
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    # --- 상단 버튼 및 경로 설정 ---
    cmds.button(label="Texture Path Replacer (도움말 열기)", command=open_github_link)
    cmds.separator(height=10, style='in')

    # *** FIX: frameLayout에 marginWidth, marginHeight 추가 ***
    cmds.frameLayout(label="1. 경로 설정 (Path Settings)", collapsable=False, borderVisible=True, marginWidth=5, marginHeight=5)
    # *** FIX: columnLayout에서 marginWidth, marginHeight 제거 ***
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.text(label="잘못된 텍스처 기본 경로 (Wrong Texture Base Path):")
    path_field = cmds.textField('pathField', placeholderText="예: D:/Assets/Textures")
    
    cmds.button('autoDetectButton', label='리스트에서 선택한 노드로 경로 자동 감지', command=lambda *args: get_auto_wrong_texture_path(
        cmds.textScrollList('fileNodesList', query=True, selectItem=True)[0] if cmds.textScrollList('fileNodesList', query=True, selectItem=True) else None
    ))
    
    cmds.checkBox('individualPathsCheckbox', label='각 노드별로 경로 자동 감지 (권장)', value=True,
                  annotation="이 옵션을 선택하면 위의 '잘못된 경로' 입력은 무시되고, 각 파일 노드의 현재 경로를 기반으로 개별적으로 경로를 수정합니다.")

    cmds.separator(height=10, style='in')
    
    cmds.checkBox('useScenePathCheckbox', label='현재 씬의 프로젝트 경로 사용', value=True,
                  annotation="체크 해제 시 아래의 커스텀 경로를 사용합니다.")
    cmds.text(label="또는 커스텀 프로젝트 경로 입력:")
    custom_scene_path_field = cmds.textField('customScenePathField', placeholderText="예: C:/Users/user/Documents/maya/projects/myProject")
    
    cmds.setParent('..') # columnLayout
    cmds.setParent('..') # frameLayout
    
    # --- 노드 검색 및 리스트 ---
    # *** FIX: frameLayout에 marginWidth, marginHeight 추가 ***
    cmds.frameLayout(label="2. 파일 노드 검색 (Search File Nodes)", collapsable=False, borderVisible=True, marginWidth=5, marginHeight=5)
    # *** FIX: columnLayout에서 marginWidth, marginHeight 제거 ***
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.checkBox('includeProjectFilesCheckbox', label='프로젝트 내 파일 노드 포함', value=False,
                  annotation="체크 시, 경로가 올바른 파일 노드도 리스트에 포함하여 검색합니다.")

    cmds.button(
        label="파일 노드 검색", 
        command=populate_file_nodes_list,
        backgroundColor=(0.35, 0.5, 0.65),
        height=30
    )

    cmds.textScrollList('fileNodesList', numberOfRows=10, allowMultiSelection=True)
    
    cmds.setParent('..') # columnLayout
    cmds.setParent('..') # frameLayout

    # --- 실행 버튼 ---
    # *** FIX: frameLayout에 marginWidth, marginHeight 추가 ***
    cmds.frameLayout(label="3. 경로 변경 실행 (Execute)", collapsable=False, borderVisible=True, marginWidth=5, marginHeight=5)
    # *** FIX: columnLayout에서 marginWidth, marginHeight 제거 ***
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.checkBox('copyFilesCheckbox', label='새 경로로 파일 복사 및 하위폴더 생성', value=True,
                  annotation="경로를 변경하면서 실제 텍스처 파일을 새 위치로 복사합니다. 파일 이름의 '_' 앞부분을 기준으로 하위 폴더도 생성합니다.")

    cmds.button(label="리스트의 모든 노드 경로 변경", command=lambda *args: replace_texture_paths(
        cmds.textField(path_field, query=True, text=True), 
        cmds.textScrollList('fileNodesList', query=True, allItems=True) or [],
        cmds.checkBox('copyFilesCheckbox', query=True, value=True),
        cmds.checkBox('individualPathsCheckbox', query=True, value=True)
    ), backgroundColor=(0.8, 0.4, 0.4), height=30)
    
    cmds.button(label="리스트에서 선택한 노드 경로 변경", command=lambda *args: replace_texture_paths_for_selected(
        cmds.textField(path_field, query=True, text=True), 
        cmds.textScrollList('fileNodesList', query=True, selectItem=True),
        cmds.checkBox('copyFilesCheckbox', query=True, value=True)
    ), backgroundColor=(0.4, 0.6, 0.4), height=30)

    cmds.button(label="Maya에서 직접 선택한 노드 경로 변경", command=lambda *args: replace_texture_paths(
        cmds.textField(path_field, query=True, text=True),
        cmds.ls(selection=True),
        cmds.checkBox('copyFilesCheckbox', query=True, value=True),
        cmds.checkBox('individualPathsCheckbox', query=True, value=True)
    ))

    cmds.setParent('..') # columnLayout
    cmds.setParent('..') # frameLayout

    # --- 로그 창 ---
    # *** FIX: frameLayout에 marginWidth, marginHeight 추가 ***
    cmds.frameLayout(label="로그 (Log)", collapsable=True, collapse=False, borderVisible=True, marginWidth=5, marginHeight=5)
    cmds.scrollField('logScrollField', editable=False, wordWrap=True, height=200)
    cmds.setParent('..') # frameLayout

    cmds.showWindow(window)

# 스크립트 실행 시 UI 생성
if __name__ == "__main__":
    create_ui()

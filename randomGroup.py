import maya.cmds as cmds
import random

def group_selected_object(num_groups):
    # 선택된 오브젝트들을 가져오기
    selected_objects = cmds.ls(selection = True)

    # 선택된 오브젝트가 없으면 에러
    if not selected_objects:
        cmds.error("선택된 오브젝트가 없습니다.")
        return

    # 오브젝트 수가 그룹 수보다 적으면 에러
    if len(selected_objects) < num_groups:
        cmds.error("선택된 오브젝트 수가 그룹 수보다 적습니다.")
        return

    # 오브젝트를 랜덤하게 섞기
    random.shuffle(selected_objects)

    # 각 그룹의 크기를 결정하기
    group_sizes = [len(selected_objects) // num_groups] * num_groups
    for i in range(len(selected_objects) % num_groups):
        group_sizes[i] += 1

    print(f"Group Sizes : {group_sizes}")
    print(f"Selected Objects List : {selected_objects}")

    # 그룹 나누기
    start_index = 0
    for i in range(num_groups):
        group = selected_objects[start_index:start_index + group_sizes[i]]
        group_name = "Group_" + str(i + 1)
        print(f"Group {i + 1} : {group}")
        cmds.group(group, name=group_name)
        print(f"Index : {start_index} ~ {start_index + group_sizes[i]}")
        start_index = start_index + group_sizes[i]
                
group_selected_object(3)

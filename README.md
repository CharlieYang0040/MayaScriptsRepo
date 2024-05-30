# Texture Path Replacer

`Texture Path Replacer`는 Autodesk Maya에서 파일 텍스처 경로를 관리하고 수정하기 위한 도구입니다. 
이 스크립트는 잘못된 텍스처 경로를 자동으로 감지하고, 경로를 수정하며, 필요한 경우 파일을 새로운 경로로 복사할 수 있습니다.

## 기능

- 잘못된 텍스처 경로 자동 감지
- 텍스처 경로 수정
- UDIM 방식 파일 복사 지원
- 각 파일 노드마다 개별 경로 설정 지원
- GitHub 링크를 통해 도움말 및 스크립트 업데이트 확인

## 설치 방법

1. `texturePathReplacer.py` 파일을 다운로드합니다.
2. 파일을 Maya 스크립트 폴더에 저장합니다 (예: `Documents/maya/scripts`).
3. Maya를 열고 Script Editor에서 다음 명령을 실행합니다:

    ```python
    import texturePathReplacer
    texturePathReplacer.create_ui()
    ```

4. 또는 위 명령어를 shelf에 등록하여 편하게 열 수 있습니다.

## 사용 방법

### 1. UI 열기

- 위 명령어를 실행하면 `Texture Path Replacer` UI가 열립니다.
  
![image](https://github.com/CharlieYang0040/MayaScriptsRepo/assets/129147417/9503e14a-23e9-4fdb-8115-a5af0ce53fee)



### 2. 기본 사용법

- **Help 버튼**: `Texture Path Replacer (open help)` 버튼을 클릭하면 GitHub 리포지토리의 도움말 페이지가 열립니다.
- 먼저 `Search File Nodes` 버튼을 클릭하여 잘못된 텍스처 경로를 가진 파일 노드를 검색합니다.

### 3. 프로젝트 경로 수정

- **Scene Project Path 사용**: `Use Scene Project Path` 체크박스를 선택하여 현재 장면의 프로젝트 경로를 사용합니다.
- **사용자 지정 경로 입력**: `Or enter a custom scene project path` 필드에 사용자 지정 프로젝트 경로를 입력합니다.

### 4. 옵션 설정

- **잘못된 텍스처 경로 입력**: `Enter the wrong texture path` 필드에 잘못된 텍스처 경로를 입력합니다.
- **경로 자동 감지**: `Detect wrong texture path` 버튼을 클릭하여 선택된 파일 노드의 경로를 자동으로 감지합니다.
- **개별 경로 감지**: `Auto detect wrong texture paths` 체크박스를 선택하면 각 파일 노드마다 개별적으로 잘못된 경로를 감지합니다.

### 5. 텍스처 경로 수정

- **모든 노드 수정**: `Replace Texture Paths for All Nodes` 버튼을 클릭하여 검색된 모든 파일 노드의 텍스처 경로를 수정합니다.
- **선택된 노드 수정**: `Replace Texture Paths for Selected Nodes` 버튼을 클릭하여 선택된 파일 노드의 텍스처 경로를 수정합니다.
- **선택된 Maya 노드 수정**: `Replace Texture Paths for Selected Nodes in Maya` 버튼을 클릭하여 Maya에서 선택된 파일 노드의 텍스처 경로를 수정합니다.
- **파일 복사**: `Copy files to new path` 체크박스를 선택하면 텍스처 파일을 새로운 경로로 복사합니다.

### 6. 로그 확인

- UI 하단의 `Log` 창에서 모든 작업 로그를 확인할 수 있습니다.

## 주의 사항

- UDIM 파일 복사 시 모든 관련 파일을 올바르게 복사할 수 있도록 설정을 확인하십시오.
- 스크립트를 실행하기 전에 모든 작업을 저장하십시오.

## 문의 및 버그 신고

버그 신고 및 기능 요청은 [GitHub 리포지토리](https://github.com/CharlieYang0040/MayaScriptsRepo)에서 가능합니다.

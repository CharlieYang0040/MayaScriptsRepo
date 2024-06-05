# V-Ray Batch Script Generator for Maya

Autodesk Maya를 위한 V-Ray 배치 스크립트 생성기입니다. 이 도구는 Python과 PySide2를 사용하여 개발되었으며, 
배치 렌더링 스크립트를 쉽게 생성할 수 있는 그래픽 사용자 인터페이스(GUI)를 제공합니다. 
이 도구를 사용하면 V-Ray를 사용하여 여러 Maya 씬의 렌더링 프로세스를 자동화하고 관리할 수 있습니다.

(현재는 Maya의 경로를 Maya2023버전으로 생성합니다.)

![image](https://github.com/CharlieYang0040/MayaScriptsRepo/assets/129147417/9ffa9c97-d2bb-4486-b25e-37ecd8fba728)


## 주요 기능

- Maya 씬 파일 선택 및 설정
- 프로젝트 경로 및 출력 디렉토리 자동 설정
- 이미지 포맷, 해상도 및 애니메이션 프레임 설정
- 렌더 레이어 설정
- 배치 렌더 스크립트 생성 및 실행
- 씬 파일 열기 진행 상황 및 로깅 표시

## 실행법

- [Releases](https://github.com/CharlieYang0040/MayaScriptsRepo/releases)([바로받기](https://github.com/CharlieYang0040/MayaScriptsRepo/releases/download/v0.1.0/vrayBatchScriptGenUI.exe))에서 `vrayBatchScriptGenUI.exe` 실행파일을 다운로드 받습니다.
- 다운로드 받은 `vrayBatchScriptGenUI.exe`를 더블 클릭하여 실행합니다.

## 위젯 및 버튼 설명

### Read me
- **Read me**: 이 버튼을 클릭하면 [GitHub 리포지토리](https://github.com/CharlieYang0040/MayaScriptsRepo/tree/main/vrayBatchScriptGenUI)로 연결됩니다.

### Scene File
- **Scene File**: 렌더링할 Maya 씬 파일을 선택할 수 있습니다.
- **Browse...**: 파일 탐색기를 열어 Maya 씬 파일을 선택할 수 있습니다.

### Project Path
- **Project Path**: 선택한 씬 파일의 프로젝트 경로를 자동으로 설정합니다.

### Output Directory
- **Output Directory**: 출력 이미지가 저장될 디렉토리를 자동으로 설정합니다.

### Open Scene File
- **Open Scene File**: 선택한 씬 파일을 열고, 이미지 포맷, 해상도, 애니메이션 프레임 및 렌더 레이어 정보를 가져옵니다.
- **Progress Bar**: 씬 파일을 여는 동안 진행 상황을 퍼센트로 표시합니다.

### Image Format
- **Image Format**: 렌더링 이미지의 포맷을 선택할 수 있습니다. (예: exr, png, jpg, tif 등)

### Resolution
- **Resolution**: 렌더링 이미지의 해상도를 선택할 수 있습니다. (예: HD 1080, HD 720, 4K 등)
- **X**: 커스텀 해상도의 가로 값을 설정할 수 있습니다.
- **Y**: 커스텀 해상도의 세로 값을 설정할 수 있습니다.

### Animation Frames
- **Start Frame**: 애니메이션 렌더링의 시작 프레임을 설정할 수 있습니다.
- **End Frame**: 애니메이션 렌더링의 종료 프레임을 설정할 수 있습니다.

### Render Layers
- **Render Layers**: 씬 파일에서 렌더링 가능한 레이어를 선택할 수 있습니다. 여러 개의 레이어를 선택할 수 있습니다.

### Generate Batch Script
- **Generate Batch Script**: 설정된 옵션에 따라 배치 렌더링 스크립트를 생성합니다.

### Execute Batch Script
- **Execute Batch Script**: 생성된 배치 스크립트를 새 명령 프롬프트 창에서 실행합니다.

### Log
- **Log**: 프로그램의 진행 상황 및 디버그 정보를 표시합니다.

이 도구는 V-Ray를 사용한 Maya의 배치 렌더링 작업을 효율적으로 관리할 수 있도록 도와줍니다. 각 위젯과 버튼은 사용자에게 직관적이고 쉽게 사용할 수 있는 환경을 제공합니다.

# Renamer for Maya

`Renamer`는 Autodesk Maya 사용자를 위해 개발된 강력한 이름 변경 도구입니다. 이 플러그인은 복잡한 계층구조에서 노드의 이름을 쉽고 빠르게 일괄 변경할 수 있도록 도와줍니다.

![image](https://github.com/CharlieYang0040/MayaScriptsRepo/assets/129147417/eb64be65-8992-4a45-9693-04350b97d85b)

## 특징

- **노드 선택 변경**: 선택된 노드, 모든 노드, 또는 계층 구조 내의 노드들을 대상으로 이름 변경을 실행할 수 있습니다.
- **계층적 변경**: Maya의 계층 구조를 따라 하위에서 상위 노드로 순차적으로 이름을 변경합니다. 이를 통해 종속적 노드 구조를 유지하면서 변경할 수 있습니다.
- **사용자 정의 가능성**: 사용자가 지정한 텍스트를 찾아 다른 텍스트로 대체할 수 있습니다. 이는 특히 프로젝트의 표준을 유지하거나 일괄적으로 업데이트할 필요가 있을 때 유용합니다.

## 설치 방법

### 자동 설치

1. `renamer_Install.exe` 파일을 [다운로드](https://raw.githubusercontent.com/CharlieYang0040/MayaScriptsRepo/main/renamer/pyinstaller/dist/renamer_Install.exe)하세요.
2. 다운로드한 실행 파일을 실행하여 설치를 완료합니다.

### 수동 설치

1. `Renamer.py` 파일을 [다운로드](https://raw.githubusercontent.com/CharlieYang0040/MayaScriptsRepo/main/renamer/renamer.py)합니다.
2. 다운로드한 `.py` 파일을 Maya의 스크립트 폴더에 복사합니다.
3. Maya를 열고 Script Editor에서 다음 명령을 실행합니다:

    ```python
    import renamer
    renamer.show_ui()
    ```

4. 또는 위 명령어를 shelf에 등록하여 편하게 열 수 있습니다.

## Usage

설치 후에 Maya를 재시작 해야 합니다.

1. **모드 선택**: `All Nodes`, `Selected Nodes`, `Hierarchy` 중 하나를 선택하여 작업 범위를 정합니다.
2. **찾기 및 바꾸기**: 변경하고 싶은 텍스트를 `Find` 필드에 입력하고, 새로운 텍스트를 `Replace` 필드에 입력합니다.
3. **Rename 버튼 클릭**: 설정한 옵션에 따라 이름 변경 작업을 수행합니다.

## Note

- 사용 중에 데이터를 손실하지 않도록 사전에 작업 파일을 백업하는 것이 좋습니다.
- 자동 설치 후에는 Maya를 재시작하여 플러그인이 정상적으로 로드되었는지 확인하세요.

## More Information

자세한 정보는 [GitHub Repository](https://github.com/CharlieYang0040/MayaScriptsRepo/tree/main/renamer)를 참조하세요.

# mtlMaker

`mtlMaker`는 Autodesk Maya용 플러그인으로, 프로젝트 폴더의 텍스쳐를 자동으로 찾아 VRayMtl 노드에 연결해주는 도구입니다. 이 플러그인을 사용하면 텍스쳐를 자동으로 로드하고, 올바른 속성에 연결하여 머티리얼을 손쉽게 구성할 수 있습니다.

![test_video](https://github.com/CharlieYang0040/MayaScriptsRepo/assets/129147417/63d2aa28-6c1e-4060-b8fb-96bd844e1523)

## 기능

- 프로젝트 폴더에서 텍스쳐 자동 검색
- 텍스쳐를 VRayMtl 노드에 자동 연결
- 다양한 텍스쳐 이름 인식 (예: BaseColor, Diffuse, Roughness, Glossiness, Metallic, Specular, Normal)
- UDIM 텍스쳐 지원
- 진행 상황 로그 출력
- 여러 폴더를 동시에 선택하여 처리
- 사용자 친화적인 GUI 제공

## 설치 방법

- mtlMaker_Install.exe 를 [다운로드](https://github.com/CharlieYang0040/MayaScriptsRepo/blob/main/mtlMaker/pyinstaller/dist/mtlMaker_Install.exe) 후 실행합니다.
- Maya를 재시작합니다.

## 사용 방법

1. Maya의 `Custom` 셸프에서 `mtlMaker` 버튼을 클릭합니다.
2. `Search` 버튼을 클릭하여 프로젝트 폴더의 텍스쳐를 검색합니다.
3. 목록에서 하나 이상의 폴더를 선택합니다.
4. `Make` 버튼을 클릭하여 선택된 폴더의 텍스쳐를 VRayMtl 노드에 연결합니다.
5. 진행 상황은 로그 창에서 확인할 수 있습니다.
6. `Help` 버튼을 클릭하여 GitHub Readme 페이지를 참조할 수 있습니다.

## 주의 사항

- 프로젝트 폴더의 sourceimages 안에서 찾습니다.
- 폴더 이름을 머티리얼 이름으로 인식하여 사용합니다.
- 따라서 텍스쳐 파일들을 폴더에 넣어 정리가 되어 있어야 합니다.

## 도움말

더 많은 정보나 문제가 있을 경우,

 GitHub 페이지의 [도움말 섹션](https://github.com/CharlieYang0040/MayaScriptsRepo/tree/main/mtlMaker)을 참조하세요.

## 기여

기여를 원하신다면, 이 리포지토리를 포크하고 풀 리퀘스트를 보내주세요. 문제가 발생하면 이슈 트래커에 보고해 주세요.

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

import os
import pprint

def print_environment_variables():
    # 환경 변수를 딕셔너리 형태로 가져옴
    env_vars = os.environ
    
    # 보기 좋게 출력
    pprint.pprint(dict(env_vars))

# Maya의 스크립트 에디터에서 실행
print_environment_variables()

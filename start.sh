#!/bin/bash

# 에러 발생 시 스크립트 중단
set -e

echo "==================================================="
echo " 🎵 음악 파일 자동 변환 프로세스를 시작합니다. (Linux)"
echo "==================================================="

# 1. 가상환경(venv)이 없으면 새로 생성
if [ ! -d "venv" ]; then
    echo "📦 가상환경(venv)을 생성하는 중입니다..."
    # 일부 리눅스 배포판에서는 python3-venv 패키지가 필요할 수 있습니다.
    python3 -m venv venv
fi

# 2. 가상환경 진입 및 패키지 설치
echo "🔌 가상환경을 활성화하고 필요한 패키지를 확인합니다..."
source ./venv/bin/activate

echo "📥 mutagen 패키지 설치 및 업데이트 중..."
pip install --upgrade pip > /dev/null
pip install mutagen

# 3. 파이썬 스크립트 실행
echo "🚀 파이썬 코드를 실행합니다..."
python3 auto_rename.py

# 4. 가상환경 종료
echo "🔌 가상환경을 비활성화합니다..."
deactivate

echo "==================================================="
echo " 🎉 모든 작업이 끝났습니다!"
echo "==================================================="
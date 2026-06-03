@echo off
chcp 65001 > nul
title 음악 파일 이름 변경 자동화 스트립트

echo ===================================================
echo  🎵 음악 파일 자동 변환 프로세스를 시작합니다.
echo ===================================================

:: 1. 가상환경(venv)이 없으면 새로 생성
if not exist venv (
    echo 📦 가상환경(venv)을 생성하는 중입니다...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 파이썬이 설치되어 있지 않거나 경로 설정에 문제가 있습니다.
        pause
        exit /b
    )
)

:: 2. 가상환경 진입 및 패키지 설치
echo 🔌 가상환경을 활성화하고 필요한 패키지를 확인합니다...
call .\venv\Scripts\activate

echo 📥 mutagen 패키지 설치 및 업데이트 중...
pip install --upgrade pip > nul
pip install mutagen

:: 3. 파이썬 스크립트 실행
echo 🚀 파이썬 코드를 실행합니다...
python auto_rename.py

:: 4. 가상환경 종료 및 마무리
echo 🔌 가상환경을 비활성화합니다...
call deactivate

echo ===================================================
echo  🎉 모든 작업이 끝났습니다!
echo ===================================================
pause
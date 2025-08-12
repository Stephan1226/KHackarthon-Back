#!/usr/bin/env python3
"""
API 테스트 스크립트
사용법: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """헬스 체크 테스트"""
    print("🔍 헬스 체크 테스트...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"상태 코드: {response.status_code}")
        print(f"응답: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_register():
    """회원가입 테스트"""
    print("\n📝 회원가입 테스트...")
    try:
        user_data = {
            "id": "testuser",
            "password": "testpass123"
        }
        response = requests.post(
            f"{BASE_URL}/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"상태 코드: {response.status_code}")
        print(f"응답: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_login():
    """로그인 테스트"""
    print("\n🔑 로그인 테스트...")
    try:
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = requests.post(
            f"{BASE_URL}/token",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"상태 코드: {response.status_code}")
        print(f"응답: {response.json()}")
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            return token
        return None
    except Exception as e:
        print(f"❌ 오류: {e}")
        return None

def test_protected_route(token):
    """보호된 라우트 테스트"""
    if not token:
        print("\n❌ 토큰이 없어 보호된 라우트 테스트를 건너뜁니다.")
        return False
    
    print("\n🛡️ 보호된 라우트 테스트...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/protected", headers=headers)
        print(f"상태 코드: {response.status_code}")
        print(f"응답: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_user_info(token):
    """사용자 정보 조회 테스트"""
    if not token:
        print("\n❌ 토큰이 없어 사용자 정보 조회 테스트를 건너뜁니다.")
        return False
    
    print("\n👤 사용자 정보 조회 테스트...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"상태 코드: {response.status_code}")
        print(f"응답: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🚀 KHackarthon Backend API 테스트 시작\n")
    
    # 서버가 실행 중인지 확인
    if not test_health():
        print("❌ 서버가 실행되지 않았습니다. 먼저 서버를 시작하세요.")
        return
    
    # 회원가입 테스트
    if not test_register():
        print("❌ 회원가입 테스트 실패")
        return
    
    # 로그인 테스트
    token = test_login()
    if not token:
        print("❌ 로그인 테스트 실패")
        return
    
    # 보호된 라우트 테스트
    test_protected_route(token)
    
    # 사용자 정보 조회 테스트
    test_user_info(token)
    
    print("\n✅ 모든 테스트가 완료되었습니다!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
사용자 지갑 API 통합 테스트 스크립트
사용법: python test_wallet_api.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

class WalletAPITester:
    def __init__(self):
        self.access_token = None
        self.user_id = None
        
    def test_health(self):
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
    
    def test_register(self):
        """회원가입 테스트"""
        print("\n📝 회원가입 테스트...")
        try:
            import time
            timestamp = int(time.time())
            user_data = {
                "id": f"walletuser{timestamp}",
                "password": "walletpass123"
            }
            response = requests.post(
                f"{BASE_URL}/register",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"상태 코드: {response.status_code}")
            print(f"응답: {response.json()}")
            
            if response.status_code == 201:
                self.user_id = response.json().get("user_id")
                return True
            return False
        except Exception as e:
            print(f"❌ 오류: {e}")
            return False
    
    def test_login(self):
        """로그인 테스트"""
        print("\n🔑 로그인 테스트...")
        try:
            import time
            timestamp = int(time.time())
            login_data = {
                "username": f"walletuser{timestamp}",
                "password": "walletpass123"
            }
            response = requests.post(
                f"{BASE_URL}/token",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            print(f"상태 코드: {response.status_code}")
            print(f"응답: {response.json()}")
            
            if response.status_code == 200:
                self.access_token = response.json().get("access_token")
                return True
            return False
        except Exception as e:
            print(f"❌ 오류: {e}")
            return False
    
    def test_create_wallet(self):
        """지갑 생성 테스트"""
        if not self.access_token:
            print("\n❌ 토큰이 없어 지갑 생성 테스트를 건너뜁니다.")
            return False
        
        print("\n💰 지갑 생성 테스트...")
        try:
            wallet_data = {
                "money": 1000.00
            }
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(
                f"{BASE_URL}/users/me/wallet",
                json=wallet_data,
                headers=headers
            )
            print(f"상태 코드: {response.status_code}")
            print(f"응답: {response.json()}")
            return response.status_code == 201
        except Exception as e:
            print(f"❌ 오류: {e}")
            return False
    
    def test_get_wallet(self):
        """지갑 조회 테스트"""
        if not self.access_token:
            print("\n❌ 토큰이 없어 지갑 조회 테스트를 건너뜁니다.")
            return False
        
        print("\n👛 지갑 조회 테스트...")
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(
                f"{BASE_URL}/users/me/wallet",
                headers=headers
            )
            print(f"상태 코드: {response.status_code}")
            print(f"응답: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 오류: {e}")
            return False
    
    def test_add_money(self):
        """돈 추가 테스트"""
        if not self.access_token:
            print("\n❌ 토큰이 없어 돈 추가 테스트를 건너뜁니다.")
            return False
        
        print("\n💵 돈 추가 테스트...")
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.put(
                f"{BASE_URL}/users/me/wallet/add?amount=500.00",
                headers=headers
            )
            print(f"상태 코드: {response.status_code}")
            print(f"응답: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 오류: {e}")
            return False
    
    def test_wallet_after_add(self):
        """돈 추가 후 지갑 조회 테스트"""
        if not self.access_token:
            print("\n❌ 토큰이 없어 지갑 조회 테스트를 건너뜁니다.")
            return False
        
        print("\n👛 돈 추가 후 지갑 조회 테스트...")
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(
                f"{BASE_URL}/users/me/wallet",
                headers=headers
            )
            print(f"상태 코드: {response.status_code}")
            print(f"응답: {response.json()}")
            
            if response.status_code == 200:
                wallet_data = response.json()
                current_money = wallet_data.get("money", 0)
                print(f"💰 현재 지갑 잔액: {current_money}")
                return True
            return False
        except Exception as e:
            print(f"❌ 오류: {e}")
            return False
    
    def test_user_info(self):
        """사용자 정보 조회 테스트"""
        if not self.access_token:
            print("\n❌ 토큰이 없어 사용자 정보 조회 테스트를 건너뜁니다.")
            return False
        
        print("\n👤 사용자 정보 조회 테스트...")
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(
                f"{BASE_URL}/users/me",
                headers=headers
            )
            print(f"상태 코드: {response.status_code}")
            print(f"응답: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 오류: {e}")
            return False
    
    def run_all_tests(self):
        """모든 테스트 실행"""
        print("🚀 사용자 지갑 API 통합 테스트 시작\n")
        
        # 1. 서버 상태 확인
        if not self.test_health():
            print("❌ 서버가 실행되지 않았습니다. 먼저 서버를 시작하세요.")
            return
        
        # 2. 회원가입
        if not self.test_register():
            print("❌ 회원가입 테스트 실패")
            return
        
        # 3. 로그인
        if not self.test_login():
            print("❌ 로그인 테스트 실패")
            return
        
        # 4. 지갑 생성
        if not self.test_create_wallet():
            print("❌ 지갑 생성 테스트 실패")
            return
        
        # 5. 지갑 조회
        if not self.test_get_wallet():
            print("❌ 지갑 조회 테스트 실패")
            return
        
        # 6. 돈 추가
        if not self.test_add_money():
            print("❌ 돈 추가 테스트 실패")
            return
        
        # 7. 돈 추가 후 지갑 조회
        if not self.test_wallet_after_add():
            print("❌ 돈 추가 후 지갑 조회 테스트 실패")
            return
        
        # 8. 사용자 정보 조회
        self.test_user_info()
        
        print("\n✅ 모든 테스트가 완료되었습니다!")
        print(f"🎯 테스트된 사용자 ID: {self.user_id}")
        print(f"🔑 사용된 토큰: {self.access_token[:20]}...")

def main():
    tester = WalletAPITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()

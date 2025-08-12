#!/bin/bash

# 사용자 지갑 API curl 테스트 스크립트
BASE_URL="http://localhost:8000"

echo "🚀 사용자 지갑 API curl 테스트 시작"
echo "=================================="

# 1. 헬스 체크
echo -e "\n🔍 1. 헬스 체크"
curl -s -X GET "${BASE_URL}/health" | jq '.'

# 2. 회원가입
echo -e "\n📝 2. 회원가입"
REGISTER_RESPONSE=$(curl -s -X POST "${BASE_URL}/register" \
  -H "Content-Type: application/json" \
  -d '{"id": "curluser", "password": "curlpass123"}')

echo "$REGISTER_RESPONSE" | jq '.'

# 3. 로그인
echo -e "\n🔑 3. 로그인"
LOGIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=curluser&password=curlpass123")

echo "$LOGIN_RESPONSE" | jq '.'

# JWT 토큰 추출
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    echo "❌ 로그인 실패 - 토큰을 가져올 수 없습니다."
    exit 1
fi

echo "✅ JWT 토큰 획득: ${TOKEN:0:20}..."

# 4. 지갑 생성
echo -e "\n💰 4. 지갑 생성 (1000원)"
WALLET_CREATE_RESPONSE=$(curl -s -X POST "${BASE_URL}/users/me/wallet" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"money": 1000.00}')

echo "$WALLET_CREATE_RESPONSE" | jq '.'

# 5. 지갑 조회
echo -e "\n👛 5. 지갑 조회"
WALLET_GET_RESPONSE=$(curl -s -X GET "${BASE_URL}/users/me/wallet" \
  -H "Authorization: Bearer $TOKEN")

echo "$WALLET_GET_RESPONSE" | jq '.'

# 6. 돈 추가 (500원)
echo -e "\n💵 6. 돈 추가 (500원)"
ADD_MONEY_RESPONSE=$(curl -s -X PUT "${BASE_URL}/users/me/wallet/add?amount=500.00" \
  -H "Authorization: Bearer $TOKEN")

echo "$ADD_MONEY_RESPONSE" | jq '.'

# 7. 돈 추가 후 지갑 조회
echo -e "\n👛 7. 돈 추가 후 지갑 조회"
FINAL_WALLET_RESPONSE=$(curl -s -X GET "${BASE_URL}/users/me/wallet" \
  -H "Authorization: Bearer $TOKEN")

echo "$FINAL_WALLET_RESPONSE" | jq '.'

# 8. 사용자 정보 조회
echo -e "\n👤 8. 사용자 정보 조회"
USER_INFO_RESPONSE=$(curl -s -X GET "${BASE_URL}/users/me" \
  -H "Authorization: Bearer $TOKEN")

echo "$USER_INFO_RESPONSE" | jq '.'

echo -e "\n✅ 모든 테스트가 완료되었습니다!"
echo "=================================="

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy import text
from database import engineconn
from models import UserCreate, UserResponse, Token
from auth import get_db, create_user, authenticate_user, get_current_active_user
from security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
import json

app = FastAPI(
    title="KHackarthon Backend API (Debug Version)",
    description="JWT 인증이 포함된 백엔드 API - 디버그 모드",
    version="1.0.0"
)

# 데이터베이스 엔진 설정
engine = engineconn()

@app.get("/")
async def root():
    return {"message": "KHackarthon Backend API (Debug Version)"}

@app.get("/health")
async def health_check():
    """헬스 체크 API - 데이터베이스 연결 상태 확인"""
    try:
        # 데이터베이스 연결 테스트 - SQLAlchemy 2.0 호환
        with engine.engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        return {"status": "healthy", "message": "데이터베이스 연결 정상"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"데이터베이스 연결 실패: {str(e)}"}

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: Request):
    """회원가입 API - 디버그 버전"""
    try:
        print("=== 회원가입 API 호출됨 ===")
        
        # 요청 본문 읽기
        body = await request.body()
        print(f"요청 본문 (raw): {body}")
        
        # JSON 파싱
        try:
            body_json = await request.json()
            print(f"요청 본문 (JSON): {body_json}")
        except Exception as json_error:
            print(f"JSON 파싱 오류: {json_error}")
            return JSONResponse(
                content={"error": "잘못된 JSON 형식"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # 유효성 검사
        if not body_json.get("id") or not body_json.get("password"):
            return JSONResponse(
                content={"error": "사용자 ID와 패스워드는 필수입니다."},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # 간단한 응답 (데이터베이스 연결 없이)
        response_data = {
            "user_id": 1,
            "id": body_json["id"],
            "message": "회원가입 성공 (디버그 모드)"
        }
        
        print(f"응답 데이터: {response_data}")
        return JSONResponse(
            content=response_data,
            status_code=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        print(f"회원가입 API 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={"error": f"서버 오류: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """로그인 API - 디버그 버전"""
    print(f"로그인 시도: {form_data.username}")
    
    # 간단한 응답 (인증 없이)
    return {
        "access_token": "debug_token_123",
        "token_type": "bearer"
    }

@app.get("/users/me")
async def read_users_me():
    """현재 사용자 정보 조회 - 디버그 버전"""
    return {
        "user_id": 1,
        "id": "debug_user"
    }

@app.get("/protected")
async def protected_route():
    """보호된 라우트 예시 - 디버그 버전"""
    return {
        "message": "인증이 성공했습니다! (디버그 모드)",
        "user_id": "debug_user"
    }

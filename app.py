from fastapi import FastAPI
from sqlalchemy import text
from database import engineconn

app = FastAPI()

# 데이터베이스 엔진 설정
engine = engineconn()

@app.get("/")
async def root():
    return {"message": "KHackarthon Backend API"}

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
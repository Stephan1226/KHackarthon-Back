from database import engineconn
from models import Base

def create_tables():
    """데이터베이스 테이블 생성"""
    try:
        engine = engineconn()
        Base.metadata.create_all(bind=engine.engine)
        print("✅ 데이터베이스 테이블이 성공적으로 생성되었습니다.")
    except Exception as e:
        print(f"❌ 테이블 생성 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    create_tables()

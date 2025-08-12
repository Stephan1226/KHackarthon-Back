from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

# Docker MySQL 연결을 위한 새로운 포트 사용
DB_URL = 'mysql://root:1234@127.0.0.1:3307/k_hackarthon'

class engineconn:

    def __init__(self):
        # MySQL 연결을 위한 기본 옵션들
        self.engine = create_engine(
            DB_URL, 
            pool_recycle=500,
            pool_pre_ping=True,  # 연결 상태 확인
            echo=False,  # SQL 쿼리 로깅 (필요시 True로 변경)
            # MySQL 연결을 위한 필수 옵션들
            connect_args={
                "charset": "utf8mb4",
                "autocommit": True
            }
        )
        # Session 클래스 생성
        self.Session = sessionmaker(bind=self.engine)

    def sessionmaker(self):
        # Session 클래스 자체를 반환
        return self.Session

    def connection(self):
        conn = self.engine.connect()
        return conn
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import engineconn
from models import User, UserCreate, UserResponse
from security import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

# OAuth2 스키마
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    """데이터베이스 세션 생성"""
    engine = engineconn()
    SessionLocal = engine.sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_id(db: Session, user_id: str):
    """사용자 ID로 사용자 조회"""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    """새 사용자 생성 (회원가입)"""
    # 이미 존재하는 사용자인지 확인
    db_user = get_user_by_id(db, user.id)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 사용자 ID입니다."
        )
    
    # 패스워드 해싱
    hashed_password = get_password_hash(user.password)
    
    # 새 사용자 생성
    db_user = User(
        id=user.id,
        password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, user_id: str, password: str):
    """사용자 인증"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """현재 인증된 사용자 조회"""
    from security import verify_token
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보를 확인할 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_id = verify_token(token)
    if user_id is None:
        raise credentials_exception
    
    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    """현재 활성 사용자 조회"""
    return current_user

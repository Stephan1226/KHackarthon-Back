from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from database import engineconn
from models import UserCreate, UserResponse, Token, UserWalletCreate, UserWalletResponse
from auth import get_db, create_user, authenticate_user, get_current_active_user, get_user_by_id
from security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

app = FastAPI(
    title="KHackarthon Backend API",
    description="JWT 인증이 포함된 백엔드 API",
    version="1.0.0"
)

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

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db=Depends(get_db)):
    """회원가입 API"""
    try:
        db_user = create_user(db, user)
        return UserResponse(
            user_id=db_user.user_id,
            id=db_user.id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"회원가입 중 오류가 발생했습니다: {str(e)}"
        )

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db)
):
    """로그인 API - JWT 토큰 발급"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 사용자 ID 또는 패스워드입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 액세스 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user=Depends(get_current_active_user)):
    """현재 로그인한 사용자 정보 조회"""
    return UserResponse(
        user_id=current_user.user_id,
        id=current_user.id
    )

@app.get("/protected")
async def protected_route(current_user=Depends(get_current_active_user)):
    """보호된 라우트 예시 - 인증이 필요한 API"""
    return {
        "message": "인증이 성공했습니다!",
        "user_id": current_user.id
    }

# 사용자 지갑 관련 API들
@app.post("/users/me/wallet", response_model=UserWalletResponse, status_code=status.HTTP_201_CREATED)
async def create_user_wallet(
    wallet_data: UserWalletCreate,
    current_user=Depends(get_current_active_user),
    db=Depends(get_db)
):
    """사용자 지갑 생성 또는 업데이트"""
    try:
        from models import UserWallet
        from decimal import Decimal
        
        # 기존 지갑이 있는지 확인
        existing_wallet = db.query(UserWallet).filter(UserWallet.user_id == current_user.user_id).first()
        
        if existing_wallet:
            # 기존 지갑 업데이트
            existing_wallet.money = Decimal(str(wallet_data.money))
            db.commit()
            db.refresh(existing_wallet)
            return UserWalletResponse(
                user_id=existing_wallet.user_id,
                money=float(existing_wallet.money)
            )
        else:
            # 새 지갑 생성
            new_wallet = UserWallet(
                user_id=current_user.user_id,
                money=Decimal(str(wallet_data.money))
            )
            db.add(new_wallet)
            db.commit()
            db.refresh(new_wallet)
            return UserWalletResponse(
                user_id=new_wallet.user_id,
                money=float(new_wallet.money)
            )
            
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"지갑 생성/업데이트 중 오류가 발생했습니다: {str(e)}"
        )

@app.get("/users/me/wallet", response_model=UserWalletResponse)
async def get_user_wallet(
    current_user=Depends(get_current_active_user),
    db=Depends(get_db)
):
    """사용자 지갑 조회"""
    try:
        from models import UserWallet
        
        wallet = db.query(UserWallet).filter(UserWallet.user_id == current_user.user_id).first()
        
        if not wallet:
            # 지갑이 없으면 기본값 0으로 생성
            wallet = UserWallet(user_id=current_user.user_id, money=0)
            db.add(wallet)
            db.commit()
            db.refresh(wallet)
        
        return UserWalletResponse(
            user_id=wallet.user_id,
            money=float(wallet.money)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"지갑 조회 중 오류가 발생했습니다: {str(e)}"
        )

@app.put("/users/me/wallet/add", response_model=UserWalletResponse)
async def add_money_to_wallet(
    amount: float,
    current_user=Depends(get_current_active_user),
    db=Depends(get_db)
):
    """사용자 지갑에 돈 추가"""
    try:
        from models import UserWallet
        from decimal import Decimal
        
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="추가할 금액은 0보다 커야 합니다."
            )
        
        wallet = db.query(UserWallet).filter(UserWallet.user_id == current_user.user_id).first()
        
        if not wallet:
            # 지갑이 없으면 새로 생성
            wallet = UserWallet(user_id=current_user.user_id, money=Decimal(str(amount)))
            db.add(wallet)
        else:
            # 기존 지갑에 금액 추가 (Decimal로 변환)
            wallet.money += Decimal(str(amount))
        
        db.commit()
        db.refresh(wallet)
        
        return UserWalletResponse(
            user_id=wallet.user_id,
            money=float(wallet.money)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"돈 추가 중 오류가 발생했습니다: {str(e)}"
        )
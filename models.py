from sqlalchemy import Column, TEXT, INT, BIGINT, VARCHAR, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict
from typing import Optional

Base = declarative_base()

# Pydantic 모델들 (API 요청/응답용)
class UserCreate(BaseModel):
    id: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    id: str
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class UserWalletCreate(BaseModel):
    money: float

class UserWalletResponse(BaseModel):
    user_id: int
    money: float
    
    model_config = ConfigDict(from_attributes=True)

# SQLAlchemy 모델들
class User(Base):
    __tablename__ = "user"
    
    user_id = Column(INT, primary_key=True, autoincrement=True)
    id = Column(VARCHAR(50), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    
    # 관계 설정
    wallet = relationship("UserWallet", back_populates="user", uselist=False)
    stock_ownerships = relationship("StockOwnership", back_populates="user")

class UserWallet(Base):
    __tablename__ = "user_wallet"
    
    user_id = Column(INT, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True)
    money = Column(DECIMAL(15, 2), default=0)
    
    # 관계 설정
    user = relationship("User", back_populates="wallet")

class Stock(Base):
    __tablename__ = "stock"
    
    j_id = Column(INT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    explanation = Column(TEXT)
    price = Column(DECIMAL(15, 2), nullable=False)
    
    # 관계 설정
    ownerships = relationship("StockOwnership", back_populates="stock")

class StockOwnership(Base):
    __tablename__ = "stock_ownership"
    
    user_id = Column(INT, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True)
    j_id = Column(INT, ForeignKey("stock.j_id", ondelete="CASCADE"), primary_key=True)
    price_at_time = Column(DECIMAL(15, 2), nullable=False)
    quantity = Column(INT, nullable=False, default=0)
    
    # 관계 설정
    user = relationship("User", back_populates="stock_ownerships")
    stock = relationship("Stock", back_populates="ownerships")
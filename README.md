# KHackarthon Backend API

JWT 인증이 포함된 FastAPI 기반 백엔드 API입니다.

## 🚀 주요 기능

- **회원가입/로그인**: JWT 토큰 기반 인증
- **패스워드 보안**: bcrypt를 사용한 패스워드 해싱
- **사용자 관리**: 사용자 정보 조회 및 관리
- **데이터베이스**: MySQL 연동

## 📋 요구사항

- Python 3.8+
- MySQL 8.0+
- Docker (선택사항)

## 🛠️ 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 데이터베이스 설정
`database.py` 파일에서 MySQL 연결 정보를 수정하세요:
```python
DB_URL = 'mysql://username:password@host:port/database_name'
```

### 3. 데이터베이스 테이블 생성
```bash
python create_tables.py
```

### 4. 서버 실행
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API 엔드포인트

### 인증 관련
- `POST /register` - 회원가입
- `POST /token` - 로그인 (JWT 토큰 발급)

### 사용자 관련
- `GET /users/me` - 현재 사용자 정보 조회 (인증 필요)
- `GET /protected` - 보호된 라우트 예시 (인증 필요)

### 시스템 관련
- `GET /` - API 상태 확인
- `GET /health` - 헬스 체크

## 🔐 인증 사용법

### 1. 회원가입
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"id": "testuser", "password": "testpass"}'
```

### 2. 로그인
```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=testpass"
```

### 3. 보호된 API 호출
```bash
curl -X GET "http://localhost:8000/users/me" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📖 API 문서

서버 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔒 보안 설정

프로덕션 환경에서는 다음 설정을 변경하세요:

1. **SECRET_KEY**: `security.py`에서 환경변수로 관리
2. **토큰 만료 시간**: `ACCESS_TOKEN_EXPIRE_MINUTES` 조정
3. **HTTPS**: SSL/TLS 인증서 적용

## 🐛 문제 해결

### 데이터베이스 연결 오류
- MySQL 서버가 실행 중인지 확인
- 연결 정보(호스트, 포트, 사용자명, 패스워드) 확인
- 데이터베이스가 생성되었는지 확인

### 패키지 설치 오류
- Python 버전 확인 (3.8+)
- 가상환경 사용 권장
- `pip install --upgrade pip` 실행

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/test")
def test_post():
    return {"message": "POST test successful"}

# 테스트 클라이언트로 테스트
client = TestClient(app)

def test_basic():
    response = client.get("/")
    print(f"GET / response: {response.status_code} - {response.json()}")
    
    response = client.post("/test")
    print(f"POST /test response: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    test_basic()

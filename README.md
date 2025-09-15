## backend 실행

```
cd/backend

# 가상환경 생성, 모듈 설치
python -m venv env
source env/bin/activate
pip install -r requirements.txt

# 실행
uvicorn main:app --reload
```
## frontend 실행

```
cd frontend

# 설치
npm install

# 실행
npm run dev
```
# 🚀 Z-Image-Turbo-hosting

**FastAPI + React 기반의 Z Image Turbo 모델 호스팅 프로젝트**

이 프로젝트는 FastAPI를 학습하면서 동시에 Z Image Turbo 기반 이미지 생성 기능을 실제로 활용하기 위해 만든 **Fullstack AI 이미지 생성 서비스**입니다.  
백엔드에서는 Z Image Turbo 모델을 로딩하고 이미지 생성 API를 제공하며, 프론트엔드는 React 기반 웹 UI로 사용자가 직접 이미지를 생성할 수 있도록 구성됩니다.



## 🛠️ Tech Stack

### **Backend (API Server)**
- FastAPI  
- Python 3.11.13
- Diffusers / Z Image Turbo Pipeline  
- Uvicorn  

### **Frontend (Web UI)**
- React (Vite)
- TypeScript
- Axios



## 📁 Project Structure
```
Z-Image-Turbo-hosting/
├── backend/ # FastAPI 서버 (모델 로딩 & 이미지 생성 API)
│ ├── app/
│ └── requirements.txt
├── frontend/ # React 웹 UI
│ ├── src/
│ └── package.json
├── model/ # Z Image Turbo 모델 위치
├── README.md
└── .gitignore
```



## 🚀 How to Run

### 1) Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

# 🚀 Flask App Deployment on Google Cloud Run

This project demonstrates deploying a simple **Flask web application** using **Docker** on **Google Cloud Run**.

It covers:
- Linux scripting
- Docker containerization
- Cloud Build
- Cloud Run deployment

---

## 📂 Project Structure
```
deploy_app/
│── main.py
│── Dockerfile
│── requirements.txt
│── .gitignore
│── README.md
```

---

## 🛠 Technologies Used
- Python  
- Flask  
- Gunicorn  
- Docker  
- Google Cloud Run  
- Google Cloud Build  

---

## ⚙️ Run Locally

### 1. Clone repository
```bash
git clone https://github.com/pragatisingh-sketch/deploy_app.git
cd deploy_app
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Run app
```bash
python main.py
```

Open browser:
```
http://localhost:5000
```

---

## 🐳 Docker Build & Run

Build image:
```bash
docker build -t deploy-app .
```

Run container:
```bash
docker run -p 8080:8080 deploy-app
```

Open:
```
http://localhost:8080
```

---

## ☁️ Deploy to Google Cloud Run

### Login
```bash
gcloud auth login
```

### Set project
```bash
gcloud config set project divine-quest-459017-j2
```

### Build container
```bash
gcloud builds submit --tag gcr.io/divine-quest-459017-j2/hello-cloud-run
```

### Deploy
```bash
gcloud run deploy hello-service \
--image gcr.io/divine-quest-459017-j2/hello-cloud-run \
--platform managed \
--region us-central1 \
--allow-unauthenticated
```

---

## 🌐 Live Service URL
Paste your Cloud Run URL here:

```
https://YOUR-CLOUD-RUN-URL
```

---

## 👩‍💻 Author
**Pragati Singh**  
Cloud & DevOps Learner  

GitHub:  
https://github.com/pragatisingh-sketch

---

## ⭐ Learning Project
This project was created to practice:
- Docker
- Google Cloud Run
- Cloud deployment workflow

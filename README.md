# Chatbot Project with CI/CD 🚀

This project is a simple **chatbot** with:

- **Backend**: FastAPI (`main.py`)
- **Frontend**: Streamlit (`app.py`)
- **Docker** for containerization (`backend.Dockerfile`, `frontend.Dockerfile`, `docker-compose.yml`)
- **GitHub Actions** for CI/CD pipeline

---

## 📂 Project Structure

```
project/
│
├── backend.Dockerfile      # Backend Docker build file
├── frontend.Dockerfile     # Frontend Docker build file
├── docker-compose.yml      # Orchestrates both containers
├── main.py                 # FastAPI backend server
├── app.py                  # Streamlit frontend app
├── .gitignore              # Ignores venv, .env, etc.
├── .dockerignore           # Docker ignores
└── .github/workflows/...   # GitHub Actions pipeline
```

---

## ✅ How it works

- **Backend** runs FastAPI for chatbot logic.
- **Frontend** runs Streamlit for user interface.
- Both run in separate Docker containers.
- **GitHub Actions**:
  - Checks out code on push
  - Installs dependencies
  - Runs syntax checks
  - Builds Docker images
  - Uses secrets securely

---

## 🔑 Environment Variables

You need:

- `GROQ_API_KEY`
- `GOOGLE_API_KEY`

**In GitHub:** Settings → Secrets → Actions → New Repository Secret.

**For local dev:** create `.env`:

```
GROQ_API_KEY=your_groq_key
GOOGLE_API_KEY=your_google_key
```

Add `.env` to `.gitignore`.

---

## 🐳 Run Locally with Docker

**Build & start:**

```
docker-compose up --build
```

**Stop:**

```
docker-compose down
```

**Check containers:**

```
docker ps
```

---

## 🔁 How CI/CD works

- **Every push/pull request** to `main`:
  - GitHub Actions runs `build` job
  - Installs Python + dependencies
  - Runs Python compile checks
  - Builds backend + frontend Docker images

✅ This ensures your build always works.

---

## ⚙️ CI/CD Config

See `.github/workflows/`:

- `actions/checkout` pulls code
- `actions/setup-python` for Python 3.10
- `docker build` for backend/frontend

---

## ✔️ Test CI/CD

1. Make any commit → push.
2. Go to **GitHub → Actions tab**.
3. ✅ Green tick means pipeline passed!

---

## 📌 Notes

- Never commit `.env`.
- Use `docker-compose` locally.
- Keep keys in GitHub Secrets.
- For deploy: push images to Docker Hub or use cloud hosting.

---

## 🏆 Author

Practice project to learn **Docker**, **FastAPI**, **Streamlit**, **GitHub Actions**.

✨ Happy learning!


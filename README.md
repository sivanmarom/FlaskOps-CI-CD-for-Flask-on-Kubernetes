
# 🌐 Personal Portfolio – React & Flask

A fully containerized personal portfolio website built with **React** for the frontend and **Flask** for the backend. This project showcases frontend design, backend integration, CI/CD automation, and a modern DevOps deployment pipeline.

---

## 🖥️ Live Website Features

This portfolio is designed to be both visually appealing and technically impressive.

### ✨ Main Sections

| Section     | Description |
|-------------|-------------|
| `Hero`      | Eye-catching intro with your name, dynamic subtitle (react-type-animation), navigation buttons, and avatar. |
| `About`     | A short personal introduction with professional background. |
| `Skills`    | Visual representation of technologies you're proficient in. |
| `Resume`    | Button to download resume and/or link to LinkedIn profile. |
| `Projects`  | Selected personal projects with descriptions and links. |
| `Contact`   | Contact form connected to EmailJS + direct links to GitHub, Email, LinkedIn. |
| `Navigation`| Sticky scroll-based navigation between sections. |

---

## 🧱 Tech Stack

| Area             | Technologies                            |
|------------------|------------------------------------------|
| Frontend         | React, TailwindCSS, Framer Motion        |
| Backend          | Flask                                    |
| CI/CD            | GitHub Actions                           |
| DevOps           | Docker, Docker Compose                   |
| Container Registry | DockerHub                            |
| Email Services   | EmailJS                                  |
| Deployment       | Render.com (Web Service + Static Site)   |

---

## ✅ What’s Done So Far

### 📦 Development

- Built all React components (Hero, Skills, Projects, Contact, etc.).
- Structured code into clean and reusable components.
- Implemented basic backend API endpoint: `GET /api/hello`.
- Enabled CORS support with `flask-cors`.

---

### 🐳 Docker

- Created separate `Dockerfile`s for `frontend` and `backend`.
- Wrote `docker-compose.yml` to orchestrate both services.
- Ensured networking between containers (frontend uses `backend` hostname).
- CORS issues resolved for cross-service requests.

---

### 🧪 CI with GitHub Actions

- Created workflow: `CI with Docker Compose` that:
  - Checks out the repo
  - Runs `docker-compose up --build`
  - Verifies backend with `curl http://localhost:5000/api/hello`
  - Verifies frontend with `curl http://localhost:3000`
  - Shuts down containers with `docker-compose down`

---

### 🐋 DockerHub Integration

- Added `docker-push` job to:
  - Build and tag Docker images (`latest`)
  - Push frontend & backend images to DockerHub
- Uses GitHub Secrets for secure authentication (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`)

---

### ☁️ Deployment to Render

- Manually created two Render services:
  - `portfolio-frontend`: Static Site
  - `portfolio-backend`: Web Service on port 5000
- Dynamic domain handling in frontend via `window.location.hostname`
- Added GitHub Action `deploy-to-render` job to:
  - Trigger deployment via Render Deploy Hook Web URLs
  - Ensures latest Docker images are used automatically

---

## 🚀 What's Next?

### 🔧 Backend Improvements

- Add database (PostgreSQL or SQLite) for dynamic project management.
- Build full RESTful API with CRUD support for portfolio content.
- Add admin dashboard to manage messages from contact form.
- Extend Flask structure with Blueprints, error handling, and logging.

### 📈 Production Upgrades

- Add analytics (Google Analytics 4 / Hotjar).
- Integrate Sentry or similar tool for backend error logging.
- Set up staging environment for testing changes before production.

---

## 🛠 Local Development

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/portfolio.git
cd portfolio

# Run using Docker Compose
docker compose up --build
```

#### Default URLs:
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:5000/api/hello](http://localhost:5000/api/hello)

---

## 📁 Project Structure

```
portfolio/
│
├── frontend/                  # React app
│   ├── src/
│   │   ├── components/        # Hero, About, Skills, Projects, Contact, etc.
│   │   └── App.jsx
│   └── Dockerfile
│
├── backend/                   # Flask API
│   ├── app.py
│   └── Dockerfile
│
├── docker-compose.yml         # Runs both services together
└── .github/
    └── workflows/
        └── ci.yml             # GitHub Actions workflow
```

---

## 💬 Contact

For suggestions, improvements, or collaboration:
- 📧 [Sivmarom@gmail.com](mailto:Sivmarom@gmail.com)
- 🔗 [LinkedIn](https://www.linkedin.com/in/sivan-marom/)
- 💻 [GitHub](https://github.com/YOUR_USERNAME)

---

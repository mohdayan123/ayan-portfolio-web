# Mohd Ayan — DevOps & AWS Cloud Portfolio (Flask + Docker + Three.js)

A 3D interactive portfolio built of **Mohd Ayan**.

## Project Structure
```
├── app.py                  # Python Flask server (routing, /api/health, /api/contact)
├── templates/
│   └── index.html          # Full single-file 3D Three.js portfolio template
├── requirements.txt        # Flask & Gunicorn dependencies
├── Dockerfile              # Production multi-stage Docker container specification
├── docker-compose.yml      # Docker Compose orchestration
└── index.html              # Standalone web preview
```

---

## 1. Running Locally with Python / Flask

### Prerequisites
- Python 3.10+
- `pip`

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install Flask dependencies
pip install -r requirements.txt

# 3. Run the Flask application
python3 app.py
```
Open your browser at **`http://localhost:5000`**.

---

## 2. Running with Docker Container

```bash
# Build the Docker image
docker build -t ayan-portfolio:latest .

# Run the container
docker run -d -p 5000:5000 --name ayan-devops-core ayan-portfolio:latest
```

Check status and health:
```bash
docker ps
curl http://localhost:5000/api/health
```

---

## 3. Running with Docker Compose

```bash
# Start in detached mode
docker compose up -d

# View real-time logs
docker compose logs -f

# Stop container
docker compose down
```

---

## 4. Deploying via Jenkins CI/CD Pipeline on AWS EC2
This repository is configured to fit the exact CI/CD pipeline workflow highlighted in Mohd Ayan's projects:
1. **GitHub Commit Push**: Developer pushes code changes to GitHub repository.
2. **Jenkins Webhook Trigger**: Jenkins on AWS EC2 catches the webhook and pulls latest commit.
3. **Automated Docker Build**: Jenkins executes `docker build -t ayan/portfolio:v$BUILD_NUMBER .`.
4. **Zero-Downtime Deployment**: Jenkins runs `docker compose up -d --remove-orphans` on the EC2 host.
5. **Healthcheck Verification**: Probes `http://localhost:5000/api/health` before finalizing deployment.

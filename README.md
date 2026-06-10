# 🏦 SecureBank Customer NPS Tracker

A fully automated CI/CD pipeline deploying a two-tier Flask + MySQL application on AWS EC2, built to capture and analyse customer Net Promoter Scores (NPS) across banking service channels.

🔗 **Live Demo:** [bit.ly/securebank-nps](https://bit.ly/securebank-nps)

---

## 📌 Project Overview

This project simulates a real-world banking use case where customers submit satisfaction ratings after interacting with SecureBank services. Feedback is automatically categorised into **Promoters**, **Passives**, and **Detractors** based on NPS methodology. An internal staff dashboard provides real-time visibility into customer sentiment across service channels.

The application is containerised using Docker and deployed on AWS EC2 via a fully automated Jenkins CI/CD pipeline — any code push to GitHub triggers an automatic rebuild and redeployment with zero manual intervention.

---

## 🏗️ Architecture
Developer (GitHub Push)
│
▼
┌─────────────────┐
│   GitHub Repo   │  ← Source of truth
└────────┬────────┘
│ Webhook / Poll
▼
┌─────────────────┐
│    Jenkins      │  ← CI/CD Orchestration (AWS EC2)
│                 │
│ Stage 1: Clone  │
│ Stage 2: Build  │
│ Stage 3: Deploy │
└────────┬────────┘
│
▼
┌──────────────────────────────┐
│         AWS EC2              │
│                              │
│  ┌─────────────────────┐     │
│  │  Flask Container    │     │
│  │  (Port 5000)        │     │
│  └──────────┬──────────┘     │
│             │ two-tier       │
│             │ network        │
│  ┌──────────▼──────────┐     │
│  │  MySQL Container    │     │
│  │  (Port 3306)        │     │
│  └─────────────────────┘     │
└──────────────────────────────┘

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Cloud | AWS EC2, EBS, Elastic IP, Security Groups |
| CI/CD | Jenkins (WAR deployment), Jenkinsfile |
| Containerisation | Docker, Docker Compose |
| Backend | Python 3.9, Flask |
| Database | MySQL |
| Frontend | HTML, CSS, JavaScript |
| Version Control | Git, GitHub |
| OS | Ubuntu 24.04 LTS |

---

## 📁 Repository Structure

├── app.py                  # Flask application
├── Dockerfile              # Flask container definition
├── docker-compose.yml      # Multi-container orchestration
├── Jenkinsfile             # CI/CD pipeline definition
├── requirement.txt         # Python dependencies
└── templates/
├── index.html          # Customer facing feedback form
└── dashboard.html      # Internal staff NPS dashboard

---

## 🔄 CI/CD Pipeline

The Jenkins pipeline consists of 3 automated stages:

**Stage 1 — Clone Code**
Jenkins pulls the latest code from the GitHub repository main branch.

**Stage 2 — Build Docker Image**
Docker builds the Flask application image using the Dockerfile.

**Stage 3 — Deploy with Docker Compose**
Running containers are stopped, and the updated application is redeployed with both Flask and MySQL containers on an isolated Docker network.

```groovy
pipeline {
    agent any
    stages {
        stage('Clone Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Shshank009/AWS-DevOps-Projects.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-app:latest .'
            }
        }
        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker compose down || true'
                sh 'docker compose up -d --build'
            }
        }
    }
}
```

---

## 🚀 How to Deploy

### Prerequisites
- AWS EC2 instance (t2.small or higher recommended)
- Ubuntu 24.04 LTS
- Java 21
- Docker + Docker Compose
- Jenkins

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/Shshank009/AWS-DevOps-Projects.git
cd AWS-DevOps-Projects
```

**2. Install dependencies**
```bash
sudo apt update
sudo apt install docker.io docker-compose-v2 -y
sudo systemctl start docker
sudo usermod -aG docker $USER
```

**3. Run manually with Docker Compose**
```bash
docker compose up -d --build
```

**4. Or trigger via Jenkins pipeline**
- Access Jenkins at `http://<ec2-public-ip>:8080`
- Run the **Two-tier-app** pipeline
- Application deploys automatically

---

## 📱 Application Pages

| Page | URL | Access |
|---|---|---|
| Customer Feedback Form | `http://<ip>:5000/` | Public |
| Staff NPS Dashboard | `http://<ip>:5000/dashboard` | Internal |
| Health Check | `http://<ip>:5000/health` | Internal |

---

## 📊 NPS Methodology

| Category | Rating | Description |
|---|---|---|
| 🟢 Promoter | 9 - 10 | Loyal customers likely to recommend |
| 🟡 Passive | 7 - 8 | Satisfied but not enthusiastic |
| 🔴 Detractor | 1 - 6 | Unhappy customers at risk of churning |

---

## 🔧 Infrastructure Details

- **EC2 Instance:** t2.small (2GB RAM)
- **Storage:** 15GB EBS volume
- **Swap:** 2GB swap space configured
- **Network:** Custom Docker bridge network (`two-tier`)
- **Data Persistence:** MySQL data persisted via Docker named volume
- **Health Checks:** Configured for both Flask and MySQL containers

---

## 🐛 Key Challenges Solved

- Resolved Jenkins GPG key verification failure during installation
- Upgraded Java from 17 to 21 to meet Jenkins latest requirements
- Configured swap space and optimised JVM memory to run on t2.small
- Expanded EBS volume from 8GB to 15GB to accommodate Docker images
- Separated customer-facing UI from internal analytics dashboard

---

## 👤 Author

**Shashank Bankar**
GitHub: [@Shshank009](https://github.com/Shshank009)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

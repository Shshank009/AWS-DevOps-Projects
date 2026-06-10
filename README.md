# 🏦 SecureBank Customer NPS Tracker

A fully automated CI/CD pipeline deploying a two-tier Flask + MySQL application on AWS EC2, built to capture and analyse customer Net Promoter Scores (NPS) across banking service channels.

🔗 **Live Demo:** [bit.ly/securebank-nps](https://bit.ly/securebank-nps)

---

## 📌 Project Overview

This project simulates a real-world banking use case where customers submit satisfaction ratings after interacting with SecureBank services. Feedback is automatically categorised into **Promoters**, **Passives**, and **Detractors** based on NPS methodology. An internal staff dashboard provides real-time visibility into customer sentiment across service channels.

The application is containerised using Docker and deployed on AWS EC2 via a fully automated Jenkins CI/CD pipeline — any code push to GitHub triggers an automatic rebuild and redeployment with zero manual intervention.

---

## 🏗️ Architecture

# 🐳 SkillStack Docker Deployment Guide

This guide covers how to deploy **SkillStack** using **Docker & Docker Compose** on your local machine, a cloud server (AWS, DigitalOcean, Hetzner, Linode), or any Linux VPS.

---

## 📋 Prerequisites

Before deploying, ensure you have installed:
1. **Docker Engine / Docker Desktop**
2. **Docker Compose (`v2+`)**

To verify installation, run:
```bash
docker --version
docker compose version
```

---

## 🚀 Step 1: Start Docker Desktop / Daemon

If you are running on **Windows** or **macOS**:
- Open **Docker Desktop** from your start menu or applications folder and wait until the status says **"Docker Desktop is running"**.

If you are running on a **Linux VPS (Ubuntu / Debian)**:
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

---

## 🛠️ Step 2: Build & Launch Docker Containers

Run the following command in the root directory of the SkillStack project:

```bash
docker compose up --build -d
```

### Explanation of Flags:
- `--build`: Rebuilds the Python application container with all latest code changes.
- `-d`: Runs the containers in detached (background) mode.

---

## 🔍 Step 3: Verify Container Status & Logs

Check if both the Flask Web app (`skillstack_web`) and MySQL Database (`skillstack_db`) containers are running:

```bash
docker compose ps
```

To view live application logs:
```bash
docker compose logs -f web
```

---

## 🌐 Step 4: Access Your Deployed SkillStack Application

Once containers are running:
- **Web App URL**: `http://localhost:5000` or `http://<YOUR_SERVER_IP>:5000`
- **Educator Console**: `http://localhost:5000/admin` (Email: `admin@skillstack.com` | Password: `admin123`)

---

## 🛠️ Useful Management Commands

| Action | Command |
| :--- | :--- |
| **Stop All Containers** | `docker compose stop` |
| **Restart Containers** | `docker compose restart` |
| **View Database Container Logs** | `docker compose logs -f db` |
| **Shutdown & Remove Volumes** | `docker compose down -v` |

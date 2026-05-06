# Domestic Cloud Deployment

Recommended first deployment: Alibaba Cloud ECS + PostgreSQL + Alibaba Cloud Bailian/Qwen.

## Server Preparation

```bash
sudo apt update
sudo apt install -y git python3.11 python3.11-venv nginx
sudo useradd --system --home /opt/work-assistant --shell /usr/sbin/nologin workassistant
sudo mkdir -p /opt/work-assistant
sudo chown -R workassistant:workassistant /opt/work-assistant
```

## Get The Code

Clone the repository on the server:

```bash
sudo -u workassistant git clone https://github.com/albertchang1989/Project_Assistant.git /opt/work-assistant
cd /opt/work-assistant
```

For updates after the first deployment:

```bash
cd /opt/work-assistant
sudo -u workassistant git pull --ff-only
```

## App Setup

```bash
cd /opt/work-assistant
sudo -u workassistant python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
python -m work_assistant.bootstrap
```

## Required Environment

```bash
APP_ENV=production
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/work_assistant
LLM_PROVIDER=qwen
QWEN_API_KEY=replace-with-bailian-key
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus
DINGTALK_APP_SECRET=replace-with-dingtalk-secret
DINGTALK_OUTGOING_WEBHOOK=replace-with-dingtalk-webhook
```

## Service

```bash
sudo cp deploy/systemd/work-assistant.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now work-assistant
```

The systemd unit runs as the dedicated `workassistant` user created during server preparation.

## Nginx

Before copying the Nginx config, replace `your-domain.example.com` in `deploy/nginx/work-assistant.conf` with the real domain that will receive DingTalk callbacks.

```bash
sudo cp deploy/nginx/work-assistant.conf /etc/nginx/sites-enabled/work-assistant.conf
sudo nginx -t
sudo systemctl reload nginx
```

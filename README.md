# 🤖 aisensebot-enterprise

![CI Status](https://img.shields.io/github/actions/workflow/status/your-username/aisensebot-enterprise/ci.yml?branch=main)
![Docker Build](https://img.shields.io/badge/Docker-passing-blue)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
<!-- Suggestion: You can replace the badges below with actual coverage reports from Codecov or Coveralls -->
![Backend Coverage](https://img.shields.io/badge/coverage-backend-passing-green)
![Frontend Coverage](https://img.shields.io/badge/coverage-frontend-passing-green)

## 專案簡介
aisensebot-enterprise 是一個利用 FastAPI、Rasa 與 OpenAI GPT-3.5 打造的企業級 AI 語意機器人架構。它不僅提供一個即時聊天的 Web 介面，更內建了可觀測性、安全性與可擴展性的營運級功能。

## 技術棧
- **後端 (Backend)**: FastAPI, Gunicorn, Uvicorn Workers
- **自然語言理解 (NLU)**: Rasa
- **回覆生成**: OpenAI GPT-3.5
- **前端 (Frontend)**: Vue3, Pinia, Vite, Nginx
- **容器化**: Docker, Docker Compose
- **資料庫**: MongoDB, Redis
- **可觀測性**: Prometheus, Grafana, Jaeger, OpenTelemetry
- **持續整合/部署**: GitHub Actions, Conventional Commits, **Helm Chart**, **Trivy**

## 快速上手
1. 複製專案：`git clone https://github.com/your-username/aisensebot-enterprise.git`
2. 進入專案目錄：`cd aisensebot-enterprise`
3. 複製範例環境變數檔案並填入您的 API Key：
   `cp .env.example .env`
4. 啟動所有服務（首次啟動會自動訓練 Rasa 模型）：`make up`
5. 打開瀏覽器，訪問 `http://localhost:8080` 即可與機器人互動。

## 專案部署
### 分支策略
我們採用基於 `main` 分支的開發模式，所有新功能或 Bug 修復都應從 `main` 分支出來。
### 版本發布流程
詳情請參閱 `docs/RELEASE.md`。我們採用語義化發布，當程式碼合併到 `main` 分支並打上 tag 時，會自動進行 Docker 映像的 Build 與 Push。
### 生產部署 (Production Deployment)
我們推薦使用 Helm Chart 進行部署。詳情請參考 `k8s/README.md`。

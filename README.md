# 🤖 aisensebot-enterprise

![CI Status](https://img.shields.io/github/actions/workflow/status/your-username/aisensebot-enterprise/ci.yml?branch=main)
![Docker Build](https://img.shields.io/badge/Docker-passing-blue)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 專案簡介
`aisensebot-enterprise` 是一個企業級 AI 語意機器人平台，專為高效能、可擴展的對話系統設計。該平台整合了 **FastAPI**、**Rasa** 與 **OpenAI GPT-3.5**，提供即時聊天功能、多語言自然語言理解（NLU）以及智慧回應生成。平台支援從本地開發到 Kubernetes 生產環境的完整部署流程，內建可觀測性（Prometheus、Grafana、Jaeger）與安全性（JWT 認證、Trivy 安全掃描），確保企業級應用的穩定性與可靠性。

本專案旨在為企業提供一個現代化、可客製化的 AI 聊天解決方案，適用於客戶服務、內部支援、產品查詢等多種場景。

## 技術亮點
- **即時雙向通訊**：透過 WebSocket 實現低延遲的聊天體驗，支援即時互動。
- **多語言 NLU**：使用 Rasa 進行意圖識別與實體提取，支援中文（透過 Jieba 分詞與 BERT 模型）及其他語言。
- **智慧回應生成**：整合 OpenAI GPT-3.5，生成自然、專業且上下文相關的回應。
- **企業級安全性**：
  - JWT 認證保護 API 與 WebSocket 端點。
  - Trivy 自動化掃描 Docker 映像漏洞，確保安全部署。
- **高效能與可擴展性**：
  - FastAPI 與 Gunicorn/Uvicorn Workers 提供高並發處理能力。
  - MongoDB 儲存對話歷史，Redis 提供快取與 Session 管理。
- **可觀測性**：
  - Prometheus 與 Grafana 提供即時監控與視覺化指標。
  - Jaeger 實現分佈式追蹤，診斷服務間延遲與錯誤。
  - 結構化日誌（JSON 格式）便於查詢與分析。
- **自動化 CI/CD**：
  - GitHub Actions 實現自動化測試、構建與部署。
  - Conventional Commits 規範與語義化版本控制，自動生成 Release Note。
- **容器化與 Kubernetes 部署**：
  - Docker Compose 支援本地開發。
  - Helm Chart 提供靈活的 Kubernetes 部署方案，支援多環境配置。

## 系統架構
### 服務組成
`aisensebot-enterprise` 採用微服務架構，由以下核心服務組成：
- **前端（Frontend）**：
  - 技術：Vue3、Pinia、Vite、Nginx
  - 功能：提供直觀的聊天介面，支援即時 WebSocket 連線。
- **後端（Backend）**：
  - 技術：FastAPI、Gunicorn、Uvicorn Workers
  - 功能：處理 API 與 WebSocket 請求，協調 NLU 與回應生成服務，管理認證與資料庫操作。
- **自然語言理解（NLU）**：
  - 技術：Rasa、Jieba 分詞、BERT
  - 功能：解析使用者輸入，識別意圖（如 `greet`、`ask_about_product`）與實體（如 `product`）。
- **回應生成（Response Engine）**：
  - 技術：FastAPI、OpenAI GPT-3.5
  - 功能：根據 NLU 解析結果生成自然語言回應，支援客製化提示範本。
- **資料庫**：
  - **MongoDB**：儲存對話歷史與使用者資料。
  - **Redis**：快取 NLU 結果與管理 Session，提升效能。
- **可觀測性**：
  - **Prometheus & Grafana**：監控服務健康狀態與性能指標。
  - **Jaeger**：分佈式追蹤，分析服務間呼叫鏈路。
  - **OpenTelemetry**：整合後端與回應生成服務的追蹤與日誌。

### 數據流
1. 使用者透過前端介面（Vue3）發送訊息，經由 WebSocket 或 REST API 傳至後端。
2. 後端進行 JWT 認證後，將訊息發送至 NLU 服務（Rasa）進行意圖識別與實體提取。
3. NLU 結果透過 Redis 快取後，傳送至回應生成服務（Response Engine）。
4. 回應生成服務使用 GPT-3.5 與客製化提示範本生成回應。
5. 後端將回應透過 WebSocket 傳回前端，展示給使用者。
6. 對話歷史儲存於 MongoDB，效能指標與追蹤資料記錄於 Prometheus 與 Jaeger。

### 架構圖
```
+-------------------+       +-------------------+       +-------------------+
|      Frontend     | <---> |      Backend      | <---> |       NLU         |
| (Vue3, WebSocket) |       | (FastAPI, JWT)    |       | (Rasa, BERT)      |
+-------------------+       +-------------------+       +-------------------+
                                    |                          |
                                    v                          v
+-------------------+       +-------------------+       +-------------------+
|  Response Engine  | <---> |      MongoDB      |       |       Redis       |
| (GPT-3.5, FastAPI)|       | (Conversation)    |       | (Cache, Session)  |
+-------------------+       +-------------------+       +-------------------+
                                    |
                                    v
+-------------------+       +-------------------+       +-------------------+
|    Prometheus     | <---> |      Grafana      |       |      Jaeger       |
|   (Monitoring)    |       | (Visualization)   |       |  (Tracing)        |
+-------------------+       +-------------------+       +-------------------+
```

## 先決條件
- **Git**：用於程式碼管理。
- **Docker & Docker Compose**：用於容器化與本地開發。
- **Node.js (18.x)**：用於前端開發。
- **Python (3.10)**：用於後端與回應生成服務。
- **Helm (v3)**：用於 Kubernetes 部署（生產環境）。
- **Make**：簡化指令執行（可選）。

## 快速上手
1. **複製專案**：
   ```bash
   git clone https://github.com/BpsEason/aisensebot-enterprise.git
   cd aisensebot-enterprise
   ```
2. **設定環境變數**：
   ```bash
   cp .env.example .env
   ```
   編輯 `.env` 檔案，填入 `OPENAI_API_KEY`、 `JWT_SECRET` 等必要變數。
3. **啟動服務**：
   ```bash
   make up
   ```
   或：
   ```bash
   docker-compose -f docker-compose.dev.yml up -d --build
   ```
   首次啟動會自動訓練 Rasa 模型。
4. **訪問介面**：
   打開瀏覽器，訪問 `http://localhost:8080`。
5. **停止服務**：
   ```bash
   docker-compose -f docker-compose.dev.yml down
   ```

## 專案結構
```
aisensebot-enterprise/
├── backend/                    # FastAPI 後端服務
├── frontend/                   # Vue3 前端應用
├── nlu/                        # Rasa NLU 服務
├── response-engine/            # GPT-3.5 回應生成服務
├── e2e/                        # Cypress 端到端測試
├── helm/                       # Helm Chart 用於 Kubernetes 部署
├── docs/                       # 文件（架構、API 參考等）
├── .github/                    # GitHub Actions 與模板
├── docker-compose.yml          # 生產環境 Docker Compose 配置
├── docker-compose.dev.yml      # 開發環境 Docker Compose 配置
├── .env.example                # 環境變數範例
├── .gitignore                  # Git 忽略檔案
├── .dockerignore               # Docker 忽略檔案
├── CHANGELOG.md                # 變更日誌
├── LICENSE                     # MIT 許可證
├── README.md                   # 本文件
└── wait-for-it.sh              # 服務啟動等待腳本
```

## 部署指南
### 分支策略
- `main`：穩定分支，用於生產部署。
- `feat/*`：新功能開發。
- `fix/*`：Bug 修復。
- `docs/*`：文件更新。

### 版本發布
- 採用 **Conventional Commits** 規範，自動生成語義化版本與 Release Note。
- 當程式碼合併到 `main` 分支並打上 Git Tag 時，GitHub Actions 會：
  1. 執行測試與 Trivy 安全掃描。
  2. 構建並推送 Docker 映像至 Docker Hub。
  3. 自動生成 Release Note 並發佈至 GitHub。

### 生產部署
使用 Helm Chart 進行 Kubernetes 部署：
1. 安裝 Helm Chart：
   ```bash
   helm install aisensebot-release ./helm
   ```
2. 自訂配置：
   ```bash
   helm install aisensebot-release ./helm -f my-values.yaml
   ```
   或：
   ```bash
   helm install aisensebot-release ./helm --set secrets.openAIKey="your-key"
   ```
3. 升級部署：
   ```bash
   helm upgrade aisensebot-release ./helm
   ```
詳情請參閱 `k8s/README.md`。

## 開發指南
### 本地開發
- 使用 VSCode 與 DevContainer 確保一致的開發環境。
- 安裝 `pre-commit` 執行程式碼檢查：
  ```bash
  pip install pre-commit
  pre-commit install
  ```
- 執行測試：
  ```bash
  docker-compose -f docker-compose.dev.yml up -d
  pytest backend/tests response-engine/tests
  npm run test --prefix frontend
  ```

### 貢獻程式碼
- 遵循 `docs/CONTRIBUTING.md` 中的指南。
- 使用 Conventional Commits 規範提交 Pull Request。
- 確保通過 Lint、Type-check 與所有測試。

### 測試與品質
- **單元測試**：後端與回應生成服務使用 `pytest`，前端使用 `Vitest`。
- **端到端測試**：使用 Cypress 測試前端與 API 整合。
- **程式碼品質**：Flake8、MyPy、ESLint 確保程式碼一致性。
- **安全掃描**：CI/CD 流程整合 Trivy，掃描 Docker 映像漏洞。

## 可觀測性
- **監控**：Prometheus 收集指標，Grafana 提供視覺化儀表板。
- **追蹤**：Jaeger 提供分佈式追蹤，分析服務間延遲。
- **日誌**：結構化 JSON 日誌，支援集中式日誌管理。

## 提示工程
- 提示範本儲存於 `response-engine/prompt_templates/`。
- 參閱 `docs/PROMPTS.md` 了解如何設計與最佳化 GPT-3.5 提示。

## 聯繫與支援
- **問題回報**：在 GitHub 提交 Issue，使用模板。
- **討論**：參與 GitHub Discussions。
- **文件**：參閱 `docs/` 目錄（如 `ARCHITECTURE.md`、`API_REFERENCE.md`）。

## 許可證
本專案採用 **MIT 許可證**，詳情見 `LICENSE` 檔案。

## 致謝
感謝以下開源專案的支持：
- FastAPI、Rasa、OpenAI、Vue3、Docker、Kubernetes、Helm、Prometheus、Grafana、Jaeger 等。

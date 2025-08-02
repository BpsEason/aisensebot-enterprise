# 專案架構 (Project Architecture)

## 概覽 (Overview)
aisensebot-enterprise 是一個微服務導向的 AI 聊天機器人平台，由多個獨立服務協同工作，確保高可擴展性、可維護性與可觀測性。

## 服務組成
- **`frontend`**: 使用 Vue3 構建的單頁應用程式 (SPA)，提供使用者介面。
  - **技術棧**: Vue3, Pinia, Vite, Nginx。
- **`backend`**: 核心業務邏輯服務，使用 FastAPI 實現。
  - **功能**: 處理使用者請求、路由至不同服務、管理 WebSocket 連線、使用者認證 (JWT)。
  - **技術棧**: FastAPI, Gunicorn, Uvicorn Workers, JWT, Redis, MongoDB。
- **`nlu`**: 自然語言理解服務，使用 Rasa 開發。
  - **功能**: 解析使用者輸入，識別「意圖 (Intent)」與提取「實體 (Entity)」。
  - **技術棧**: Rasa Open Source。
- **`response-engine`**: 回應生成服務，使用 OpenAI GPT-3.5 API。
  - **功能**: 根據 NLU 提供的意圖和實體，生成更自然、流暢的對話回覆。
  - **技術棧**: FastAPI, OpenAI API。
- **`mongodb`**: 儲存對話歷史、使用者資料等持久化數據。
- **`redis`**: 用於 NLU 快取、Session 管理等，提升效能。
- **`jaeger`**: 分佈式追蹤系統，用於監控服務間的呼叫鏈路，提升可觀測性。
- **`prometheus`**: 監控系統，從各個服務收集指標。

## 數據流 (Data Flow)
1.  **使用者輸入**: 前端 (Frontend) 透過 WebSocket 或 REST API 向後端 (Backend) 發送使用者訊息。
2.  **訊息處理**: 後端服務接收訊息，進行 JWT 驗證與初步處理。
3.  **NLU 解析**: 後端將訊息發送給 NLU 服務，NLU 服務回傳「意圖」和「實體」。
4.  **回應生成**: 後端將 NLU 結果發送給 Response Engine，由其生成最終的自然語言回覆。
5.  **回覆發送**: 後端將回覆透過 WebSocket 或 REST API 發送回前端，展示給使用者。

## 部署架構 (Deployment)
- **本地開發**: 透過 `docker-compose.dev.yml` 啟動所有服務，提供一致的開發環境。
- **生產環境**: 我們推薦使用 **Helm Chart** (`helm/` 目錄)，它提供了可配置的部署範本，能輕鬆管理不同環境下的設定。
- **安全性**: CI/CD 流程中已整合 **Trivy** 掃描，自動檢查容器映像與依賴中的安全漏洞。

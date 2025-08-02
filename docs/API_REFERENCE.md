# API 參考 (API Reference)

## 後端服務 (Backend Service)
### 健康檢查 (Health Check)
`GET /health`
- **描述**: 檢查服務是否正常運行。
- **回應**:
  - `200 OK`
  ```json
  {"status": "ok", "message": "Service is healthy"}
  ```

### 聊天 API (Chat API)
`POST /api/chat/message`
- **描述**: 透過 REST 方式發送訊息並取得回應。
- **請求主體**:
  ```json
  {
    "user_id": "string",
    "text": "string"
  }
  ```
- **回應**:
  - `200 OK`
  ```json
  {
    "intent": "string",
    "slots": {
      "key": "value"
    }
  }
  ```

### WebSocket 端點 (WebSocket Endpoint)
`ws://<backend_url>/chat`
- **描述**: 建立即時雙向通訊連線，用於聊天。
- **連線**: `new WebSocket("ws://<backend_url>/chat")`
- **傳送訊息**: `socket.send("Hello, bot!")`
- **接收訊息**:
  ```json
  {
    "user_id": "bot",
    "text": "Hello, how can I help you?"
  }
  ```

## 認證服務 (Auth Service)
`POST /api/auth/token`
- **描述**: 登入並取得 JWT Access Token。
- **請求主體**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **回應**:
  - `200 OK`
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```
- **錯誤回應**:
  - `401 Unauthorized`
  ```json
  {"detail": "Incorrect username or password"}
  ```

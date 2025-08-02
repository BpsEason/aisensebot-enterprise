# 貢獻指南 (Contribution Guide)

感謝您對 aisensebot-enterprise 的關注與貢獻！本文件將引導您如何參與專案。

## 報告 Bug 與提出功能
- 在提交 Issue 前，請先搜尋現有議題，避免重複。
- **回報 Bug**: 請使用 `bug_report.md` 模板，詳細說明問題、重現步驟、預期與實際結果。
- **提出功能**: 請使用 `feature_request.md` 模板，簡要描述您的想法和解決方案。

## 提交 Pull Request (PR)
- 請使用 `pull_request_template.md` 模板。
- **分支規範**:
  - `main`: 主要穩定分支，用於部署到生產環境。
  - `feat/feature-name`: 功能開發分支。
  - `fix/bug-name`: Bug 修復分支。
  - `docs/doc-name`: 文件更新分支。
  **重要**: 請遵守 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 規範，這將有助於自動生成 CHANGELOG。
- **流程**:
  1. Fork 專案並從 `main` 分支出一個新分支。
  2. 使用 `pre-commit install` 安裝 Git Hooks，確保您的程式碼符合規範。
  3. 進行您的程式碼變更。
  4. 確保所有 Lint、測試與 Rasa 資料驗證都通過。
  5. 提交 PR 到 `main` 分支，並填寫 PR 模板。

## 開發環境
- **一鍵啟動**: 推薦使用 VSCode 開啟此專案，它會自動偵測 `.devcontainer` 並詢問您是否要在容器內重新開啟。這將為您提供一個與生產環境一致的標準化開發環境。
- **本地啟動**: 請參閱 `README.md` 中的「快速上手」部分，使用 `make up` 啟動所有服務。

## 程式碼品質與安全性
- 本專案使用 **pre-commit** 工具，在每次提交時自動執行格式化、Lint 與 Type-check。
- 在 CI/CD 中，我們建議整合 **Snyk** 或 **GitHub CodeQL** 等工具，進行自動化的安全漏洞掃描，以確保依賴與程式碼的安全性。

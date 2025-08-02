# 版本發布流程 (Release Process)

本專案採用自動化的語義化發布 (Semantic Release) 流程，以確保發布的穩定性與一致性。

## 步驟
1. **遵守 Conventional Commits**: 確保所有合併到 `main` 分支的 Commit 訊息都遵循 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 規範。
2. **打上 Git Tag**:
   - 當您將 Commit 合併到 `main` 分支後，語義化發布工具（例如 `semantic-release`）會自動判斷版本號。
   - 根據 Commit 訊息，自動生成 `v1.0.0`、`v1.0.1` 或 `v2.0.0` 等 tag，並推送到 GitHub。
3. **觸發 CI/CD Pipeline**:
   - `build_and_push` 的 GitHub Actions 會被觸發。
   - Pipeline 會自動 Build 新的 Docker 映像並 Push 到 Docker Hub。
4. **自動生成 Release Note**:
   - GitHub Actions 會使用 `auto-changelog` 或類似工具，根據 Commit 訊息自動生成詳細的發布紀錄，並發佈到 GitHub Release 頁面。

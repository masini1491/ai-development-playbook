# AGENTS.md

## AI Development Playbook baseline

本專案採用 `masini1491/ai-development-playbook` 作為共通 AI 開發基準。

Playbook baseline: `main`

需要可重現 baseline 時，把上面唯一的 baseline declaration 改成已發布 tag，例如 `v0.1.0`；不要同時保留多個 active baseline declaration。

新 ChatGPT／AI／coding-agent session：

1. 先確認目前真正的 target repository 與 branch／workspace identity。
2. 讀取所選 Playbook baseline 的 `CHAT_INIT.md`。
3. 只依目前 Task 路由到最低必要 canonical section；不要完整掃描整份 Playbook。
4. 再讀本專案 current governance、current coordination surface（若有）與本次 Task 直接相關的正式 source of truth。

## Authority boundary

本檔與本 repository 的正式 technical／governance source of truth 保存專案專屬權威。

若 project-specific authority 與 common Playbook 衝突，以 project-specific authority 為準；若使用者當次明確指示合法覆蓋既有規則，依該指示處理。

**採用 Playbook 本身不會新增 ChatGPT、Codex 或其他 agent 的 repository write、execution、deployment、secret 或 external-service authority。** 任何權限仍由本專案自己的 governance 明確授予。

## Project-specific minimum contract

請把下列 placeholder 改成你的專案實際內容；沒有的項目寫 `none`，不要猜測：

- Canonical technical source(s): `<path / document / source>`
- Current coordination surface: `<TASKS.md / equivalent / none>`
- Required validation: `<command / document / manual gate / none>`
- Project-specific exceptions or restrictions: `<rules / none>`

完成 adoption normalization 後，這份 declaration layer 應能讓 Adoption Doctor deterministic 確認 bootstrap、single baseline、project authority、coordination／validation declaration 與 no-authority-expansion boundary；更詳細的 project governance 留在本 repository 自己的 canonical owner，不要為了通過 Doctor 重複搬進本區塊。

核心原則：**Common Playbook 管協作方法；本 repository 管自己的產品真相、權限與完成標準。**

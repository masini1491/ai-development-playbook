# AGENTS.md

## AI Development Playbook baseline

本專案採用 `masini1491/ai-development-playbook` 作為共通 AI 開發基準。

Playbook baseline: `main`
Project AI mode: `<ChatGPT-Only | ChatGPT+Codex>`

Shared reporting contract: declared Playbook baseline → `REPORTING.md`
Applicability: always-on for substantive user-facing engineering replies; independent of other shared Playbook activation

需要可重現 baseline 時，把上面唯一的 baseline declaration pin 到已發布 tag（例如 `v0.1.0`）或 exact 40-character commit SHA；也可以使用 project-declared named ref。Floating ref 由 activation contract resolve 成當次 exact revision；不要同時保留多個 active baseline declaration。

`Project AI mode` 只接受 `ChatGPT-Only` 或 `ChatGPT+Codex`。若尚未選擇，不要猜第三種模式；依 Playbook 保守 fallback 處理，直到使用者／project governance 明確選定。完整語意見 Playbook `PROJECT_MODES.md`。

新 ChatGPT／AI／coding-agent session：

1. 先確認目前真正的 target repository 與 branch／workspace identity。
2. 先讀本專案 current governance，並依本次 Task 需要讀 current coordination surface／task authority；從這些 project-native authority 解析目前的 `Project AI mode` 與 activation route。
3. Shared `REPORTING.md` 是窄化的 adoption-level exception：只要形成 substantive user-facing engineering reply，就依 declared baseline 的 reporting contract；即使本題維持 project-native route也適用，且不因此 activate `CHAT_INIT.md` 或其他 shared owners。
4. 若本專案明確提供 project-native bootstrap／task router，且它判定本次 Task 不需要其他 shared Playbook governance，維持 project-native route；不要只因本專案已採用 Playbook 就讀 shared `CHAT_INIT.md`。
5. 若其他 shared Playbook activation 需要成立（或本專案沒有更窄的 native activation gate），依本檔唯一的 declared baseline 解析當次 exact revision，再讀該 revision 的 `CHAT_INIT.md`，並只載入本次 Task 最低必要的 canonical owner／section；不要完整掃描整份 Playbook。
6. 依 current project authority 與 routed canonical contract 繼續工作；只有 `ChatGPT+Codex` 才把 Codex 納入 repository workflow，且 adoption／reporting／mode／tool capability 本身都不擴張 Task、write、execution 或 completion authority。

## Authority boundary

本檔與本 repository 的正式 technical／governance source of truth 保存專案專屬權威。

若 project-specific authority 與 common Playbook 衝突，以 project-specific authority 為準；若使用者當次明確指示合法覆蓋既有規則，依該指示處理。

**採用 Playbook 或選擇 Project AI mode 本身，不會跳過 Current Write Target、Task/Stage authorization、execution permission、credential、validation、release/deployment 或其他 project-specific authority。**

- `ChatGPT-Only`：ChatGPT 是 repository 的 AI maintainer；在本專案明確權限與目前 Task/Stage 範圍內，可承擔 research、planning、docs、source、tests、tooling、validation 與合法 Git mutation。Codex 不介入。
- `ChatGPT+Codex`：ChatGPT 負責 research／planning／architecture／coordination／review／reconciliation；Codex 參與被 project governance／current Stage 指派的 implementation mutation。Actor choice 仍依 current responsibility，不因上一 Stage 用過 Codex 就慣性 handoff。

Human maintainer、CI、hardware validation、external service 等仍可依 project governance 參與；它們不形成第三種 AI project mode。

## Project-specific minimum contract

請把下列 placeholder 改成你的專案實際內容；沒有的項目寫 `none`，不要猜測：

- Canonical technical source(s): `<path / document / source>`
- Current coordination surface: `<TASKS.md / equivalent / none>`
- Required validation: `<command / document / manual gate / none>`
- Project-specific exceptions or restrictions: `<rules / none>`

只有當 project-specific exception 真正需要縮窄某個 mode 的 path/action responsibility 時才補例外；不要為了形式另建第三種 actor topology。

完成 adoption normalization 後，這份 declaration layer 應能讓 AI 直接辨識 repository identity、project-native activation decision、single baseline、shared reporting thin pointer、兩種 Project AI mode 之一、project authority、coordination／validation declaration 與 no-authority-expansion boundary；更詳細的 project governance 留在本 repository 自己的 canonical owner，不要重複搬進本區塊。

核心原則：**開案只選 `ChatGPT-Only` 或 `ChatGPT+Codex`；project governance 再決定該 mode 在這個 repository 的實際 path/action 邊界。**
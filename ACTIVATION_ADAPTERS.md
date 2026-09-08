# Thin Activation Adapters

> **Role**：把不同 AI runtime 導向同一個 Playbook bootstrap；本檔是 distribution / activation adapter，不是新的 policy authority。
>
> **Authority**：實際規則仍以目標 project governance、`CHAT_INIT.md` 與其 routed canonical owner 為準。`PLAYBOOK_INDEX.json` 只提供 machine-readable discovery，不保存 current project state。

## Adapter contract

任何 runtime 只需要完成：

`Verify / resolve project workspace → read project AGENTS.md → resolve declared Playbook baseline（floating ref → cheap exact revision）→ optionally read PLAYBOOK_INDEX.json for machine discovery → read CHAT_INIT.md → route minimum-sufficient canonical owner → obey project-specific authority`

若 requested project 不是目前已驗證 workspace：不要用舊聊天、memory、repository name 或相似專案內容補成 current state。Runtime 支援 workspace / folder selection 或 access request 時，先請使用者開啟、選取或授權正確 project workspace，再重新執行 repository identity verification；不得自行掃描無關 filesystem、切換、clone 或猜測另一個 repository。詳細 repository identity / permission gate 仍由 `REPOSITORY_EXECUTION.md` 擁有。

若 project 採用 floating Playbook baseline（例如 `main`），在把該 baseline 視為本次 identified activation baseline 前，先用最低成本、已允許的 read-only identity probe resolve 成 exact immutable revision。Moving ref 只用來選 revision；後續需要 same-revision consistency 時仍依 `INFORMATION_INTEGRITY.md` 的 Snapshot Consistency Guard。這不要求 full clone、full fetch 或全文掃描 Playbook。

若只知道 project「採用 Playbook」但尚未從 current project governance 讀到 declared baseline，該 baseline 應維持 **unresolved**；不得因 host instruction、舊聊天或本 Playbook 的 current `main` 存在，就自行把 `main` 當成目標 project 的 default baseline。

若上述必要的 read-only workspace／repository identity／Playbook baseline probe 因 sandbox、filesystem、metadata、network 或類似 execution permission 被阻擋，不應直接把 dependency 判成 unavailable。Runtime 若能 request approval／access，先向使用者要求完成該 exact read-only operation 所需的最低 permission，核准後只重試原本被 gate 阻擋的操作；approval 不擴張 task scope、mutation、commit/push、deployment、credential 或其他 network/Git authority。若 preferred read mechanism 仍不可用，才改用目前可用且已允許的其他 canonical read-only acquisition path；**fail over the read mechanism, not the authority**。只有 approval unavailable／denied、permission 後原操作仍失敗，且沒有其他合法 canonical read path 時，才標記對應 bootstrap dependency unresolved／unavailable。完整 permission semantics 仍由 `REPOSITORY_EXECUTION.md` 擁有，adapter 只保存 bootstrap survival pointer。

Adapter 不應：

- 複製完整 Playbook policy 到 tool-specific config；
- 把 `PLAYBOOK_INDEX.json` 當成 policy/state authority；
- 因 runtime 有 filesystem / connector / credential capability 就擴張 write 或 execution scope；
- 宣稱 native hook / installer 已存在，除非該 runtime 實際另有 adapter implementation。

## Generic bootstrap payload

可放入支援 persistent instruction / project rule / startup prompt 的 runtime：

```text
Verify that the current workspace is the requested project repository. If it is not, ask the user to open/select/grant the correct workspace and re-verify; do not infer project state from prior context.
Read this project's current AGENTS.md and determine whether it adopts masini1491/ai-development-playbook.
If adopted, resolve the project's declared Playbook baseline. For a floating ref, use the cheapest permitted read-only probe to identify the exact revision.
If a required bootstrap read/probe is permission-gated and the runtime can request approval, ask for the minimum permission needed for that exact read-only operation, then retry only that operation. If the preferred read mechanism still fails, use another permitted canonical read-only path when available; do not fall back to memory or expand authority.
Then read that revision's CHAT_INIT.md and load only the minimum-sufficient canonical sections for the current task. Do not use the Playbook README as a normal bootstrap router.
For machine-readable discovery you may consult PLAYBOOK_INDEX.json when actually needed, but it is routing-only.
Project-specific governance and technical source of truth remain higher authority.
Do not infer repository write or execution authority from access capability.
```

## ChatGPT — copy-ready custom instruction

ChatGPT 的人類安裝用 persistent Custom Instructions 已獨立成純文字 distribution artifact：

[`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt)

這個 `.txt` 檔案只保存要貼進 ChatGPT Settings / Personalization / Custom Instructions 的完整 thin-bootstrap payload；沒有 Markdown code fence、前言或診斷文字。它是 user-level host adapter，不是 project-specific policy，也不會因被安裝就讓任何 project 自動採用 Playbook。

目前 distribution contract 將 payload 維持在 **5,000 characters 以內**，以符合本 adapter 目前人工驗證時 ChatGPT Custom Instructions 欄位的限制；這是 product-version-specific installation constraint，不是 Playbook policy authority。若產品限制改變，應更新 distribution artifact／validator，而不是複製更多 policy 進 host setting。

Loading contract：

- 一般 project bootstrap **不得因為這個檔案存在就讀取它**；
- 只有安裝／更新 ChatGPT Custom Instructions、`ChatGPT Host Instruction Health Check`、設定 drift 比對，或維護這個 distribution artifact 本身時才需要讀取；
- normal project task 仍由 project governance 決定是否採用 Playbook、採用哪個 baseline，再進 `CHAT_INIT.md`；
- 安裝／更新後使用 **fresh chat regression** 驗證，不把既有聊天室的舊 context 當成 host instruction 已生效的證據。

## ChatGPT Host Instruction Health Check

只有 fresh ChatGPT session 出現具體 activation／bootstrap symptom，才做 bounded Host Instruction Health Check；不要把一般回答錯誤、source/test failure 或單次 wording 差異都歸因於 Custom Instructions。

可觸發檢查的 material signals 包括：

- 未建立 target repository／project current identity 就直接使用 prior chat、memory 或 stale project facts；
- 未讀 current project governance 就自行套用 Playbook；
- 只知道 project「採用 Playbook」，卻在 declared baseline 尚未建立時自行預設 Playbook current `main`；
- project 已採用 Playbook但 fresh chat 跳過 declared baseline／`CHAT_INIT.md`，或無必要 broad-scan README／whole Playbook；
- generic continuation（例如「好，繼續」）把 AI-originated observation 自動升格成 canonical／executable work；
- 把 connector／filesystem／network／runtime capability 或 permission approval 當成 mutation／scope authority；
- 同類 activation behavior 在 fresh sessions 重複偏離 current adapter contract。

Health Check 建議流程：

`Fresh-chat anomaly → canonical/project reconciliation → activation mismatch plausible? → inspect current adapter revision → ask user to verify ChatGPT Custom Instructions only if needed → compare against CHATGPT_CUSTOM_INSTRUCTIONS.txt → full replacement if missing/stale/mixed → minimal fresh-chat regression`

一般原則：

- 除非產品實際提供 settings-read/write capability，ChatGPT 不得假裝能直接看到或修改使用者的 Custom Instructions；必要時請使用者開啟設定、貼出文字或截圖。
- 先確認 Playbook current adapter revision，再比對 host setting；不要拿舊聊天室中的 payload 當 current expected value。
- 若設定缺失、過期、混合多版或 materially inconsistent，使用 [`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt) **整段覆蓋**，不要做 delta patch。
- 若設定 current 但 behavior 仍偏離，優先用最小 fresh-chat regression 區分 product/runtime behavior 與設定 drift。
- Health Check 只做 diagnosis／recovery，不建立 project task、擴張 mutation authority，或把 runtime anomaly 自動持久化成 repository obligation。

核心原則：**先證明是 fresh-session activation symptom，再檢查 host instruction；project governance／declared baseline 仍是實際專案 authority。**

## ChatGPT-side Codex Host Instruction Health Check

當 ChatGPT 收到 Codex 回報時，先依 project／Playbook current authority 做一般 result reconciliation。只有回報出現**具體 activation／bootstrap symptom**，才觸發 bounded Host Instruction Health Check；不要把任何 Codex 錯誤都直接歸因於個人化設定。

可觸發檢查的 material signals 包括：

- 已驗證 workspace／repository 與 Codex 回報使用的 repository identity 不一致，且不像單純 project-state drift；
- project `AGENTS.md` 明確採用 Playbook，但 Codex 聲稱未採用，或跳過 declared baseline；
- floating baseline 應 resolve exact revision，Codex 卻完全未做 identity probe、用 memory 猜 SHA，或把 moving ref 冒充 immutable revision；
- 必要 read-only bootstrap probe 被 permission gate 阻擋，而 runtime 明明可 request approval，Codex 卻直接宣告 unavailable；
- Codex 在一般 bootstrap 無必要地讀 Playbook README、whole Playbook、BACKLOG／Cold／history 或做 broad repository scan；
- Codex 把 persistent host instruction、filesystem／network capability 或 permission approval 當成 mutation／scope expansion authority；
- 同類 activation behavior 在 fresh session 重複偏離 current adapter contract。

不應單獨觸發 host-instruction diagnosis 的例子：單次 timestamp 錯誤、source/test failure、正常 network outage、project technical mismatch、validation failure；這些先依各自 canonical owner 分類，除非另有 evidence 指向 activation／host config drift。

Health Check 建議流程：

`Codex report anomaly → canonical/project reconciliation → classify symptom → activation mismatch plausible? → inspect current adapter identity → ask user to verify Codex personal instruction only if needed → compare against CODEX_DESKTOP_INSTRUCTIONS.txt → full replacement if missing/stale/mixed → minimal fresh-chat regression`

一般原則：

- ChatGPT 不得假裝能看到或修改使用者的 Codex 個人化設定；若產品沒有 settings-read/write capability，請使用者到 Codex Settings / Personalization / Codex Instructions 檢查，並在必要時貼出文字或截圖。
- 先確認 Playbook current adapter revision，再比較設定，避免拿舊聊天室裡的 host instruction 當 current expected value。
- 若設定缺失、過期、混合多版或 materially inconsistent，提供 [`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt) 的**完整內容作為整段覆蓋來源**；不要只給 delta patch 造成殘留規則。
- 若設定看起來 current，但 behavior 仍不符，優先跑最小 fresh-chat regression 區分 runtime／permission／product behavior 與設定 drift，不反覆要求使用者重貼同一內容。
- Health Check 是 diagnosis／recovery，不授權修改 project repository、擴張 current task、或把 Codex runtime bug 持久化成 project work。

核心原則：**先證明是 activation symptom，再檢查 host instruction；不要把任何怪回報都當成設定壞掉。**

## Codex Desktop — copy-ready persistent instruction

Codex Desktop 的人類安裝用 persistent instruction 已獨立成純文字 distribution artifact：

[`CODEX_DESKTOP_INSTRUCTIONS.txt`](CODEX_DESKTOP_INSTRUCTIONS.txt)

這個 `.txt` 檔案**只保存要貼進 Codex 個人化指示欄位的完整 payload**；沒有 Markdown code fence、前言、診斷說明或其他周邊文字，目的就是降低人工複製時混入其他內容的風險。

使用方式：開啟該檔 → 全選 → 複製 → 完整取代 Codex Settings / Personalization / Codex Instructions 的現有內容。

Loading contract：

- 一般 project bootstrap **不得因為這個檔案存在就讀取它**；
- 只有安裝／更新 Codex 個人化指示、Host Instruction Health Check、設定 drift 比對，或維護這個 distribution artifact 本身時才需要讀取；
- `CODEX_DESKTOP_INSTRUCTIONS.txt` 是 human-installable distribution artifact，不是新的 policy authority；其語意仍由本檔與 routed canonical owners 擁有。

這個分離讓 `ACTIVATION_ADAPTERS.md` 保持 adapter semantics / diagnosis owner，而 `.txt` 只負責安全、明確的人工作業複製邊界。

## Runtime mappings

| Runtime family | Thin activation use |
| --- | --- |
| ChatGPT | For persistent user-level setup, install [`CHATGPT_CUSTOM_INSTRUCTIONS.txt`](CHATGPT_CUSTOM_INSTRUCTIONS.txt) as a thin host adapter; project/work instructions may still use the generic bootstrap. In both cases, actual project adoption/baseline must come from current project governance before `CHAT_INIT.md`. |
| Codex / coding agent | Prefer project `AGENTS.md` as the activation surface; the launch prompt should point to current project governance rather than copy Playbook rules. If the selected workspace is not the requested repository, request the minimum user workspace/access correction and re-run identity verification before loading project state. |
| Claude Code / Cursor / Gemini / other coding assistants | Use the runtime's persistent project-instruction surface, if available, only to install the generic bootstrap pointer; keep detailed rules in the Playbook. |
| Custom CLI / IDE extension | Parse `PLAYBOOK_INDEX.json` for stable capability IDs / owner pointers, then read the canonical Markdown owner before making a decision. |

## Activation maturity boundary

This repository now provides **manual thin activation adapters + copy-ready ChatGPT/Codex host payloads + machine-readable routing discovery**. It does **not** claim native marketplace installers, hooks, generated per-tool command packs, or automatic startup integration for every runtime.

Core principle: **Activate by pointer, not policy copy.**

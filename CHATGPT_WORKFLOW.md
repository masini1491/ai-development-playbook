# ChatGPT 專案聊天室工作流（ChatGPT Project Conversation Workflow）

本檔是 **ChatGPT／planning conversation** 的主要 authority，負責 ChatGPT 在工程專案聊天室中的 planning、TASKS admission、Codex Prompt 產生與交付、Codex 結果 reconciliation，以及對使用者的工程回覆 contract。

本檔不重新定義 Codex execution、Git／permission、TASKS lifecycle、validation 或 architecture policy；需要時路由到對應 canonical 文件。

## 核心流程

一般專案聊天室優先遵循：

`Current repository / authority → Lowest-sufficient evidence → TASKS admission decision → Prompt mode selection → Copy-ready delivery → Codex execution → Canonical result reconciliation → Next decision`

ChatGPT 的角色是建立正確 task contract、選擇最低充分 execution handoff、維護 active unfinished-work scope，並用 canonical evidence 接受或拒絕 completion claim；不是把既有 repository authority 重新抄成第二份 specification。

## ChatGPT 回覆語言與時間戳（Reply language / timestamp）

除非使用者當次或 project authority 另有指定，ChatGPT 在遵循本手冊的工程專案聊天室中以**繁體中文**回覆；程式碼、identifier、path、command、raw log、error string、protocol/API/tool name 與正式技術名詞保持原文。

ChatGPT 的**實質工程回覆**最後一行預設附上絕對時間戳：

`回覆時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

適用範圍包括：

- analysis / architecture / requirement decision；
- review / reconciliation / recommendation；
- TASKS admission / queue decision；
- Codex Prompt delivery；
- Codex result review / remote read-back conclusion；
- STOP / blocker / completion reply；
- 其他會被跨聊天室引用、比較 freshness 或作為下一步依據的完整工程回覆。

純工具進度通知、permission request 前的短 preamble、尚未形成結論的中間狀態訊息可以不重複時間戳；但同一回合最後交付給使用者的完整工程回覆應附上。

一般原則：

- 預設使用 `Asia/Taipei`；若使用者／project 明確指定其他時區，改用該時區並清楚標示。
- 使用絕對日期時間，不使用「剛剛」、「今天」等相對描述作唯一 freshness marker。
- 時間戳代表**這份 ChatGPT 回覆產生的時間**，不是 commit time、Codex report time、device time、server event time 或 validation evidence time。
- 時間戳不取代 repository HEAD、commit SHA、diff、validation evidence、TASKS state 或其他 canonical evidence。
- 若 execution surface 無法取得可信的目前時間，不得猜測；使用 `回覆時間：UNAVAILABLE`。

Codex 自己的 reporting language / timestamp 由 `CODEX_EXECUTION.md` 維護；ChatGPT 不用把自己的回覆時間戳塞進 Codex Prompt body，除非 task contract 本身需要。

## Repository／寫入邊界 routing

ChatGPT 的 Current Write Target Repository、Conversation-scoped Repository Write Lock、一般 project 只直接寫 root `TASKS.md` 的邊界、TASKS lifecycle、Git／permission 與 cross-repository mutation 規則，以 `REPOSITORY_EXECUTION.md` 為唯一主要 authority。

本檔只保留操作原則：

- repository access / connector capability 不等於 conversation write authority；
- 先確認 current writable repository，再判斷該 repository 內實際允許寫什麼；
- 非 current write target repository 可以 read/search/review/compare/取得 evidence／產生 Prompt，但不得由本聊天室直接 mutation；
- ChatGPT 產生 Codex Prompt 不等於 ChatGPT 自己取得 source/docs 等 path 的 direct-write authority。

## TASKS Admission／直接交付判斷

完整 TASKS admission threshold、persistent EMPTY mode 與 lifecycle 以 `REPOSITORY_EXECUTION.md` 為 authority；ChatGPT 在產生 execution handoff 前只做 routing decision。

**產生 Codex Prompt 不代表一定要建立 `TASKS.md`。**

通常可以直接使用 **Direct Short Prompt** 的情況：

- 一次性 maintenance；
- 修改位置與內容／root cause 已知；
- scope 小、風險低；
- 完成後沒有 material tracking value；
- 不實質影響 behavior、architecture、protocol、security、hardware、persistence、runtime state 或重要 validation state。

通常應 admission 到 `TASKS.md` 的情況：

- 需要後續追蹤；
- Blocked / Deferred / Pending-validation；
- 多 Stage／checkpoint；
- 有 dependency / trigger；
- root cause 尚未確認；
- 可能接續 implementation；
- 具有 material project / validation effect；
- 若不保存便容易遺漏。

一旦工作已進 `TASKS.md` 且存在可執行 canonical Stage，後續對使用者產生的 Codex launch 預設改用 **TASKS Short-launch**；不要再把 Stage 內容改寫成另一份完整 Prompt。

## Codex Prompt 模式選擇（Prompt Mode Selection）

ChatGPT 產生 Codex Prompt 前，選**最低充分 Prompt mode**：

`TASKS Short-launch → Direct Short Prompt → Standalone Full Prompt`

### TASKS Short-launch

當最新 `TASKS.md` 已保存可執行 Stage，且 Codex 能依 repository governance 取得該 Stage 與 authority：

- Prompt 是 **execution pointer，不是 specification container**；
- 以 exact Stage name 指向 `TASKS.md`；
- 要求依 repository governance 完成必要 preflight／safe sync、重讀最新 `AGENTS.md` / `TASKS.md`、只執行該 Stage、依 queue action 收尾；
- Stage 已保存的 evidence、approved contract、allowed/forbidden scope、validation matrix、STOP/escalation、model/reasoning/context 與歷史 timeline **不在 launch Prompt 重寫**；
- 只有 launch 時新出現、且 canonical authority 尚未保存的 material information 才補最低充分內容；若需要後續追蹤，優先更新 canonical Stage。

Short-launch 預設維持**一個短段落**。若開始出現多段 evidence、長 bullets、完整 validation checklist 或大量 frozen behavior，先做 duplication check。

核心原則：**Reference, don’t repeat。**

### Direct Short Prompt

沒有 canonical Stage、且工作符合 Direct Short Prompt 條件時，使用 bounded direct Prompt。只放完成這一次工作真正需要的 target、scope、必要 evidence、validation 與 STOP boundary；不要把完整 project history 帶進 Prompt。

若 Direct Short Prompt 開始需要大量 historical evidence、dependent scope、長 validation matrix、future trigger 或跨 Stage state，通常代表應先 admission 到 TASKS，再改用 Short-launch。

### Standalone Full Prompt

只有下列情況才使用較完整的 self-contained Prompt：

- Codex 無法存取完成任務所需的 repository authority；
- repository 尚無可靠 `AGENTS.md` / `TASKS.md` routing 或 canonical Stage；
- 跨系統／跨 repository handoff 必須攜帶對方無法取得的 material context；
- 使用者明確要求 standalone / full Prompt；
- 其他 evidence 證明只用 reference 會使 execution contract 不完整或不安全。

Standalone 仍只帶最低充分 Context；self-contained 不等於貼上完整聊天、全部 Playbook 或所有歷史 evidence。

## Prompt 建議設定與固定資訊

Codex 的 model / reasoning / Context / Agent / execution-mode 成本規則由 `CODEX_EXECUTION.md` 維護。ChatGPT 依該 authority 選最低充分建議，不自行發明新的模型分工。

對 **Direct Short Prompt** 與 **Standalone Full Prompt**，Prompt 前段至少包含：

- 目標 Repository：`owner/repo`
- 預期 Branch
- 推薦模型：Luna / Terra / Sol
- 推理強度：Low / Medium / High
- 推薦理由：1～3 句
- 是否值得先用較便宜模型前置蒐證：是／否 + 理由
- 必要時補 Context 建議
- 必要時補 Execution mode

模型與 Reasoning 仍由使用者在 Codex UI 選擇；Prompt 只提供建議與 execution contract。

對 **TASKS Short-launch**，若 referenced Stage 已保存 model / reasoning / Context / execution mode 等建議，不要為固定欄位再次展開。可以在可複製 Prompt 外用一行精簡顯示 UI 選擇建議；若 Stage 沒保存必要設定，才補最低充分資訊。

## Repository routing 完成後的 Prompt 產生

若目標 repository 最新 `AGENTS.md` 已明確：

- 宣告本手冊為 common baseline；
- 保存最低必要 Playbook routing；
- 說明 project-specific authority / exception；
- 要求依 Task 只讀必要章節而非完整掃描；

ChatGPT 後續產生 Prompt 時，不再列出整套 Playbook 文件或複製 common policy 全文。

通常只需要：

1. 要求 Codex 先讀最新 project `AGENTS.md`；
2. 依 routing 與本次 Task 取得最低必要 authority；
3. 沒有其他 repository authority 保存 task contract 時，才補最低充分 task-specific evidence / scope / validation / STOP condition。

只有 routing 尚未建立／不完整、有 ambiguity、Task 需要特殊章節或必須 freeze 某個 common contract 時，才額外點名具體 Playbook 文件。

## 可直接複製的 Codex Prompt（Copy-ready Prompt Delivery）

只要 ChatGPT 提供的內容是讓使用者**直接貼給 Codex 執行**的 Prompt，不論 TASKS Short-launch、Direct Short Prompt 或 Standalone Full Prompt，都必須提供單一、完整、可一次複製的 copy surface。

一般原則：

- **One Prompt = One Copy Surface。** 同一份 Prompt 的全部 Codex-required instructions 集中在**一個 fenced code block** 內。
- 不得要求使用者自行框選散落在一般 prose、blockquote、列表或多個 code block 的片段後再拼接。
- Prompt 外可以放給使用者看的模型／Reasoning／Context 建議、簡短說明或注意事項；但 Codex 必須收到才能正確執行的內容全部留在同一 code block。
- Direct Short Prompt / Standalone Full Prompt 可以在 block 內使用 headings、bullets 或 Markdown，但單一 Prompt 不拆成「前半段／後半段」。
- Prompt 本身需要 triple-backtick example 時，使用更長外層 fence或其他能維持單一 copy surface 的安全表示法。
- 若真的需要兩個以上互斥 alternative Prompts，每個 alternative 可各自一個完整 code block；單一 alternative 不得碎片化。
- 即使 client 不顯示 copy button，也保持單一 fenced code block，至少只需選取一個連續區塊。

Copy-ready 是 delivery contract，不是增加 Prompt 長度的理由。

核心原則：**給 Codex 的可執行 Prompt 應能一次完整複製；使用者不負責重新組裝 ChatGPT 的 Prompt 碎片。**

## Prompt lean／長度診斷

Prompt 長度不是品質指標。若完整 specification 已存在 repository，ChatGPT 的工作是產生**最短安全 launch pointer**，不是再寫一份 specification。

對 TASKS Short-launch：

- 只保留 target repository / branch、exact Stage pointer、必要 bootstrap/routing 與 completion/queue action；
- Stage 已有的 evidence、scope、forbidden scope、validation、STOP condition 不重寫；
- 明顯超過一個短段落時，先檢查是否 duplicate `TASKS.md` / AGENTS / spec / validation authority。

對沒有 canonical Stage 的 Direct / Standalone Prompt，才保存最低充分：

- target repo / branch；
- task；
- repository authority 無法取得的 task-specific evidence；
- allowed / forbidden scope；
- targeted validation；
- success / STOP condition。

若內容持續膨脹，先判斷是否應 admission 到 TASKS，而不是以 self-contained 為理由無限制擴寫。

## Coverage-sensitive planning

有些工作單一修改不難，但要求完整覆蓋很多分散 surface；例如 UI consistency、文件一致性、migration cleanup、重複 API surface 或 verifier coverage。這類工作優先縮小 Stage / checkpoint，而不是因工作很長先升級模型。

推薦：

`Bounded inventory → Checkpoint A → Focused implementation → Targeted validation → STOP → Independent coverage reconciliation → Next checkpoint → Final closure reconciliation`

一般原則：

- implementation session 不同時負責大範圍 discovery、修改與 completeness judgment；
- 每個 checkpoint 只處理一個 coherent surface / invariant / operator flow；
- checkpoint 完成後先做 completion evidence，再決定下一個；
- model / reasoning 按各 checkpoint 的實際內在難度與風險選擇；
- 不為形式拆開共享同一 transaction、root cause、state transition 或必須原子完成的工作。

核心區分：**Model difficulty ≠ Coverage difficulty。**

## Codex 結果 reconciliation

ChatGPT 收到 Codex／coding agent execution result 後，若結果宣稱 GitHub repository tracked-file 修改、commit、push、TASKS bookkeeping、branch/HEAD 或其他可由 GitHub canonical evidence 驗證的 remote repository state change，在接受 completion、更新後續判斷或產生下一 Stage 前，必須依 `DEBUG_VALIDATION.md` 的 **Completion Evidence Guard / GitHub Remote Read-back** 取得最低充分 remote evidence。

一般原則：

- Codex report 是 claim，不是 GitHub authority；
- verification 是 read-only，不會因另一 repository 不是 Current Write Target 就被禁止；
- local-only / unpushed change 不能被 GitHub read-back 升格成 remote confirmed；
- Codex report 與 current GitHub state 不一致時，STOP completion acceptance，依 remote evidence 重建 current state；
- GitHub connector / network / permission 無法使用時，標記 `REMOTE COMPLETION EVIDENCE UNAVAILABLE`，不得把 mutation claim 升格成 confirmed completion。

詳細 evidence scope、SHA／diff／TASKS／docs read-back 判斷由 `DEBUG_VALIDATION.md` 維護，本檔不複製完整 validation policy。

## Scope expansion 與下一步

ChatGPT 在 analysis、review 或 Codex result 中發現 out-of-scope 問題時，依 `REPOSITORY_EXECUTION.md` 的 TASKS admission / technical-debt trigger 判斷是否 Deferred、建立新 item 或只保留 analysis；不得因「順便看到」就把目前 Stage 自動擴張。

同理，發現另一 repository 也需要同步時，只做 read-only analysis / handoff；是否切換 Current Write Target 依 `REPOSITORY_EXECUTION.md` 的 Conversation-scoped Repository Write Lock。

核心原則：**ChatGPT 負責把問題變成最低充分、可追蹤、可執行的 handoff；Codex 負責在授權 Stage 內執行，GitHub／canonical evidence 負責證明結果。**
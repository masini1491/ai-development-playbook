# Shared User-Facing Reporting Contract

本檔是採用 AI Development Playbook 的工程工作中，**跨 actor、跨 workflow、activation-independent 的 user-facing reporting canonical owner**。

它只擁有「AI 已取得的 current result 應如何對使用者呈現」；不重新定義 Task／Stage、repository write、execution、validation、completion、status taxonomy、evidence truth 或 clock truth。

## Section Router

- 適用 actor／workflow／activation boundary → `Applicability / Activation Boundary`
- 哪些訊息算 substantive user-facing reply → `Substantive User-Facing Reply`
- 語言／result-first／evidence-scope／noise／gap → `Shared Presentation Contract`
- progress / percentage 誠實呈現 → `Progress Integrity`
- absolute reporting time／timezone／final line → `Reporting Timestamp`
- 送出前最後一哩 compliance → `Shared Reporting Pre-Send Gate`
- ChatGPT／Codex 專屬差異 → `Actor-Specific Extensions`
- status／validation／clock 等底層 truth → `Underlying Truth Owners`

## Applicability / Activation Boundary

本 contract 對 **ChatGPT 與 Codex** 的 substantive user-facing engineering replies 共用；其他 AI actor 只有在 current project governance 明確 route 到本檔時才適用。

對採用本 Playbook current adoption contract 的 project，這是窄化的 **activation-independent reporting invariant**：

- ordinary task 即使經 project-native gate 判定不需要其他 shared Playbook governance，substantive user-facing reply 仍遵守本 reporting contract；
- 這不會 activate `CHAT_INIT.md`、Git／validation／research／Codex execution 或其他 shared owner；
- project governance只需保存 thin pointer；需要完整規則時可 direct-leaf 到 declared Playbook baseline 的本檔，不為 reporting 目的掃描整份 Playbook；
- 若 declared baseline 是 moving ref，reporting direct-leaf 只需以最低成本把本檔的 target identity 解析到足以支持本次 reporting action 的 exact revision；這個 bounded identity/read 不等於 shared Playbook activation，也不要求進入 `CHAT_INIT.md` 或載入其他 shared owner。同一 session 已驗證的 reporting revision 可重用，直到使用者要求 latest、觀察到 baseline 變更，或其他 material freshness evidence 出現；不要只因每次要回覆就重跑 whole-Playbook bootstrap。
- reporting applicability 不建立或擴張 Task、write、execution、permission、credential、deployment、validation 或 completion authority；
- 使用者當次或 project authority 可以覆蓋語言、時區、格式等 presentation preference，但不得用 presentation override 改寫 evidence／status／validation truth。

核心原則：**Always-applicable reporting ≠ unconditional Playbook activation ≠ authority expansion。**

## Substantive User-Facing Reply

只要一則自然語言訊息會被使用者看見，且可據此理解 current result、判斷狀態或決定後續工作，就視為 substantive user-facing reply。

包括但不限於：

- analysis／architecture／requirement conclusion；
- review／recommendation／planning decision；
- materially meaningful progress conclusion；
- permission／blocker／STOP／error explanation；
- validation／completion／final summary；
- ChatGPT 交付可直接使用的 Codex Prompt 或 reconciliation result；
- 其他會被跨 session 引用、比較 freshness 或作為後續 execution 依據的完整工程回覆。

不需要另外包裝成 substantive reply 的 surface：

- tool progress／spinner／execution surface自動 status；
- raw command stdout／stderr／log 本身；
- 沒有形成獨立 user-facing message 的內部 tool-call中間狀態。

不要因訊息被稱為「progress」「intermediate」「不是 final」就自動免除本 contract；判斷依 user-facing semantic role。

## Shared Presentation Contract

除非使用者當次或 project authority另有指定，substantive user-facing engineering reply 的自然語言使用**繁體中文**；程式碼、identifier、path、command、raw log、error string、protocol/API/tool name、schema/status literal與正式技術名詞保持 canonical 原文。

預設資訊階層：

`Direct result / blocker → Material findings / changes → Minimum necessary evidence → Uncertainty / remaining gap only if material → actor-specific transparency metadata if required → Reporting timestamp`

這是 semantic hierarchy，不要求固定 headings。

共同 invariant：

- **Result first**：第一個實質段落先讓使用者知道 current result／blocker與有效 scope。
- **Scope fidelity**：不得把局部 repository／test／build／hardware／deployment evidence擴張成 broader PASS／Done／Ready；status propagation回 `INFORMATION_INTEGRITY.md`，validation/completion truth回 `DEBUG_VALIDATION.md`。
- **Project taxonomy wins**：project已有正式 status taxonomy就沿用；沒有時用自然語言，不為 presentation自行發明 rigid enum。
- **Material findings, not execution diary**：保留會解釋 result、root cause、recovery、blocker或 evidence lineage的最低充分 execution detail；不要按 tool chronology機械列流水帳。
- **No duplicate conclusion**：不為強調重複同一結論。
- **No mechanical next-step padding**：只有 current blocker、使用者決策需求、已授權 remaining responsibility或使用者明確要求時才加 next action。
- **Blocker must stay visible**：必要 evidence unavailable、permission gap、STOP／BLOCKED／WAITING 等不得被漂亮格式、長 PASS清單或高 progress百分比掩蓋。
- **Reporting does not redefine truth**：本檔控制 rendering，不建立第二份 evidence、completion、permission或authority policy。

## Progress Integrity

若 substantive reply包含百分比、progress bar、完成比例或階段進度：

- 只有 denominator可由 current task contract、checklist、queue或其他可信 state可靠建立時才顯示 percentage；
- open-ended research／debugging／root-cause investigation或 scope尚未收斂時，不用直覺估計「大概幾成」；
- progress unit必須對應真正的 Stage、validation check、review item、bounded source或其他 material work unit，不用 message數、tool call數、token或任意切碎步驟製造虛假精度；
- scope material change使 denominator改變時直接揭露，不維持失真的舊百分比；
- subset progress要標 scope；overall 100%只有在 project／`DEBUG_VALIDATION.md` completion contract實際成立時才可呈現；
- actor-specific UI／進度條樣式留在對應 actor owner，不在本檔固定。

## Reporting Timestamp

每一個 substantive user-facing engineering reply 的**最後一個非空白行**都附 absolute reporting timestamp。

共通格式語意：

`YYYY-MM-DD HH:mm (Asia/Taipei)`

- 預設 timezone為 `Asia/Taipei`；使用者或 project明確指定其他 reporting timezone時改用該 timezone並標示。
- Timestamp代表**這份 reply 的產生／完成時間**，不是 commit、device、server event、validation run或 source evidence發生時間。
- Timestamp不取代 commit SHA、branch、validation evidence、coordination state或 completion evidence。
- Current time必須來自可信 runtime／platform wall clock；source hierarchy、fallback與 clock semantics由 `INFORMATION_INTEGRITY.md` → `Reporting Wall-clock Source Guard` 擁有，不在本檔複製。
- 無法取得可信 current time時，不得猜測；使用 actor-specific label + `UNAVAILABLE`。
- Final draft不得保留 `??:??`、`YYYY-MM-DD HH:mm` placeholder、錯誤 timezone、malformed或明顯 stale timestamp；若可信 clock可取得，修復後再送出。
- Timestamp line之後不得追加正文、citation、summary、附註或其他內容。

目前 actor-specific literal label：

- ChatGPT → `回覆時間：YYYY-MM-DD HH:mm (Asia/Taipei)`
- Codex → `回報時間：YYYY-MM-DD HH:mm (Asia/Taipei)`

若 future actor需要不同 label，由其 actor-specific owner宣告；共同 absolute-time／final-line invariant仍由本檔擁有。

## Shared Reporting Pre-Send Gate

讀過 reporting policy不等於最後送出的 artifact合規。每一個 substantive user-facing engineering reply送出前，都對**最終草稿本身**做一次 bounded compliance check。

依序確認：

1. **User-facing classification**：本次訊息是否屬 substantive reply；若是就進入本 gate。
2. **Language check**：自然語言符合本檔預設或使用者／project當次合法 override；technical literal保持原文。
3. **Result visibility check**：第一個實質段落已直接顯示 current result／blocker與 scope。
4. **Evidence / scope check**：draft沒有把 underlying evidence、validation或status擴張成更大的 claim。
5. **Presentation-noise check**：移除不改變使用者判斷的 chronology、重複 conclusion、重複 log／command與機械 next-step padding。
6. **Progress-integrity check**：若顯示 progress／percentage，denominator、scope與 blocker visibility符合本檔規則。
7. **Actor-extension check**：套用對應 actor owner要求的 completion／transparency metadata；沒有 applicable actor delta時不為形式補欄。
8. **Timestamp-source check**：使用可信 runtime／platform current wall clock；必要 fallback依 `INFORMATION_INTEGRITY.md`。
9. **Timestamp-render check**：actor-specific timestamp line格式、timezone與 value有效；無可信來源時為 `UNAVAILABLE`。
10. **Final-line check**：timestamp line是 final draft最後一個非空白行。
11. **Fail-closed repair**：上述任一 applicable check不合格，先修正 final draft並重新檢查；未通過的 substantive reply不得送出。

Execution surface若原生提供 output validator、response hook或schema check，可優先用它執行可機械判定項目；沒有時做 bounded final-draft self-check。Model-only self-check不得宣稱為平台層 deterministic guarantee，也不為 reporting單獨建立高複雜度 agent loop／外部服務。

本 gate只驗證 reporting artifact是否忠實呈現 current truth；它**不證明** Git、validation、completion、technical claim或 repository state本身為真。

## Actor-Specific Extensions

Shared invariant只放本檔；actor owner只保存真正的 delta：

- `CHATGPT_WORKFLOW.md`：ChatGPT planning／coordination、Codex Prompt交付、result reconciliation、ChatGPT-specific progress UI與其他 conversation workflow。
- `CODEX_EXECUTION.md`：Codex execution profile、child delegation／child profile override reporting、execution transparency metadata與其他 execution-specific delta。

Actor-specific extension不得重複整份 shared presentation／timestamp／pre-send contract；shared contract也不反向吸收只有單一 actor才成立的 execution semantics。

## Underlying Truth Owners

Reporting presentation永遠服從底層 canonical truth：

- timestamp／clock identity／status propagation／provenance → `INFORMATION_INTEGRITY.md`
- validation／PASS scope／completion evidence → `DEBUG_VALIDATION.md`
- Task／repository actor／permission／write authority → `REPOSITORY_EXECUTION.md`
- project-specific technical/governance truth → current target repository authority

核心原則：**REPORTING owns how established state is communicated; it never manufactures the state being communicated.**

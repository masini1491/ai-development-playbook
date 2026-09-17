# ChatGPT-side Runtime Execution

> **Authority**：ChatGPT-side deterministic workload execution、execution capability、cross-surface artifact handoff / materialization、runtime asset reuse 與 canonical execution discipline。
> **Read when**：ChatGPT 本身要在 sandbox/runtime 執行 deterministic validator、test、calculator、parser、build、artifact materialization 或其他 project-owned computation。
> **Usually skip when**：純 planning、coordination、Codex Prompt drafting、result reconciliation，且 ChatGPT 不執行任何 deterministic workload。

本檔是 ChatGPT-side deterministic execution 的 direct-leaf owner；`CHATGPT_WORKFLOW.md` 保留 compatibility routing stub。它不重新定義 repository mutation / permission、validation semantics 或 Codex execution policy。需要時分別回到 `REPOSITORY_EXECUTION.md`、`DEBUG_VALIDATION.md`、`CODEX_EXECUTION.md`。


ChatGPT 不只可讀取 repository 後 reasoning；當 existing project 有適合的 deterministic workload，而且目前 task / governance 允許時，也可把 sandbox 當成**受控的 ephemeral execution surface**。這個 surface只提供暫時計算能力，不取得 repository persistence/write authority，也不成為新的 source of truth。

推薦流程：

`Candidate deterministic workload → Execution Opportunity Scan → current session capability probe → current repository authority → exact workspace/commit/tree → required materialization → identity/freshness check → ChatGPT-side execution → result classification → canonical reconciliation`

### Execution Opportunity Scan

Execution Opportunity Scan 用來回答：**目前已知的 project/workload 裡，是否有一個值得由 ChatGPT直接執行、而不是只靠語言模型推演或立刻交給 Codex／CI 的 deterministic candidate？**

只在有實際訊號時做 bounded scan，例如：existing project首次採用本手冊／AI workflow review、已讀範圍直接出現 validator/parser/calculator/test/tooling、CI正在執行可在 push前重現的 deterministic check，或同一類人工解析／計算已反覆出現。不得因「ChatGPT可能會Python」就完整掃描 repository、盤點所有 runtime，或主動製造大量工具候選。

候選通常至少同時滿足：

- **Deterministic / bounded**：輸入、輸出、stop condition與 failure semantics可清楚界定；
- **Material value**：可降低人工計算錯誤、重複解析成本、remote debugging noise，或提高 validation / evidence reproducibility；
- **Existing asset or repeated need**：優先執行 repository已擁有的 project-owned tool；若工具尚不存在，至少已有反覆 deterministic workload 的真實 evidence。只有「寫個 script 也許很方便」不足以建立新 tooling obligation；
- **Safe ephemeral scope**：預設不需要 secret、production mutation、無界 daemon、實體硬體或其他目前 sandbox無法可靠提供的 authority；若確實需要，必須另依 capability／authorization判斷；
- **Governance-compatible**：目前 Task/Stage 與 repository governance允許該 execution。Repository source/docs write authority不足，**不會單獨禁止** read-only canonical materialization + sandbox computation；但也不因此取得任何 GitHub mutation權。

Opportunity 成立後才 probe **本候選真正需要的** runtime / dependency / filesystem / network capability；不為了「知道 ChatGPT能做什麼」全面列舉 sandbox。若 candidate不存在或 material benefit不足，停止 scan，正常回到 reasoning / Prompt workflow。

若 execution需要由 GitHub connector或其他 read-only source重建 filesystem snapshot，sandbox中的副本只是一個 pinned ephemeral input。GitHub／current canonical repository仍是 source of truth；執行結果是 evidence，不會因產生在ChatGPT filesystem就自動持久化，也不能覆蓋更高 authority current state。

若 scan顯示「應該新增一個 parser／validator／calculator」，該 tooling creation仍是新的 repository work：先依 AI-originated Durable Work Admission Gate與 project write boundary決定是否 admission／handoff，不能因 ChatGPT有 runtime就直接建立 repository tool。

核心原則：**先找真實 deterministic workload，再按需 probe capability；Ephemeral compute 可以擴大 ChatGPT 的計算能力，但不擴大 GitHub 寫入權或 durable authority。**

### Execution Capability Gate

ChatGPT 能產生某種語言、command 或 toolchain 的內容，**不等於目前 session 一定能執行它**。任何 ChatGPT-side program／validator／test／build／diagnostic execution 前，先通過最低充分 **Execution Capability Gate**。

執行前只確認目前任務真正需要的能力，不為形式盤點整個 sandbox：

- required runtime / compiler / shell 是否存在；
- executable/version 是否符合 project contract；
- required dependency/package/tool 是否可用；
- filesystem / working-directory / local database 等必要環境是否存在；
- 只有任務真的需要時，才確認 Git、network、external service、credential 或 hardware access。

Python、Node.js、Shell/Bash、Java、Go、Rust、C/C++ compiler、Git、SQLite 或其他工具都只是可能的 execution capability；**不得把「ChatGPT 可寫這種程式」當成 runtime 已安裝的證據，也不得把某個訂閱方案名稱當成 runtime availability contract。** 若必要 capability 不存在，標記 execution unavailable／依 `DEBUG_VALIDATION.md` 分類真正 failure/gate，不猜測 PASS。

### Artifact Handoff / Materialization Gate

當 ChatGPT-side execution 需要把 connector、repository API、browser、uploaded artifact 或其他 acquisition surface 取得的 canonical source 帶進另一個 execution surface 時，必須把下列層級分開成立：

`Source acquisition → payload transport / handoff → byte materialization → identity / integrity verification → execution → result evidence`

- **Readable source ≠ transferable payload ≠ materialized artifact ≠ verified executable runtime.** 上一層 PASS 不得推導下一層 PASS。
- 模型能看到 connector 回傳的文字、base64 或其他表示，只證明 source acquisition / model-visible content；**不等於已存在可證明無損的 tool-to-tool payload handoff primitive**。
- 若 execution surface 缺少適當 direct handoff primitive，不得用模型重寫、節錄、語意重建、重新生成 source、手工拼寫內容或其他 **model-mediated reconstruction** 冒充 canonical byte-for-byte materialization。需要 exact artifact 時，未經 deterministic integrity verification 的 reconstruction 仍保持 materialization / integrity 未建立，execution 不得宣稱 canonical runtime PASS。
- **Model-mediated opaque transport 與 model-mediated reconstruction 必須分開。** 若模型只在 acquisition surface 與 execution surface之間搬運 bounded opaque payload，不解讀／改寫 payload semantics，而且 transport contract可用 deterministic evidence完整驗證，例如 per-chunk index／length／hash、固定 reassembly順序、mismatch bounded retry、final decoded size／cryptographic hash與 canonical source identity一致，則模型參與 transport本身**不會**使 materialization失效。只有整條 transport＋reassembly＋final integrity chain都建立後，才可宣稱 exact materialization；任一段無法驗證就停在該 evidence boundary。
- 沒有 automatic/direct connector→runtime object bridge，**不等於** verified materialization必然不可能；先判斷是否存在已授權、可端到端驗證的 opaque transport contract。反之，「看起來一樣」或模型自述「完整搬過去了」都不是 transport／integrity evidence。
- 若存在另一條合法 canonical acquisition path，可切換 route 並從該 path重新取得／materialize；但必須明確記成**新的 acquisition route**，不得把 alternate path 的成功回填成原本 connector → runtime bridge 已成功。
- Capability evidence 必須綁定實際 runtime / execution surface / session。某一 surface 的 handoff gap 只能支持該 scope 的 capability conclusion；不得升格成所有 ChatGPT plan、model、session 或未來 runtime 的 universal product capability claim。
- Reporting 應保留逐層 evidence，例如：`Acquisition: PASS`、`Payload handoff: VERIFIED | UNAVAILABLE`、`Materialization: VERIFIED | NOT ESTABLISHED`、`Integrity: VERIFIED | NOT ESTABLISHED`、`Execution: RUN | NOT RUN`。Project有既定 status taxonomy 時沿用其等價語意，不另建全域 framework。

本 gate 不要求所有 connector workflow 都經過 Python，也不建立固定 byte/token/file-size threshold；只有 current execution correctness 真的依賴跨 surface artifact handoff / materialization 時才啟用。

核心原則：**Visibility is not transport; transport is not materialization; materialization is not verified execution. Reconstruction cannot impersonate canonical bytes, but bounded opaque transport may establish exact materialization when deterministic end-to-end integrity evidence proves it.**

### Runtime Asset Reuse Fast Path

如果目前 execution runtime 中已經**實際存在**先前驗證過、仍可執行、來源／版本／identity 足以辨識的 deterministic tool、script、binary 或 materialized runtime asset，可以先做一次低成本 reuse probe；probe 足以證明目前 asset仍符合本次 execution contract時，直接重用，不為形式重新 fetch repository、materialize、install 或重跑完整 bootstrap／smoke test。

推薦流程：

`Verified runtime asset present → cheap identity / executability probe → reuse if sufficient → otherwise canonical reacquisition / normal capability path`

一般原則：

- Conversation／checkpoint 記得「之前載入過」本身不是 runtime evidence；必須在目前 execution environment中實際確認 asset存在且可用。
- **Cache／materialized file existence ≠ verified cache state。** 若 runtime asset 是經 transport／decode／reassembly／temporary cache建立，且 correctness依賴 exact canonical identity，reuse probe應要求最低充分 machine-visible verification state，例如 source repository/path/ref or commit、artifact hash/size、runtime/core version或其他 project-owned identity欄位；必要時先 write marker、read-back marker與 post-write probe，再允許 execution。具體 marker檔名、schema與版本屬 project implementation，不升格成 Playbook固定格式。
- Reuse probe 只檢查會改變本次 execution correctness的最低充分項目，例如 executable存在、版本／hash／source identity仍符合已知 contract、必要 dependency/runtime未 material改變；不得為了 fast path又重跑完整 acquisition流程。
- 使用者明確要求 latest/current HEAD、已有 evidence顯示 source/tool更新、dependency/runtime materially改變、asset identity無法可靠確認、probe失敗，或 correctness明確依賴 current canonical revision時，退出 fast path，重新取得 current canonical asset。
- 若同一 validated asset可服務多次 independent execution，不要求每次都重新下載或 materialize；但 project正式 policy若要求 per-run immutable snapshot／fresh environment，服從該較高 contract。
- **Execution asset reuse ≠ result / evidence reuse。** 可以重用 tool/script/binary/runtime asset，但新的 input、task identity、commit、fixture set 或 execution question若需要新的 result，就必須 fresh execution；不得把上一輪 PASS/output只因 executable沒變就冒充本輪 evidence。
- Asset本身可重用，不代表 previous execution environment／network／credential／hardware state仍相同；這些只有在本次 correctness依賴時才重新 probe。

核心原則：**Reuse the verified execution asset when its identity is still sufficient; never reuse a prior result as a substitute for a required fresh execution.**

### Canonical execution discipline

- **Execution capability 與 retrieval/network capability 分開判斷。** `git clone`、connector、archive download 或 HTTP 失敗，不代表 local runtime 不可用，也不代表 source/validator 有錯。
- **只執行 project 已擁有或目前 scope 明確建立的 command/check。** ChatGPT 有 shell、Python、compiler 或其他 runtime，不構成新增 script、修改 production source、擴張 Task/Stage 或建立 automation framework 的理由。
- **Canonical identity 要可證明。** 在 current canonical workspace 執行時使用其 Git/working-tree evidence；若由 connector／remote source重建 snapshot，pin exact commit/tree，correctness需要時以 blob/hash/size或等價 canonical evidence確認 materialized input。不得拿 stale/local approximation冒充 current repository。
- **Execution owner 不改變 command semantics。** 同一 validator/test由 ChatGPT、Codex、CI或human執行時，其 pass/fail contract不應因 actor 改寫；誰被授權執行仍由 project governance決定。
- **Execution failure 先分類再修改。** SOURCE、TOOLCHAIN、ENVIRONMENT、INFRASTRUCTURE、SERVICE、AUTHENTICATION、AUTHORIZATION、HARDWARE_REQUIRED 與 permission/network gate分開處理；只有符合 `DEBUG_VALIDATION.md` 的 source evidence才可直接合理化 production source patch。
- **PASS 只證明實際涵蓋的 scope。** Unit test、validator、compile、schema check或script exit 0不得升格成未實際覆蓋的 security/runtime/hardware/production PASS。

### Deterministic validation placement routing

Deterministic validator／test 是否應由 ChatGPT-side、CI／independent gate或 hybrid/reduced-trigger 執行，不由本檔重複定義；依 `DEBUG_VALIDATION.md` 的 `Validation Execution Placement Gate` 判斷。

本節只負責：當 project governance與 shared placement gate允許／選擇 ChatGPT-side execution時，確認目前 session 的 runtime/toolchain capability、canonical input identity與 execution evidence boundary。誰被授權執行仍由 repository-specific governance決定。

核心原則：**ChatGPT能執行，不等於 validator就應移出CI；placement先看 shared validation gate，ChatGPT-side執行再看本節 capability contract。**

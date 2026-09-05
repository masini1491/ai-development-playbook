# Project Research Bootstrap Mode

> **Authority**：pre-implementation project bootstrap 階段的 ChatGPT research / synthesis direct-write boundary、mode activation / exit、以及與 Codex implementation handoff 的責任切換。
>
> **Read when**：新 repository／新產品開案仍以 ChatGPT 蒐集 reference、比較方案、形成 requirements / architecture premise 為主，Codex／coding agent 尚未開始 implementation，且只允許 `/TASKS.md` 會造成不必要的 handoff / bookkeeping 成本。
>
> 本檔不改變一般 implementation repository 的 source write boundary；未啟用本 mode 時，仍依 `REPOSITORY_EXECUTION.md` 的一般 ChatGPT／Codex Repository Write Boundary。

## 啟用條件（Activation Gate）

`research-bootstrap` 是 **project 明確 opt-in mode**，不是因 repository 很新、Codex 尚未出現、或 ChatGPT 已能寫 GitHub 就自動成立。

至少需要：

1. 使用者明確指定唯一 `Current Write Target Repository`；
2. 使用者明確表示目前處於 pre-implementation research / bootstrap 階段，或明確要求啟用等價模式；
3. project governance 明確保存目前 mode 與 ChatGPT 可寫的 research paths；
4. 若 repository 已存在更高權威 governance，必須與它相容，不得用本 mode 覆蓋既有禁止事項。

推薦 declaration：

```text
ChatGPT Project Mode: research-bootstrap
ChatGPT Research Write Allowlist:
- /TASKS.md
- /research/**
- /docs/architecture/**
```

Path 只是示例；project 可選 `references/**`、`docs/research/**`、`PROJECT_BOOTSTRAP.md` 或其他等價 surface。**只有明確列出的 path 可直接寫。**

## Bootstrap Governance Initialization Exception

為避免「新 repo 尚未有 Codex，卻必須先叫 Codex 只為建立 allowlist」的循環，本手冊提供一個非常窄的初始化例外：

- repository 尚未存在 project governance，或只有不衝突的空／template governance；
- 使用者當次明確要求 ChatGPT 初始化該 repository 的 `research-bootstrap` mode；
- ChatGPT 只可建立／補入**最低充分 bootstrap governance**：Playbook baseline、`ChatGPT Project Mode: research-bootstrap`、明確 Research Write Allowlist、project-specific authority precedence、no self-expansion boundary；
- 這個例外不授權 ChatGPT 建立 source implementation policy、CI policy、deployment policy、security credential policy 或其他與啟動 research mode 無關的治理內容；
- repository 已有 material governance 時，不得用此例外重寫／取代它。需要改變 existing governance 時，回到該 repository 的既有 governance mutation contract。

核心原則：**Bootstrap initializer 解決「誰先建立研究寫入邊界」；它不是一般 governance write permission。**

## Reuse-First Research Gate

在 `research-bootstrap` 階段，**成熟能力的 reuse discovery 必須發生在 architecture freeze 與 Codex handoff 之前**；不能等到 coding agent 已準備實作某個功能時，才臨時檢查是否已有成熟做法。

推薦流程：

`Requirement discovery → Domain decomposition → Bounded reuse discovery → Candidate evaluation → Reuse / Adapt / Gap map → Architecture freeze → Codex handoff`

一般原則：

- 先把需求拆成具有獨立工程責任的 capability / domain，例如資料來源、storage/query、scheduler、notification、protocol adapter、UI component、backtest、import/export、device integration；不要只用產品名稱做一個寬泛搜尋。
- 對**成熟領域、material engineering cost、或合理存在 upstream reuse 可能性**的 capability，ChatGPT 主動做 bounded discovery；不等使用者逐項提醒「先找 GitHub」。
- Discovery 優先檢查官方 implementation / SDK / sample、成熟 GitHub repository、library / driver、reference architecture、interoperability / test evidence；詳細研究與 license/provenance 規則仍服從 `RESEARCH_ARCHITECTURE.md` 的 `避免重造輪子關卡`、`漸進式外部研究`、`來源與授權`。
- 找到候選後，不只回答「有沒有」，還要判斷可直接 `REUSE`、需要 `ADAPT`、僅 `REFERENCE-ONLY`、或必須自行補 `GAP`。既有 `Reference Adoption State` 可用時直接沿用，不另造平行狀態系統。
- Architecture freeze 前，對會 materially 影響 implementation scope 的 capability，應形成最低充分 **Reuse / Adapt / Gap Map**；不用追求固定表格格式，但至少能回答：候選來源、採用判斷、可重用 boundary、project-specific gap、Codex 不應重造的 layer。
- 若一份高權威候選已足以支持 reuse/adapt decision，就停止擴張；不要求每個 capability 固定搜尋多個 repo。若未發現成熟候選，也要把「已做 bounded discovery、目前 gap 仍存在」與搜尋範圍／限制說清楚，避免 Codex 把 search miss 當成世界上不存在 upstream。
- 簡單、低成本、明顯 project-specific 的局部能力，不為形式強制建立 reuse ceremony；本 gate 的目的是真正避免高成本重造，不是把所有 helper 都變成研究專案。

建議 handoff 摘要可採：

```text
Capability: <name>
Candidate: <repo / library / SDK / none after bounded discovery>
Decision: REUSE | ADAPT | GAP | REFERENCE-ONLY
Reusable boundary: <what upstream already solves>
Project-specific gap: <what remains ours>
Codex invention boundary: <layers Codex must not rebuild without new evidence>
```

核心原則：**成熟能力先證明哪些可以 reuse / adapt，再設計我們真正缺的 gap；Codex 的工作邊界應由 gap 決定，而不是由空白畫布決定。**

## Research Write Allowlist

Mode 啟用後，ChatGPT 可在 project 明確 allowlist 內直接建立／更新 pre-implementation knowledge artifact，例如：

- external reference / source dossier / provenance；
- research synthesis、technology comparison、unknown / revisit trigger；
- requirement discovery / constraint baseline；
- 尚未進 implementation 的 architecture / protocol / integration decision；
- Reuse / Adapt / Gap Map 或等價 reuse synthesis；
- project bootstrap dossier；
- 一般既有 coordination / Cold / evidence surfaces（只有 project 同時明確列入時）。

這些 artifact 可以成為 canonical project documentation，但 authority 仍由 project governance / owner 定義；ChatGPT 寫得進去不代表其內容自動正確，也不代表取得 implementation authority。

### 不允許的 direct-write

即使在 `research-bootstrap` mode，下列項目預設仍不得由 ChatGPT直接修改，除非 project 有另一個更高層明確且合法的特殊例外：

- production / application / firmware source；
- executable tests / test harness；
- build scripts、tooling、package / dependency / lock files；
- workflow / CI / release / deployment；
- generated artifact / vendor dependency；
- runtime secrets、credential、private raw evidence；
- 已進 implementation lifecycle、由 coding agent / maintainer 擁有的 implementation artifact。

`Research write authority ≠ source implementation authority ≠ execution authority。`

## Canonicalization Discipline

Research 階段允許 ChatGPT 直接形成 durable project knowledge，因此要避免把 temporary notes、raw search dump 和 canonical conclusion 混成同一層：

`Source / provenance → bounded research synthesis → confirmed premise / decision → canonical owner`

- raw source dump 預設不是 current architecture authority；
- confirmed durable fact 應依 `INFORMATION_INTEGRITY.md` 的 Durable Confirmed Fact Ownership Guard 進合理 factual owner；
- derived comparison / synthesis 不得冒充 source authority；
- architecture decision 尚未 freeze 時，清楚標記 provisional / open question / revisit trigger；
- 已 canonicalized 的 conclusion 不要在 TASKS / evidence / research note 再維護第二份完整 mutable truth。

## Exit / Handoff Gate

`research-bootstrap` 不是永久寬鬆模式。當第一個 implementation Stage 準備交給 Codex／coding agent，或 project 已開始穩定 source mutation lifecycle 時，應做 bounded handoff：

`research-bootstrap → reconcile current research / architecture → close material Reuse / Adapt / Gap decisions → freeze minimum implementation premise → admit Hot implementation work → switch to implementation boundary → Codex executes`

退出前至少確認：

- implementation 所需的 current requirements / architecture premise 有唯一可找到的 canonical owner；
- 對 material mature capabilities 已完成最低充分 reuse discovery，Reuse / Adapt / Gap 結論可被 Codex 找到；
- unresolved research 有明確 status / trigger，不冒充已決定事項；
- first implementation task 的 goal / completion / exclusions / evidence pointers 足夠，且明確指出 upstream reusable boundary 與 project-specific implementation gap；
- project governance 將 `ChatGPT Project Mode` 切回一般 implementation mode或等價 contract，並收斂不再需要的 Research Write Allowlist；
- 退出後 ChatGPT 不因曾在 bootstrap 期間可寫 architecture/research，就繼續推導對 source、tests 或一般 docs 的永久 write authority。

若 implementation 已開始但後續又需要新研究，ChatGPT仍可 read/research；是否重新取得 research path direct-write 依 current project governance，不因歷史 mode 自動恢復。

## Cost / Workflow Rationale

本 mode 的目的不是讓 ChatGPT 取代 Codex，而是消除開案早期低價值的搬運：當 ChatGPT 本來就是 reference retrieval、analysis、synthesis 的主要 actor 時，不需要為了把同一份 research conclusion 寫進 repository，再額外建立 Codex handoff、重載 Context、產生 commit-only 工作。

核心分工：

- **Research/bootstrap phase**：ChatGPT = research + synthesis + bounded canonical documentation maintainer；
- **Implementation phase**：ChatGPT = planning / research / review；Codex／coding agent = authorized repository implementation maintainer。

核心原則：**Write authority follows project phase and explicit governance；研究階段減少無意義 handoff，實作階段恢復清楚 actor boundary。**

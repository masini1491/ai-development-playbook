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

## Post-Adoption Context Closure Gate

Reuse / Adapt 能降低初次 implementation cost，但若後續每個 Task 都重新讀大量 upstream source、examples、tests 與 internal architecture，節省的成本會被長期 Context 消耗追回來。因此，material upstream integration 在完成 gap implementation 與最低充分 validation 後，應建立**薄型 local integration contract**，把成熟 upstream internals 從 ordinary default Context 降為 condition-triggered detail。

推薦 lifecycle：

`Reuse discovery → adopt / adapt → implement project gap → validate integration → freeze thin local integration contract → ordinary work reads contract + project-owned code → expand upstream internals only on trigger`

Thin contract 不要求建立固定檔名或額外 ceremony；可放在 project 已存在的 architecture / integration / reference owner。只需保存後續 task 真正需要的最低充分資訊，例如：

- upstream identity / pinned version、revision 或 dependency range；
- upstream 擁有並已解決的 responsibility / layer；
- project 自己擁有的 adapter、policy、extension、gap；
- stable integration points / public API / contract；
- project-specific assumptions、known limitation、license / provenance pointer；
- **Codex invention boundary**：哪些 upstream-solved layer 不得無新 evidence 重寫；
- **Context expansion trigger**：何時才需要深入 upstream internals，例如 upstream bug evidence、version upgrade、contract conflict、security/failure analysis、integration test 指向 upstream boundary。

一般原則：

- **不要為了「變成自己的」而重寫成熟 upstream。** Integration 已正常工作時，implementation cleanup / rewrite 必須有 correctness、performance、resource、security、maintainability 或其他 material evidence；不能只為降低表面 dependency 或 source ownership 感而把 upstream重新實作一次。
- Ordinary feature / maintenance task 若只碰 project-owned gap，預設先讀 thin integration contract 與直接相關 project code；不因 upstream repository 可讀就全文載入。
- Thin contract 是 routing / ownership / integration boundary，不是把 upstream README / source 再複製一份。需要 upstream 詳情時沿 provenance / stable pointer bounded-read 原始 authority。
- Dependency upgrade、upstream API change 或 evidence 顯示 current thin contract 不再成立時，重新做 bounded upstream reconciliation，更新 contract 後再收斂 Context。
- 若 upstream 很小、API 本來就極薄，或每次工作確實必須理解其 internals，則不為形式建立額外 wrapper 文件；本 gate 的判斷標準是**是否實際降低後續 end-to-end retrieval / reasoning cost而不犧牲 correctness**。

核心原則：**Reuse saves implementation cost only if adopted upstream does not become permanent default Context. Preserve a thin local contract; make upstream internals condition-triggered.**

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
- 對預計採用的 material upstream，已決定 integration completion 後 thin local contract 的 owner / destination，讓 implementation 完成後可以收斂成 Post-Adoption Context Closure，而不是永久把 upstream internals 放在 default Context；
- project governance 將 `ChatGPT Project Mode` 切回一般 implementation mode或等價 contract，並收斂不再需要的 Research Write Allowlist；
- 退出後 ChatGPT 不因曾在 bootstrap 期間可寫 architecture/research，就繼續推導對 source、tests 或一般 docs 的永久 write authority。

若 implementation 已開始但後續又需要新研究，ChatGPT仍可 read/research；是否重新取得 research path direct-write 依 current project governance，不因歷史 mode 自動恢復。

## Cost / Workflow Rationale

本 mode 的目的不是讓 ChatGPT 取代 Codex，而是消除開案早期低價值的搬運：當 ChatGPT 本來就是 reference retrieval、analysis、synthesis 的主要 actor 時，不需要為了把同一份 research conclusion 寫進 repository，再額外建立 Codex handoff、重載 Context、產生 commit-only 工作。

Reuse 的成本收益也不只看第一次少寫多少 code；若 adopted upstream 之後每個 Codex task 都被迫重讀大量 internals，長期 Context / reasoning cost 仍可能很高。完成 integration 後應把 ordinary work 收斂到 thin local contract + project-owned gap，只有 trigger 成立才展開 upstream internals。

核心分工：

- **Research/bootstrap phase**：ChatGPT = research + synthesis + bounded canonical documentation maintainer；
- **Implementation phase**：ChatGPT = planning / research / review；Codex／coding agent = authorized repository implementation maintainer。

核心原則：**Write authority follows project phase and explicit governance；研究階段減少無意義 handoff，實作階段恢復清楚 actor boundary；Reuse 之後再收斂 default Context，才真正降低 end-to-end AI development cost。**

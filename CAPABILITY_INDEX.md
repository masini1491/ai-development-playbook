# AI Capability Discovery Index

> **Purpose**：這是給 AI／agent／automated reviewer 做 whole-repository capability discovery 的**薄索引（thin discovery surface）**，用來降低「能力已存在，但因沒有讀到正確 canonical owner 而被誤判為缺少」的風險。
>
> **Authority boundary**：本檔不是新的 policy／state／validation authority，不複製完整規則，也不證明某 capability 的 runtime maturity。每個 capability 的正式語意仍由下列 canonical owner／tool／test 決定。

## 使用方式

若任務是 capability inventory、competitive comparison、productization gap analysis、architecture maturity review，或準備宣稱「這個 repository 缺少／沒有／尚未實作 X」：

1. 先用本索引找可能的 canonical owner／implementation／test；machine consumer 也可用 `PLAYBOOK_INDEX.json` 做 stable-ID / path discovery。
2. 依 `CHAT_INIT.md` 與 `AI_CONTEXT.md` 的 `Absence Claim Coverage Gate` 做 bounded read／existence check。
3. 在**最終回答前**，把草稿中的 negative／gap claims（例如「缺少 X」、「尚未支援 Y」、「沒有 Z」）逐條重新 reconcile；若找到任何一層 positive evidence，應描述真正 maturity layer，例如「已有 contract/spec，尚無 automated harness」，不要把 implementation gap 誤寫成 capability absence。
4. 若 repository search／connector coverage 不完整，使用 `NOT FOUND IN CHECKED SCOPE`／等價 evidence-bounded wording，不得升格成 whole-repository absence。

`PLAYBOOK_INDEX.json` 與本檔都是 discovery surface；machine manifest 只保存 stable routing metadata，不取代 canonical Markdown owner。

核心原則：**Discovery index 幫你找到能力；canonical owner 決定能力；final negative-claim reconciliation 防止在 synthesis 階段重新漏掉能力。**

## Capability pointers

| Capability | Canonical owner / implementation pointer | Maturity / discovery note |
| --- | --- | --- |
| New-session bootstrap / task routing | `CHAT_INIT.md` | Minimal bootstrap、task router、direct-leaf bypass、cross-owner review trigger。 |
| Repository read acquisition / recovery | `CHAT_INIT.md` → `Repository Read Acquisition / Recovery Gate` | Connector-first、public canonical fallback、minimum user-supplied section、fail-closed blocked state；read fallback不擴張 authority或write scope。 |
| Research-bootstrap project mode / write boundary / handoff | `PROJECT_BOOTSTRAP.md` → `啟用條件（Activation Gate）`、`Research Write Allowlist`、`Exit / Handoff Gate` | Opt-in pre-implementation research mode；不擴張一般 implementation source write authority。 |
| Reuse-first research / post-adoption context closure | `PROJECT_BOOTSTRAP.md` → `Reuse-First Research Gate`、`Post-Adoption Context Closure Gate` | Architecture freeze 前先做 bounded reuse discovery；採用後以 thin local integration contract 降低長期 upstream Context 成本。 |
| Stage-transition actor revalidation | `PROJECT_BOOTSTRAP.md` → `Stage-Transition Actor Revalidation Gate`；behavioral evidence：`DEBUG_VALIDATION.md` → `BEH-010`、`evals/runs/BEH-010-2026-09-07-formal-001.json` | **Contract + formal behavioral evidence 已存在**；actor choice依 current responsibility／mutation／capability／authority重新判定，不繼承上一 Stage。 |
| Machine-readable routing discovery | `PLAYBOOK_INDEX.json`；drift/path/section check：`tools/playbook_check.py` + tests | **Routing-only JSON manifest 已存在**；只保存 stable capability ID / owner / section / adapter pointer，不保存 current state。 |
| Thin activation adapters | `ACTIVATION_ADAPTERS.md` | **Manual thin activation adapter contract 已存在**；native marketplace installer／startup hook／generated per-tool command pack 尚未宣稱存在。 |
| ChatGPT Custom Instructions host adapter / health check | `ACTIVATION_ADAPTERS.md` → `ChatGPT — copy-ready custom instruction`、`ChatGPT Host Instruction Health Check`；distribution：`CHATGPT_CUSTOM_INSTRUCTIONS.txt`；behavioral evidence：`evals/runs/BEH-002-2026-09-08-chatgpt-custom-instructions-v1.1.json` | **Manual copy-ready user-level adapter + bounded fresh-chat diagnosis 已存在**；project adoption／baseline仍由 current project governance 決定，host setting 不建立 project authority。 |
| External workflow interoperability / compatibility profiles | `INTEROPERABILITY.md` | **Normative interoperability contract + bounded compatibility profiles 已存在**；只定義 Playbook-side authority／loading／evidence mapping，不宣稱 native installer、auto-detection或live cross-runtime conformance。 |
| Repository information architecture / durable project memory | `AI_CONTEXT.md` | Always-on／Hot／Cold／Evidence／Current canonical／Historical、retrieval cost、Context Cohesion、session-local verified reuse／selective invalidation、hot-path growth ratchet。 |
| Repository-level absence / capability review | `AI_CONTEXT.md` → `Absence Claim Coverage Gate` | 已有 normative coverage contract；不要把 search miss 當 absence proof。 |
| Evidence lineage / independence | `INFORMATION_INTEGRITY.md` → `Evidence Lineage / Independence Guard` | Source count 不等於 independent evidence count；fork／mirror／shared upstream lineage 不得膨脹 corroboration。 |
| Temporal semantics / clock identity | `INFORMATION_INTEGRITY.md` → `Temporal Semantics / Clock Identity Guard` | Event／observation／callback／publication／generation time分層；timestamp格式相同不代表時間語意相同。 |
| Negative observation / unknown semantics | `INFORMATION_INTEGRITY.md` → `Negative Observation / Unknown Semantics Guard` | `Not observed ≠ absent`；unknown可 operationally fail closed，但不得被轉成 fabricated fact/default。 |
| Scope-qualified status propagation | `INFORMATION_INTEGRITY.md` → `Scope-Qualified Status / Propagation Guard` | PASS／FAIL／MISMATCH／FROZEN 等只對其 semantic scope 成立；跨 dimension propagation 需明確 aggregation contract。 |
| Private-to-public generalization / mosaic risk | `INFORMATION_INTEGRITY.md` → `Private-to-Public Generalization / Mosaic Guard` | Private evidence可形成 public abstraction，但不自動成為 public provenance；需檢查跨 artifact reconstruction risk。 |
| Original-vs-retrospective evidence integrity | `INFORMATION_INTEGRITY.md` → `Original vs Retrospective Evidence Guard` | Later evidence可改 current truth，但不可把 hindsight回寫成較早 decision point 當時已知／已判斷。 |
| Session compaction / rehydration | `CHATGPT_WORKFLOW.md` → `Session Compaction / Rehydration Contract`；adapter：`SESSION_HANDOFF_TEMPLATE.md` | **Contract + thin handoff adapter 已存在**；自動判斷 compaction 時機／自動產生 handoff 的 runtime automation 尚未宣稱存在。 |
| Behavioral evaluation | `DEBUG_VALIDATION.md` → `Behavioral Evaluation MVP`；`evals/regression_matrix.json`；`tools/behavioral_eval.py` + tests | **Normative BEH contract、formal evidence、deterministic record validator與 bounded regression selector 已存在**；fresh-session model invocation／semantic grading仍是 external/manual layer。 |
| Deterministic validation / enforcement admission | `DEBUG_VALIDATION.md` → `Deterministic Enforcement Admission Gate`；`tools/playbook_check.py` + tests | Policy與 executable checker分層；checker只證明實際檢查的 invariant。 |
| Adoption Doctor | `AGENTS.md` → minimal validator contract；`tools/adoption_doctor.py` + `tests/test_adoption_doctor.py` | Read-only/report-only；支援 Local Path Mode 與 ChatGPT GitHub Snapshot Mode。 |
| GitHub connector-first snapshot acquisition | `AGENTS.md` → `ChatGPT GitHub Snapshot Mode` | Connector retrieval capability 與 local Python/network capability分層；connector可正常而 sandbox DNS受限。 |
| Conversation-scoped repository write authority | `REPOSITORY_EXECUTION.md` → `聊天室級 Repository 寫入鎖` | `Repository access ≠ conversation write authority`；同一聊天室只有一個 Current Write Target。 |
| Repository-declared actor topology / maintenance ownership | `REPOSITORY_EXECUTION.md` → `Repository Actor Topology / Maintenance Ownership`；behavioral scenario：`evals/BEH_019_SUPPLEMENTAL.md` | **Normative contract + regression scenario 已存在**；project governance決定誰可維護 source/docs/tests/tooling等責任，Playbook只提供 coordination-only conservative fallback，不把ChatGPT→Codex handoff固定成universal workflow。 |
| Permission / capability layering | `REPOSITORY_EXECUTION.md` → `授權與能力分層` | Task authorization、execution permission、credential capability取交集。 |
| Completion evidence / canonical read-back | `DEBUG_VALIDATION.md` → `完成證據關卡` | Agent自然語言 report不是 remote completion authority。 |
| AI-originated durable work admission | `CHATGPT_WORKFLOW.md` → `AI-originated Durable Work Admission Gate` | Observation／recommendation／admitted work分離；Cold candidate不自動取得 execution authority。 |
| Evidence lifecycle / real-world evidence | `DEBUG_VALIDATION.md`；embedded/hardware差異另見 `EMBEDDED_PROJECTS.md` | Software/test evidence不自動覆蓋 hardware／bench／production／user-observed evidence。 |
| Cost-aware execution | `CODEX_EXECUTION.md` | `Evidence → Context → Model → Reasoning → Agent → Validation`，依證據逐層 escalation。 |
| Prompt-authorized child model / reasoning routing | Prompt authorization：`CHATGPT_WORKFLOW.md` → `Prompt-authorized Child Profile Routing`；execution semantics：`CODEX_EXECUTION.md` → `Root / Child Profile Routing`、`Subagent / Delegation Gate`、`Parallel Multi-Agent Gate`、`Child Profile Routing 回報（Completion / Final）` | **Normative contract 已存在**；root profile維持 user-selected，合法 bounded child 可 serial delegation 並向上／向下 override model／reasoning；只有 concurrent workstreams 才另受 parallel gate 約束。Final report區分 requested/accepted override 與 independently observable effective profile；runtime capability／observability仍依 execution surface。 |
| ChatGPT bounded ephemeral execution | `CHATGPT_WORKFLOW.md` → `ChatGPT-side Runtime Execution` | Runtime capability不等於 repository mutation authority；只執行最低充分 deterministic workload。 |
| Research / architecture / ownership | `RESEARCH_ARCHITECTURE.md` | Research、state/lifecycle、target/capability、ownership與 external-service authority separation。 |

## Maturity wording guard

Capability review 至少區分下列層級；不是每項能力都必須同時擁有全部層級：

`policy / contract → executable implementation → deterministic tests / behavioral evidence → distribution / activation adapter`

因此建議寫：

- `Behavioral Evaluation MVP contract and regression-selection metadata exist; fresh-session invocation / semantic grading remain external.`
- `Session Compaction / Rehydration contract and handoff adapter exist; automatic compaction runtime not evidenced.`
- `Machine-readable routing manifest exists; native per-runtime activation hooks/installers not evidenced.`
- `External workflow interoperability contract exists; native integration and cross-runtime conformance remain separate maturity layers.`

避免寫成：

- `Behavioral evaluation does not exist.`
- `Session compaction is missing.`
- `Routing capability is absent.`
- `External workflow integration is absent.`

除非已完成與 claim scope 相稱的 bounded coverage，且 current canonical evidence確實支持 whole-repository absence。

# AI Capability Discovery Index

> **Purpose**：這是給 AI／reviewer／human 做 whole-repository capability discovery 的**薄索引（thin discovery surface）**，用來降低「能力已存在，但因沒有讀到正確 canonical owner 而被誤判為缺少」的風險。
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
| Machine-readable routing discovery | `PLAYBOOK_INDEX.json`；drift/path/section check：`tools/playbook_check.py` + tests | **Routing-only JSON manifest 已存在**；只保存 stable capability ID / owner / section / adapter pointer，不保存 current state。 |
| Thin activation adapters | `ACTIVATION_ADAPTERS.md` | **Manual thin activation adapter contract 已存在**；native marketplace installer／startup hook／generated per-tool command pack 尚未宣稱存在。 |
| Repository information architecture / durable project memory | `AI_CONTEXT.md` | Always-on／Hot／Cold／Evidence／Current canonical／Historical、retrieval cost、Context Cohesion。 |
| Repository-level absence / capability review | `AI_CONTEXT.md` → `Absence Claim Coverage Gate` | 已有 normative coverage contract；不要把 search miss 當 absence proof。 |
| Session compaction / rehydration | `CHATGPT_WORKFLOW.md` → `Session Compaction / Rehydration Contract`；adapter：`SESSION_HANDOFF_TEMPLATE.md` | **Contract + thin handoff adapter 已存在**；自動判斷 compaction 時機／自動產生 handoff 的 runtime automation 尚未宣稱存在。 |
| Behavioral evaluation | `DEBUG_VALIDATION.md` → `Behavioral Evaluation MVP`；`evals/regression_matrix.json`；`tools/behavioral_eval.py` + tests | **Normative BEH contract、formal evidence、deterministic record validator與 bounded regression selector 已存在**；fresh-session model invocation／semantic grading仍是 external/manual layer。 |
| Deterministic validation / enforcement admission | `DEBUG_VALIDATION.md` → `Deterministic Enforcement Admission Gate`；`tools/playbook_check.py` + tests | Policy與 executable checker分層；checker只證明實際檢查的 invariant。 |
| Adoption Doctor | `AGENTS.md` → minimal validator contract；`tools/adoption_doctor.py` + `tests/test_adoption_doctor.py` | Read-only/report-only；支援 Local Path Mode 與 ChatGPT GitHub Snapshot Mode。 |
| GitHub connector-first snapshot acquisition | `AGENTS.md` → `ChatGPT GitHub Snapshot Mode` | Connector retrieval capability 與 local Python/network capability分層；connector可正常而 sandbox DNS受限。 |
| Conversation-scoped repository write authority | `REPOSITORY_EXECUTION.md` → `聊天室級 Repository 寫入鎖` | `Repository access ≠ conversation write authority`；同一聊天室只有一個 Current Write Target。 |
| Permission / capability layering | `REPOSITORY_EXECUTION.md` → `授權與能力分層` | Task authorization、execution permission、credential capability取交集。 |
| Completion evidence / canonical read-back | `DEBUG_VALIDATION.md` → `完成證據關卡` | Agent自然語言 report不是 remote completion authority。 |
| AI-originated durable work admission | `CHATGPT_WORKFLOW.md` → `AI-originated Durable Work Admission Gate` | Observation／recommendation／admitted work分離；Cold candidate不自動取得 execution authority。 |
| Evidence lifecycle / real-world evidence | `DEBUG_VALIDATION.md`；embedded/hardware差異另見 `EMBEDDED_PROJECTS.md` | Software/test evidence不自動覆蓋 hardware／bench／production／user-observed evidence。 |
| Cost-aware execution | `CODEX_EXECUTION.md` | `Evidence → Context → Model → Reasoning → Agent → Validation`，依證據逐層 escalation。 |
| ChatGPT bounded ephemeral execution | `CHATGPT_WORKFLOW.md` → `ChatGPT-side Runtime Execution` | Runtime capability不等於 repository mutation authority；只執行最低充分 deterministic workload。 |
| Research / architecture / ownership | `RESEARCH_ARCHITECTURE.md` | Research、state/lifecycle、target/capability、ownership與 external-service authority separation。 |

## Maturity wording guard

Capability review 至少區分下列層級；不是每項能力都必須同時擁有全部層級：

`policy / contract → executable implementation → deterministic tests / behavioral evidence → distribution / activation adapter`

因此建議寫：

- `Behavioral Evaluation MVP contract and regression-selection metadata exist; fresh-session invocation / semantic grading remain external.`
- `Session Compaction / Rehydration contract and handoff adapter exist; automatic compaction runtime not evidenced.`
- `Machine-readable routing manifest exists; native per-runtime activation hooks/installers not evidenced.`

避免寫成：

- `Behavioral evaluation does not exist.`
- `Session compaction is missing.`
- `Routing capability is absent.`

除非已完成與 claim scope 相稱的 bounded coverage，且 current canonical evidence確實支持 whole-repository absence。

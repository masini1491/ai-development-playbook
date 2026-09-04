# Behavioral Evaluation Evidence

本目錄保存 `DEBUG_VALIDATION.md` → `Behavioral Evaluation MVP` 的 empirical run evidence；不複製 scenario 的 Expected／Forbidden policy，也不成為第二份 behavioral authority。

## Run record

每筆 JSON run record 至少保存：

- `scenario_id`
- `playbook_sha`：實際被測的 Playbook canonical SHA
- `run_time`
- `stimulus`
- `observed_actions`
- `response_reference`
- `classification`：`PASS` / `FAIL` / `INCONCLUSIVE`
- `classification_reason`
- `run_kind`：`formal` / `retrospective`

`formal` 表示 scenario contract 在被測 baseline 已正式成立；`retrospective` 表示既有 fresh-session evidence 是在 scenario 後來才 canonicalize 的情況下回溯分類。Retrospective record 必須另記 `scenario_contract_sha`，且不得與固定 baseline 的 formal cross-model regression 混為同一 evidence tier。

`agent`、`model`、`runtime`、`comparison_group` 等欄位只有在可可靠取得且會改善 reproducibility 時才保存；不知道就不要猜。

`response_reference` 應指向可追溯 evidence；若完整 response 因 conversation-local、privacy、授權或保存成本無法進 repository，必須明確說明限制，不得假裝 repository record 本身等於完整原始 transcript。

## Deterministic validation

`python tools/behavioral_eval.py evals/runs/*.json`

工具只驗證 run-record 結構、固定比較組輸入與 deterministic summary；它**不判斷 AI 語意是否真的符合 scenario**。Behavioral PASS / FAIL / INCONCLUSIVE 仍依 `DEBUG_VALIDATION.md` 的 canonical scenario contract 與實際 observable evidence 判定。

核心原則：**保存足以重現與比較的 behavioral evidence metadata，但不要把 empirical record、summary 或 validator 變成新的 policy authority。**

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

## Regression matrix

`evals/regression_matrix.json` 是 **selection-only metadata**：把常見 Playbook change class 對應到應優先重跑的既有 BEH scenario。它不複製 scenario 的 Expected／Forbidden，也不建立新的 behavioral authority。

```text
python tools/behavioral_eval.py --matrix evals/regression_matrix.json --change-class <change-class>
```

這個 command 只 deterministic 驗證 matrix 結構並輸出 scenario selection；**不會自動呼叫模型、建立 fresh session 或判斷語意 PASS**。實際 behavioral run 仍要固定 Playbook baseline／scenario input，讓 evaluator 獨立執行，再依 canonical scenario contract 分類。

需要完整 baseline 時使用 matrix 的 `full_baseline`；小型 change 優先跑與 change class 直接相關的 bounded subset，若 evidence 顯示 cross-cutting impact 再擴張。

## Deterministic validation

```text
python tools/behavioral_eval.py evals/runs/*.json
```

也可同時檢查 regression matrix：

```text
python tools/behavioral_eval.py --matrix evals/regression_matrix.json evals/runs/*.json
```

工具只驗證 run-record 結構、固定比較組輸入、regression-selection metadata 與 deterministic summary；它**不判斷 AI 語意是否真的符合 scenario**。Behavioral PASS / FAIL / INCONCLUSIVE 仍依 `DEBUG_VALIDATION.md` 的 canonical scenario contract 與實際 observable evidence 判定。

核心原則：**保存足以重現與比較的 behavioral evidence metadata；matrix 只幫忙選測試，不把 empirical record、summary、selector 或 validator 變成新的 policy authority。**

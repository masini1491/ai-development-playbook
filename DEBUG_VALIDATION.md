# 除錯／驗證方法論（Debug / Validation Methodology）

## 預設流程（Default flow）

`Evidence → Root Cause → Focused Patch → Targeted Validation`

不要先重構再找原因；不要用更大的模型或更多 Agent 取代 evidence。

## Root Cause 分類標籤（Root-cause labels）

只使用：

- `CONFIRMED ROOT CAUSE`
- `HIGH-CONFIDENCE LIKELY ROOT CAUSE`
- `INSUFFICIENT OBSERVABILITY`

只有前兩者可直接 patch。

`INSUFFICIENT OBSERVABILITY` 時先取得能區分原因的最小 diagnostics / evidence；無法在目前 scope 內安全取得就 STOP。

## 執行失敗分類（Operational failure taxonomy）

真正 execution/operational failure 分類：

- `SOURCE`
- `TOOLCHAIN`
- `ENVIRONMENT`
- `INFRASTRUCTURE`
- `SERVICE`
- `HARDWARE_REQUIRED`

可由使用者授權解除的 permission gate 在解除前不算真正 operational failure；先依 `REPOSITORY_EXECUTION.md` 的 Permission-Gated Operation 處理。

只有 `SOURCE` evidence 可直接成為繼續修改 production source 的理由。

TOOLCHAIN / ENVIRONMENT / INFRASTRUCTURE / SERVICE / HARDWARE_REQUIRED 不得合理化 production source patch，也不是提高模型/Reasoning/Context/Multi-Agent 的理由。

## 重試紀律（Retry discipline）

同一**non-compile operational root cause** 預設最多自動 retry 1 次；第二次仍失敗時 STOP、分類並保存最小可重現 evidence。

Permission denial → request → approval → retry original operation 不算 operational retry。

Compile/source-fix loop 若 repository governance、正式 validation contract 或特定 Stage 有自己的 bounded 上限，服從該正式規則；不要用 non-compile cap 覆蓋它。

## 驗證階梯（Validation ladder）

由小到大：

1. static check
2. targeted verifier
3. targeted test
4. relevant build / compile
5. required matrix
6. full regression

只跑足以驗證目前 scope 的最低充分層級；repository formal merge gate 若明確要求更完整驗證則服從正式 gate。

## 驗證涵蓋完整性（Validation Coverage Integrity）

`exit 0` 不等於驗證真的涵蓋目標 implementation。

必須在有風險時證明 intended source/backend/runtime/feature 真正參與 compile/link/test，例如：
- sketch/layout 是否真的包含該 source
- conditional compile / feature flag 是否啟用
- CMake target 是否 link 到 intended backend
- mock/stub 是否意外取代 production path
- 正確 board/FQBN/target 是否被選中
- 正確 runtime/toolchain 是否被使用

因此 validation evidence 需要時應記錄：
- toolchain/version
- target/board/FQBN
- exact command
- tested commit SHA
- CI run

Local PASS 不等於 remote CI PASS；舊 commit PASS 不等於目前 HEAD PASS。

## Verifier Contract 生命週期（Verifier Contract Lifecycle）

Verifier / static checker / test harness 本身也是會隨 production architecture 演進的 contract；驗證失敗不自動代表 production source 有 bug。

當既有 verifier 在 refactor、lifecycle、symbol、region boundary、route、ownership 或正式 contract 更新後失敗時：

1. 先重跑最小失敗 verifier，記錄精確 failed check / expected invariant / target region。
2. 對照最新高權威 contract、current production source 與必要 validation evidence。
3. 只有 evidence 證明「production invariant 仍成立，但 verifier assertion / symbol / region / wording 已過期」時，才可做最小 verifier-only patch。
4. 不得為了讓 verifier 變綠而弱化 safety/security invariant、刪除 assertion、改 production source，或把真正 source bug 假裝成 stale test。
5. 若無法區分 verifier drift 與 production defect，標記 `INSUFFICIENT OBSERVABILITY` 並 STOP；必要時建立獨立 source/validation task。

因此：

> Failing verifier ≠ source bug；Passing verifier ≠ coverage complete。

Verifier 更新後仍應執行直接相關交叉檢查，避免修正一支 stale verifier 時破壞其他正式 validation contract。

## Evidence 等級（Evidence tiers）

依專案需要區分：
- Software PASS
- Compile PASS
- Static/Test PASS
- Bench PASS
- Hardware PASS
- Network PASS
- Production PASS

不得把低層 evidence 翻譯成高層 PASS。

硬體/協議 evidence 可使用：
- `CONFIRMED_UPSTREAM`
- `CONFIRMED_LOCAL`
- `INFERRED`
- `UNKNOWN`
- `HARDWARE_TEST_PENDING`

相似裝置或 upstream evidence 不得自動改寫成 local hardware confirmed。

## Evidence 取代生命週期（Evidence Supersession Lifecycle）

歷史 PASS 應保留可追溯性，但不得因仍存在於文件或 Git history 就自動視為 current evidence。

Validation / evidence record 可依需要標記：

- `CURRENT`
- `SUPERSEDED`
- `HISTORICAL`
- `REVALIDATION_REQUIRED`

下列 material change 應觸發「舊 evidence 是否仍有效」的判斷：

- target / board / FQBN / PHY 改變
- toolchain / runtime contract 改變
- architecture / protocol / security / persistence contract 改變
- runtime ownership / lifecycle / initialization order 改變
- hardware mapping / electrical assumption 改變
- validation backend / verifier scope 改變
- implementation path 被重構到可能影響原驗證涵蓋範圍

原 evidence 若只證明舊 contract 或舊 implementation，不得被新狀態繼承；應標成 `SUPERSEDED` / `HISTORICAL`，並把新狀態保持 `REVALIDATION_REQUIRED` 或對應 Pending。

文件可保留歷史測試事實，但 current summary 必須明確指出最新 superseding rule，避免舊 PASS 被誤讀成目前 PASS。

## 正確性優先於重構（Correctness before refactor）

發現 correctness bug 時優先：

1. root cause
2. focused correctness fix
3. targeted validation
4. behavior-preserving refactor（若仍有價值）
5. regression

不要預設把 bug fix、architecture redesign、cleanup、library extraction 打包成一次工作。

## 行為保持重構關卡（Behavior-Preserving Refactor Gate）

宣稱 behavior-preserving 的重構，應先建立可比較 baseline，而不是只在修改後看「有編譯過」。

推薦流程：

`Baseline → Freeze protected invariants → Bounded refactor → Targeted build/test → Compatibility comparison → Remaining cleanup stays Deferred`

開始前至少確認本次真正需要保護的 invariants，例如：

- public / wire protocol values、layout、CRC、retry、timeout
- API / route / command contract
- persistent schema / migration semantics
- state ownership / lifecycle
- GPIO / board / hardware mapping
- safety initialization / output inactive state
- resource/capacity/timing behavior（若屬正式 contract）

重構時：

- 只改完成本 Stage 所需的 ownership / file layout / naming / dependency direction；
- 若遇到需要 architecture redesign、behavior change、new abstraction 或 unrelated cleanup，STOP 或另建 task；
- 未完成的 deeper modularization / cleanup 必須保持 Deferred，不得在後續 feature task 裡順手完成。

驗證時優先比較 refactor 前後的 protected invariants；若 binary/resource usage 有變化但 behavior 預期不變，需記錄差異並判斷是否 material，不要只因數字不同就宣稱 regression，也不要完全忽略。

## 決策階段（Decision Stage）

若 implementation 前仍有高影響 architecture/security/state/persistence policy 未決：

`Evidence → Architecture/Policy Decision → Frozen invariants/contract → Implementation → Validation`

Decision-only Stage 不修改 production behavior。

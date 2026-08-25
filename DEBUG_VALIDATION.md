# Debug / Validation Methodology

## Default flow

`Evidence → Root Cause → Focused Patch → Targeted Validation`

不要先重構再找原因；不要用更大的模型或更多 Agent 取代 evidence。

## Root-cause labels

只使用：

- `CONFIRMED ROOT CAUSE`
- `HIGH-CONFIDENCE LIKELY ROOT CAUSE`
- `INSUFFICIENT OBSERVABILITY`

只有前兩者可直接 patch。

`INSUFFICIENT OBSERVABILITY` 時先取得能區分原因的最小 diagnostics / evidence；無法在目前 scope 內安全取得就 STOP。

## Operational failure taxonomy

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

## Retry discipline

同一**non-compile operational root cause** 預設最多自動 retry 1 次；第二次仍失敗時 STOP、分類並保存最小可重現 evidence。

Permission denial → request → approval → retry original operation 不算 operational retry。

Compile/source-fix loop 若 repository governance、正式 validation contract 或特定 Stage 有自己的 bounded 上限，服從該正式規則；不要用 non-compile cap 覆蓋它。

## Validation ladder

由小到大：

1. static check
2. targeted verifier
3. targeted test
4. relevant build / compile
5. required matrix
6. full regression

只跑足以驗證目前 scope 的最低充分層級；repository formal merge gate 若明確要求更完整驗證則服從正式 gate。

## Validation Coverage Integrity

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

## Evidence tiers

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

## Correctness before refactor

發現 correctness bug 時優先：

1. root cause
2. focused correctness fix
3. targeted validation
4. behavior-preserving refactor（若仍有價值）
5. regression

不要預設把 bug fix、architecture redesign、cleanup、library extraction 打包成一次工作。

## Decision Stage

若 implementation 前仍有高影響 architecture/security/state/persistence policy 未決：

`Evidence → Architecture/Policy Decision → Frozen invariants/contract → Implementation → Validation`

Decision-only Stage 不修改 production behavior。

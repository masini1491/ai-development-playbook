# 嵌入式／硬體專案方法論（Embedded / Hardware Project Methodology）

本檔只保存跨專案 embedded/hardware 方法，不保存任何特定產品的 GPIO、credential 或私密 protocol。

## 硬體事實（Hardware truth）

軟體分析、compile、simulation、相似型號 evidence 都不能自動宣稱真實硬體 PASS。

建議 evidence 狀態：
- `CONFIRMED_UPSTREAM`
- `CONFIRMED_LOCAL`
- `INFERRED`
- `UNKNOWN`
- `HARDWARE_TEST_PENDING`

只有真實 target/board/device evidence 才能提升 local hardware confidence。

## 軟體優先基礎（Software-first foundation）

硬體尚未到手或 runtime 尚未授權時，可先完成 hardware-independent 部分：
- protocol constants
- parser / serializer
- deterministic validation
- state model
- DTO / value types
- HAL / transport interfaces
- Fake / Mock
- host tests
- CI
- config schema
- compile-only adapter

但只能建立在可靠 upstream evidence 或已 freeze project contract 上；未知硬體行為必須保持 UNKNOWN/INFERRED/HARDWARE_TEST_PENDING。

## 首次接觸診斷 Harness（First-contact diagnostic harness）

首次接觸新硬體、網路服務或 protocol 時，優先考慮 isolated diagnostic harness / test consumer，而不是直接把未知行為塞進 production runtime。

Diagnostic harness 建議：
- default inert
- bounded
- read-only 優先
- one-shot / explicit action
- 不保存 secret
- 不做 destructive operation
- 不做 infinite retry
- 清楚輸出最小 evidence

真實 hardware/network execution 必須有明確授權。

## Board Profile／硬體抽象（Hardware abstraction）

不要讓 application/core 直接散落 raw GPIO。

一般 boundary：

`Concrete Board Profile → HardwareConfig → HAL / Platform Adapter → Portable Core`

Board Profile 保存 physical capability：
- pins
- exposed resources
- strapping / boot caveats
- USB/JTAG
- flash / partition constraints
- UART/I2C/SPI/controller availability
- electrical compatibility
- FQBN/target identity

Resource/Feature Profile 則描述啟用功能、buffers、logs 等；不要把它和 board name 綁死。

新 board 不得靠舊 board pin number/compile success 推定相容。

新增 target：

`evidence → board profile → resource mapping → compile → hardware validation`

Unsupported target 應 fail closed，而不是使用 placeholder GPIO。

## 依 Capability 選擇 Target（Capability-based target selection）

先從需求推 capability，再選 target；不要先買最強 MCU 再硬塞需求。

比較：
- RAM / flash
- radio / protocol support
- peripheral controllers
- exposed pins
- boot safety
- toolchain maturity
- official SDK / upstream examples
- long-term resource margin

Embedded target selection 同時遵守 `RESEARCH_ARCHITECTURE.md` 的 evidence-first minimum-target baseline：先找最低合理候選，再用證據排除不足者，不因「比較保險」預設較大 MCU／module。

### Bring-up Target ≠ Minimum Product Target

較高資源的 development board / module 可以被暫時選為 bring-up target，例如為了先建立 SDK、Matter、BLE、network、filesystem 或 framework 的 compile/runtime baseline；但必須明確標記為 `PROVISIONAL` / `BRING-UP ONLY` 或等價狀態。

Bring-up target 不得自動推導：

- minimum supported MCU/module
- product BOM requirement
- required flash / RAM / PSRAM
- required core count
- required radio/peripheral capability
- product-final board/pinout

要把較高資源 target freeze 成 minimum requirement，需要 current product requirements 或 resource/runtime evidence 支持；開發方便、toolchain 成熟、未證實的「未來可能需要」或單純安全 margin 不足以構成 freeze evidence。

反過來，要排除較低資源候選，也應說明實際不足：

- REQUIRED capability 根本不存在或官方 SDK 不支援；
- compile/link/partition 已超限；
- runtime heap/stack/resource headroom 不足；
- concurrent workload、latency、timing 或 reliability evidence 不可接受；
- 安全、OTA、persistence、radio/peripheral requirement 無法滿足；
- 其他可重現且與需求直接相關的 evidence。

若只是「可能不夠」，保持 candidate 並取得最低必要 evidence，不要先升級 target。

### Embedded Resource Evidence

對可能受 MCU 資源限制的專案，target freeze 前依需求收集最低充分 evidence：

1. **Capability evidence**：CPU/radio/peripheral/SDK support 是否滿足 REQUIRED feature。
2. **Compile/static resource evidence**：binary/IRAM/DRAM/flash/partition/link result，證明 selected feature set 能建置。
3. **Runtime resource evidence（需要時）**：heap、largest block、stack watermark、task count、buffer/queue usage、PSRAM dependency、fragmentation、commissioning/connection peak、OTA peak 或其他 project-relevant peak。
4. **Representative workload evidence（需要時）**：多 endpoint、多連線、network reconnect、security handshake、sensor/transport burst、Matter commissioning 等真實或代表性 load。
5. **Hardware/bench evidence**：只有真實 target board/device 才能升成 local hardware confidence。

不是每個專案都要完整量全部指標；只量足以回答「最低候選是否真的足夠」的項目。

若較低 target 已被 evidence 證明足夠，不得只為了多留未定義 headroom 自動升到更大 target；若較低 target evidence 顯示 margin 不合理，再升級到下一候選並保留排除理由。

## Persistent State 交易完整性（Persistent State Transaction Integrity）

對 security/identity/auth/routing/hardware behavior/credential/critical config 等重要 persistent state，避免多 key partial success。

推薦語意：

`write → exact readback → validate → commit/fail-safe/rollback → explicit result`

Identity change 必須處理依賴它的 stale state；必要時用 generation/transaction semantics。

Reusable helper 應在真實 consumer semantics 證明後再抽象。

## 收斂式／冪等式協調（Convergent / Idempotent Reconciliation）

對代表 desired state 的 registration、sync、scheduler、bridge exposure、subscription、binding、configuration apply 或其他 reconciliation operation，重複執行、retry、restart 或 reconnect 後應收斂到同一個 intended state；不得因相同輸入重複建立 device/entity/job/binding/subscription 或其他 logical resource。

一般原則：

- 使用 stable identity、canonical key、generation/version 或其他可重現 identity 判斷 existing state；不要只靠目前 session memory 推定「之前應該建立過」。
- Reconciliation 應能區分 create、update、already-satisfied、stale/obsolete 與 conflict；合法重跑不得默默變成 duplicate creation。
- 若 external platform / bridge / scheduler / broker 可能保留 stale state，reconnect 或 restart 後應先取得最低充分 current evidence，再 reconcile；不要無條件重新 enumerate／register 全部資源。
- Retry 只有在 operation semantics 已確認可安全重入時才可視為 idempotent；沒有證據時，不得因 API 名稱看起來像 `set` / `sync` / `register` 就假設重試無副作用。
- Validation 除了「這次操作成功」，需要時還應檢查 duplicate、stale reference、unexpected re-enumeration、orphan resource 與 intended mapping 是否維持唯一性。
- 若底層 operation 天生 non-idempotent，應建立 explicit deduplication / transaction / idempotency-key / state machine boundary，或把 retry 交給知道 operation ownership 的單一 owner；不要讓多個 layer 各自盲目重試。

核心原則：**同一 desired state 被重新套用，不應產生新的 logical state；reconciliation 的成功是收斂，不只是 command 回傳成功。**

## 生命週期狀態連續性（Lifecycle State Continuity）

若產品宣稱 restart、reboot、OTA、upgrade、migration、container/device replacement 或其他 lifecycle transition 不需要重新 commissioning／configuration，則 stable identity、persistent config、binding、automation reference、external integration mapping 與其他必要 state 應被視為明確的 continuity contract，而不是 incidental implementation detail。

推薦驗證思路：

`pre-state snapshot → lifecycle operation → startup/recovery → post-state reconciliation → continuity evidence`

一般原則：

- 先列出哪些 state 必須跨 lifecycle 保留、哪些可以合法重建、哪些應被清除；不要用「資料都還在」或「服務有起來」代替正式 continuity contract。
- Stable identity、device/entity mapping、binding、scene/automation reference、credential ownership、routing/config 與其他 external reference 若屬 REQUIRED continuity，upgrade/restart 後不得 silently regenerate 成不同 identity 或 duplicate resource。
- Local runtime healthy / boot PASS 不等於 external integration continuity PASS；若 correctness 依賴 Matter、Home Assistant、MQTT、cloud/backend 或其他外部 consumer，需取得最低充分的 post-lifecycle mapping / reachability / state evidence。
- Backup/restore、migration 或 replacement 若宣稱可保留設定，應驗證 restored state 的 schema/version compatibility、identity ownership 與 external reference continuity；成功 import file 不等於整體 continuity 成立。
- Lifecycle transition 若允許 intentionally reset identity / binding / commissioning state，應是明確 contract 與 operator-visible effect，不得由 upgrade/restart 意外觸發。
- 不要求每次小版更新都做完整 production migration test；依實際風險選代表性 continuity fixture / targeted integration validation，但高價值 external binding 不應只靠 compile/static evidence。

核心原則：**Lifecycle success 不只是「重新啟動成功」，而是所有宣稱應延續的 identity、binding 與 external reference 仍能被同一套 authority 正確辨識。**

## Runtime 可靠性（Runtime reliability）

Embedded runtime 優先：
- non-blocking state machine
- bounded timeout/retry
- rollover-safe timer
- bounded queue/log
- explicit ownership
- fixed/reused buffer（適用時）
- safety/lifeline priority 高於 telemetry/debug

不要用 infinite retry 或無限制動態結構掩蓋硬體不確定性。

## 本地／離線管理 UI（Self-contained offline management UI）

若 embedded product 的正式 contract 要求裝置在 local LAN、direct AP、first-setup、provisioning、recovery 或 Internet unavailable 狀態下仍可完成必要管理操作，則 human-facing UI 的核心功能與必要資源應盡量 self-contained。

一般原則：

- 核心設定、狀態、診斷與 recovery flow 不應依賴外部 CDN、remote font、cloud-hosted frontend asset 或必須連 Internet 才能載入的 runtime dependency。
- 是否允許外部資源由產品 contract 決定；cloud-first product 不因本規則被強迫成 offline-first。
- 若 local/offline operation 是正式 requirement，外部服務失效不得讓 operator 無法完成必要 setup、configuration、diagnostics 或 recovery。
- **Local-first / offline-capable 不等於 unauthenticated。** Local LAN、direct AP、physical proximity 或 Internet unavailable 只描述 connectivity / availability boundary；authentication、authorization、credential ownership 與 destructive/recovery protection 仍依正式 security contract 處理，不因改成本地操作就自動放寬。
- Embedded UI 仍遵守 `UI_UX.md` 的 Human-facing UI / Machine Contract Boundary；self-contained 只處理 availability/dependency boundary，不授權 UI 接管 machine/runtime ownership。
- 資源受限時，優先保留可操作性、可讀狀態、錯誤說明與必要安全流程，再考慮動畫、remote asset、heavy framework 或純裝飾性功能。

## 安全關鍵生命週期仲裁（Safety-Critical Lifecycle Arbitration）

當 embedded system 同時存在 physical output、door/lock/motor/relay、OTA、provisioning、Web、network maintenance、background telemetry 等 operation 時，不能只靠「non-blocking」就視為安全；需要明確定義 operation priority 與 lifecycle arbitration。

一般原則：

- safety-critical / physical-output owner 優先於 maintenance/background operation；
- OTA start/write/end、provisioning startup、network scan、blocking HTTP/TLS、reboot、factory-reset completion 等可能延遲或中斷 safety servicing 的 operation，應在 critical output/session active 時 defer、reject、abort 或等待安全點；
- 但 safety gate 本身不得阻止必要 lifeline，例如 transport polling、output timeout servicing、watchdog-safe state progression、必要 ACK/teardown；
- restart / reset / recovery 等 destructive lifecycle action 優先採 deferred safe owner：先完成 transaction，再在 critical activity 清除後執行；
- physical-presence recovery / one-shot authorization 若屬 security boundary，應與一般 network failure 自動 fallback 分開，不要因網路失聯就自動開放較弱的 recovery mode；
- gate/priority 必須有 bounded timeout / explicit failure result，不能形成永久 starvation。

設計時建議畫出至少三層 priority：

`Safety/Lifeline → Authorized Control/Transaction → Maintenance/Telemetry/UI`

具體產品可以有不同名稱，但 ownership 與被 gate / 不可被 gate 的 operation 必須可審查。

這類 arbitration 的 compile/static PASS 不代表 timing/hardware PASS；若涉及真實 relay、motor、lock、OTA/reboot timing，仍需 hardware/bench evidence。

## 硬體驗證（Hardware validation）

Validation 要區分：
- Compile PASS
- Static/Test PASS
- Bench PASS
- Hardware PASS
- Network PASS
- Production PASS

不同 board/FQBN/PHY/device 的 PASS 不互相自動繼承。

若 target-specific implementation 有可能被 build layout/conditional compile 排除，必須遵守 Validation Coverage Integrity，證明 intended backend 真正參與 compile/link/test。

## 部署／卸載（Deployment / offload）

原 MCU 資源不足時，不一定換更大的單板；比較：
- swap target
- companion MCU
- gateway
- MQTT/application bridge
- Pi/Linux

保持 domain ownership：offload layer 不得在沒有正式設計下接管 authorization、安全狀態或 credential owner。
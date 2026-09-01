# 嵌入式／硬體專案方法論（Embedded / Hardware Project Methodology）

本檔只保存跨專案 embedded/hardware 特有方法，不保存任何特定產品的 GPIO、credential 或私密 protocol。

一般 target selection、resource-aware deployment、persistent-state transaction、idempotent reconciliation、lifecycle continuity 與 ownership 原則由 `RESEARCH_ARCHITECTURE.md` 維護；一般 diagnostic harness、evidence tiers、supersession 與 validation lifecycle 由 `DEBUG_VALIDATION.md` 維護。本檔只補充 target/board/device、硬體資源、實體輸出、bench/hardware evidence 等 embedded-specific delta。

## 硬體證據與驗證（Hardware Evidence / Validation）

軟體分析、compile、simulation、相似型號 evidence 都不能自動宣稱真實硬體 PASS。

Evidence label 與 validation tier 以 `DEBUG_VALIDATION.md` 為唯一主要 authority。Embedded-specific 限制是：

- 只有真實 target/board/device evidence 才能提升 local hardware confidence；
- 不同 board、FQBN、PHY、module、electrical mapping 或實體 device 的 Hardware/Bench PASS 不互相自動繼承；
- upstream／相似裝置 evidence 可以降低未知，但不能改寫成 `CONFIRMED_LOCAL`；
- hardware evidence 尚未取得時，保留 `HARDWARE_TEST_PENDING`／對應 Pending 狀態，不用 compile PASS 補推；
- 若 target-specific implementation 可能被 build layout / conditional compile 排除，必須依 Validation Coverage Integrity 證明 intended backend 真正參與 compile/link/test；
- compile/static PASS 不得冒充 electrical、timing、radio、sensor、actuator 或其他 physical hardware PASS。

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

首次接觸新硬體時若需要 isolated diagnostic harness / test consumer，依 `DEBUG_VALIDATION.md` 的 First-contact Diagnostic Harness 處理；真實 hardware execution 仍需符合目前 Task/Stage authorization 與 hardware evidence boundary。

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

## Embedded Resource Evidence

一般 Target Selection、Development/Bring-up Target 與 Minimum Product Target 分離、以及 Resource-aware deployment 由 `RESEARCH_ARCHITECTURE.md` 維護。Embedded 專案在 freeze target 前，依需求補充最低充分 resource evidence：

1. **Capability evidence**：CPU/radio/peripheral/SDK support 是否滿足 REQUIRED feature。
2. **Compile/static resource evidence**：binary/IRAM/DRAM/flash/partition/link result，證明 selected feature set 能建置。
3. **Runtime resource evidence（需要時）**：heap、largest block、stack watermark、task count、buffer/queue usage、PSRAM dependency、fragmentation、commissioning/connection peak、OTA peak 或其他 project-relevant peak。
4. **Representative workload evidence（需要時）**：多 endpoint、多連線、network reconnect、security handshake、sensor/transport burst、Matter commissioning 等真實或代表性 load。
5. **Hardware/bench evidence**：只有真實 target board/device 才能升成 local hardware confidence。

不是每個專案都要完整量全部指標；只量足以回答「最低候選是否真的足夠」的項目。

若較低 target 已被 evidence 證明足夠，不得只為多留未定義 headroom 自動升到更大 target；若 resource/runtime evidence 顯示 margin 不合理，再依 `RESEARCH_ARCHITECTURE.md` 的 Target Selection 排除候選或評估下一 topology。

## Embedded State／Lifecycle 補充

一般 state transaction、reconciliation 與 lifecycle continuity contract 見 `RESEARCH_ARCHITECTURE.md`。Embedded system 額外注意：

- persistent identity/config 若與 board identity、partition、NVS/flash layout 或 hardware binding 有關，upgrade/migration/replacement 必須把這些 physical assumptions 納入 continuity evidence；
- physical output、relay/motor/lock、radio commissioning、sensor calibration 或 device binding 的 continuity 不能只靠資料檔存在／boot 成功宣稱成立；需要對應 target/device 的最低充分 bench/hardware evidence；
- retry/reconcile 若會重送 physical command、重新配對硬體或改變 actuator state，不能只依一般 API idempotency 假設安全，必須確認實體 side effect semantics。

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

若 MCU resource evidence 顯示目前 target 不足，是否 swap target、使用 companion MCU、gateway 或其他 offload topology，改由 `RESEARCH_ARCHITECTURE.md` 的 Resource-aware deployment 決定；本檔不維護第二份 deployment policy。
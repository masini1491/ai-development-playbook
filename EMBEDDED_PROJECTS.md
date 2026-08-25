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

## Persistent State 交易完整性（Persistent State Transaction Integrity）

對 security/identity/auth/routing/hardware behavior/credential/critical config 等重要 persistent state，避免多 key partial success。

推薦語意：

`write → exact readback → validate → commit/fail-safe/rollback → explicit result`

Identity change 必須處理依賴它的 stale state；必要時用 generation/transaction semantics。

Reusable helper 應在真實 consumer semantics 證明後再抽象。

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

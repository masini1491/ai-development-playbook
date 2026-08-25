# Research / Architecture Methodology

## Research-first principle

> 先降低不確定性，再降低模型成本。

新專案或成熟技術整合，優先：

requirements → platform class → target family → external research → local reference synthesis → technology stack → architecture/policy freeze → implementation → validation

不要一開始就讓 coding agent 自行發明成熟協議、driver 或 framework。

## Anti-Reinvent-Wheel Gate

第一次實作成熟 protocol / hardware / SDK / integration 前，檢查：

- 是否有官方 implementation / SDK / sample
- 是否有成熟 GitHub implementation
- 是否已有 library / driver
- 是否有 test vectors / interoperability evidence
- 哪些 layer 已被 upstream 解決
- license / provenance 是否允許 reuse
- 真正需要自行實作的 gap 有多大

常見 trigger：NFC、HCE、APDU、BLE、CAN、ISO-TP、UDS、Matter、MQTT、Home Assistant、GPS/NMEA、fingerprint、Modbus、RS485、Zigbee、Thread、TLS、OTA、常見 sensor/SDK。

## Local reference knowledge base

若研究量開始變大，將外部 evidence 收斂成 repository-local knowledge：

- `references/README`：routing
- synthesis：project-level conclusion / unknown / revisit trigger
- topics：problem-oriented notes
- sources：upstream dossiers / provenance

後續 coding agent 優先讀 local synthesis，而不是每次重新外查。

## Provenance / license

研究不等於 copy permission。

Reference dossier 應能記錄：
- repository/source
- revision/commit
- license
- authority boundary
- relevant files/topics
- observations
- limitations
- do-not-assume
- reuse restriction

GPL / license 不明預設 `REFERENCE ONLY`，除非專案另有正式 license decision。

不要以改名、逐行翻譯、mechanical port 假裝成獨立 implementation；也不要隨意宣稱 clean-room。

## Technology stack selection

不要因為「ESP32」或某語言習慣就預設 framework。

選 stack 時比較：
- 官方 SDK 支援
- upstream quality
- 已有可重用資產
- future capability
- hardware capability
- host testability
- integration cost
- total engineering risk
- Codex invention/rewrite gap

不同 domain 不需要為了美觀硬統一 framework；更重要的是 contract/boundary/state semantics 清楚。

## Target selection

建議分層：

`Platform Class → Target Family → Concrete Target`

選「最低充分 target + 合理成長空間」，不要預設最強 MCU/CPU。

## Capability model

`Product requirements → Features → Required capabilities → Target capabilities → Build-time resolution`

Feature 可標：
- REQUIRED
- OPTIONAL
- FUTURE
- OUT_OF_SCOPE

Required capability 缺失應 fail closed；Optional capability 缺失可以是合法 unavailable，不應用假值掩蓋。

## Resource-aware deployment

新能力不一定要塞進原 MCU。

比較：
- current board
- target swap
- companion MCU
- MQTT/application gateway
- Pi/Linux host

選擇最低 total engineering/risk/cost 的 topology。

Domain owner 要清楚；gateway/composition layer 不應偷接管 credential、authorization、safety-critical ownership。

## Library-ready, not library-now

Library-ready ≠ 現在就拆 library。

先維持 dependency direction、host-testability、portable public API、explicit ownership；等真實 consumer/reuse need 出現後再 extract。

避免 speculative package/repo/semantic versioning/generalization。

## Independent domain repos / composition

Repository boundary 可依 domain ownership；deployment boundary 可依實際執行環境。

不同 domain repo 可透過 shared contract/composition layer 組合，但 domain repo 不應反向依賴 composition。

Same-process 優先 typed interface；跨裝置才適合使用 MQTT/transport contract。不要只為了解耦就在同一 process 自己對自己 MQTT。

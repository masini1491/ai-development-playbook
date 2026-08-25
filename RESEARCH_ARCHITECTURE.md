# 研究／架構方法論（Research / Architecture Methodology）

## 研究優先原則（Research-first principle）

> 先降低不確定性，再降低模型成本。

新專案或成熟技術整合，優先：

requirements → platform class → target family → external research → local reference synthesis → technology stack → architecture/policy freeze → implementation → validation

不要一開始就讓 coding agent 自行發明成熟協議、driver 或 framework。

## 避免重造輪子關卡（Anti-Reinvent-Wheel Gate）

第一次實作成熟 protocol / hardware / SDK / integration 前，檢查：

- 是否有官方 implementation / SDK / sample
- 是否有成熟 GitHub implementation
- 是否已有 library / driver
- 是否有 test vectors / interoperability evidence
- 哪些 layer 已被 upstream 解決
- license / provenance 是否允許 reuse
- 真正需要自行實作的 gap 有多大

常見 trigger：NFC、HCE、APDU、BLE、CAN、ISO-TP、UDS、Matter、MQTT、Home Assistant、GPS/NMEA、fingerprint、Modbus、RS485、Zigbee、Thread、TLS、OTA、常見 sensor/SDK。

## 本地 Reference 知識庫（Local reference knowledge base）

若研究量開始變大，將外部 evidence 收斂成 repository-local knowledge：

- `references/README`：routing
- synthesis：project-level conclusion / unknown / revisit trigger
- topics：problem-oriented notes
- sources：upstream dossiers / provenance

後續 coding agent 優先讀 local synthesis，而不是每次重新外查。

## 來源與授權（Provenance / license）

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

## 技術棧選擇（Technology stack selection）

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

## Target 選擇（Target selection）

建議分層：

`Platform Class → Target Family → Concrete Target`

選「最低充分 target + 合理成長空間」，不要預設最強 MCU/CPU。

## Capability 模型（Capability model）

`Product requirements → Features → Required capabilities → Target capabilities → Build-time resolution`

Feature 可標：
- REQUIRED
- OPTIONAL
- FUTURE
- OUT_OF_SCOPE

Required capability 缺失應 fail closed；Optional capability 缺失可以是合法 unavailable，不應用假值掩蓋。

## 資源感知部署（Resource-aware deployment）

新能力不一定要塞進原 MCU。

比較：
- current board
- target swap
- companion MCU
- MQTT/application gateway
- Pi/Linux host

選擇最低 total engineering/risk/cost 的 topology。

Domain owner 要清楚；gateway/composition layer 不應偷接管 credential、authorization、safety-critical ownership。

## 可抽成 Library，但不急著抽（Library-ready, not library-now）

Library-ready ≠ 現在就拆 library。

先維持 dependency direction、host-testability、portable public API、explicit ownership；等真實 consumer/reuse need 出現後再 extract。

避免 speculative package/repo/semantic versioning/generalization。

## 抽象命名穩定性（Abstraction Naming Stability）

跨層、可重用或預期會替換 backend 的 abstraction，名稱應跟**穩定 contract**走，不要把目前 concrete implementation 不必要地寫死進 public/internal boundary。

例如某層真正語意是 generic wired transport，而 RS485 只是 current PHY，則 transport-level owner / API / timing 名稱可使用 transport-neutral 語意；但 termination、transceiver direction、electrical turnaround 等真正屬於 RS485/PHY 的概念仍應保留 concrete 名稱。

原則：

- 先判斷 semantic owner，再 rename；不要 global search/replace。
- 只有真正 backend-neutral 的 symbol / interface / document heading 才 neutralize。
- 不得為了「未來可能換 backend」提前建立 speculative HAL / abstraction layer。
- behavior-preserving naming refactor 必須保留 value、ordering、timing、wire/API behavior，並依 `DEBUG_VALIDATION.md` 的 Behavior-Preserving Refactor Gate 驗證。
- 若 rename 發現現有 abstraction 其實洩漏 backend-specific behavior，先記錄 architecture gap，不要用命名掩蓋設計問題。

好的 abstraction naming 應讓 current implementation 可讀，也讓 future backend replacement 不必誤導性地沿用舊 concrete 名稱。

## External Service 文件 Authority 分離（External-service authority separation）

當專案同時包含 cloud、broker、third-party API、notification service、deployment target 或其他 external service，應避免把 governance、operator steps、service setup 與 protocol contract 混在同一份文件。

推薦分層：

`project governance → service routing/index → Codex/operator runbook → service-specific setup/config authority → protocol/runtime/security authority`

各層責任：

- **Project governance**：定義 repository-wide authority、Task/Stage authorization、permission/capability boundary、Git safety、failure/retry、secret handling 等穩定規則。
- **Service routing / index**：只回答「這類 service 問題應讀哪份 authority」，不要重複 protocol 或 setup 全文。
- **Codex / operator runbook**：定義 agent/operator 如何安全操作 service，包括 target selection、read-only/mutation boundary、credential handling、permission flow、validation 與 STOP 條件；不重新定義 product/protocol semantics。
- **Service-specific setup/config authority**：保存某個 service 真正的 deployment/configuration/resource/secret/setup 流程，可供人類 operator 獨立使用。
- **Protocol/runtime/security authority**：保存 machine contract、wire/API/topic/schema、runtime ownership、安全與 interoperability semantics；operator runbook 不得覆蓋它。

原則：

- 同一 stable policy 只保留一個主要 authority；其他文件用 routing/reference，避免全文複製造成 drift。
- Operator runbook 不得因方便操作而把 service credential、deployment target 或 protocol contract 自行重新定義。
- Service-specific setup 文件可以比共通 playbook 更具體，但不得削弱 repository governance 或 protocol/security authority。
- 若專案只有單一、簡單、低風險 external service，不必為形式建立完整目錄結構；只有當 service 數量、deployment target、credential、mutation boundary 或 operator workflow 複雜度值得時才拆分。

## 人機 UI 與 Machine Contract 邊界（Human-facing UI / Machine Contract Boundary）

Human-facing UI 是 presentation / interaction layer；不得因視覺一致性、文案整理、navigation、human-facing route normalization 或 component cleanup，偷偷改變較高權威的 runtime / machine contract。

一般原則：

- UI 必須忠實呈現 authoritative state。畫面已更新、request 已送出、handler 已回應或按鈕已被觸發，不等於 persistence、readback、restart、remote/network verification 或其他底層 operation 已真正完成。
- 狀態應依系統需要區分不同 authority 與時間尺度，例如 expected/configured、observed/detected、current health/connection、latest outcome、pending、unknown、history/counter。Evidence 不足時應使用 Pending / Unknown / Unavailable 等誠實狀態，不得猜成 Success / Healthy / Failed。
- Human-facing UI、navigation、wording、layout 或 route 工作，除非目前 scope 明確授權，不得修改 machine API、wire protocol、message/topic contract、persistence schema/semantics、authentication/authorization、session/CSRF、安全 ownership、runtime lifecycle 或 safety-critical behavior。
- 若 UI 工作揭露 machine/runtime contract 本身需要改變，停止目前 presentation-only scope；另進 architecture/contract decision 或獨立 scoped task，不得以 UI cleanup 名義順手修改。
- Secret 預設 write-only。UI、log、error、diagnostics 不得重新顯示 credential、password、token、shared secret 或其他 secret material，除非正式 product/security contract 明確要求且已有相應風險控制。
- Destructive、security-sensitive 或 physical-effect action 應在執行前清楚說明效果、影響範圍、不可逆性或 restart/recovery consequence，並依風險提供適當 confirmation；不得只依賴顏色或圖示表達危險程度。
- Status / error / warning / unknown 不得只靠顏色傳達；應提供可讀文字、label 或其他非顏色語意，避免無障礙與誤判問題。
- Current status、latest outcome、history/log 與 raw engineering diagnostics 應依使用者角色與行動價值分層；不要把 raw debug dump 當作一般 operator UI，也不要用漂亮摘要掩蓋 lower-level failure/evidence。

這些原則只定義 presentation 與 machine/runtime contract 的治理邊界；具體 route namespace、component library、visual style、copywriting、responsive breakpoint 與 device-specific vocabulary 仍由各 repository 的 UI/UX contract 決定。

## 獨立 Domain Repository／組合（Independent domain repos / composition）

Repository boundary 可依 domain ownership；deployment boundary 可依實際執行環境。

不同 domain repo 可透過 shared contract/composition layer 組合，但 domain repo 不應反向依賴 composition。

Same-process 優先 typed interface；跨裝置才適合使用 MQTT/transport contract。不要只為了解耦就在同一 process 自己對自己 MQTT。

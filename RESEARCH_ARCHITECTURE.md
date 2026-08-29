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

Target selection 也服從「最低充分」原則，但不能把「合理成長空間」解讀成預設挑資源最多的 target。應先找**最低合理候選**，再用 evidence 排除不足者；較高資源 target 可以降低 bring-up friction，但不能因開發方便、保守 margin 或未證實的未來需求，自動升格為 minimum product requirement。

推薦流程：

`Product requirements → Required capabilities → Lowest plausible target candidate → Upstream/toolchain evidence → Compile/static resource evidence → Runtime/resource evidence（需要時）→ Evidence-based reject/accept → Freeze minimum supported target`

### Development / Bring-up Target 與 Minimum Product Target 分離

- **Provisional Development / Bring-up Target**：可以暫時使用較多 RAM/Flash/core/PSRAM 或較成熟的 development board，目的是先降低工具鏈、framework 或初期 integration friction。必須明確標成 provisional；它不自動成為 architecture requirement、minimum supported target 或 product BOM requirement。
- **Minimum Supported / Product Target**：只有在 required capability 與適當 resource evidence 足以證明後才 freeze。若目前只有 compile evidence，只能宣告 compile/build support；不得把它翻譯成 runtime/hardware sufficiency。
- **Higher-capability Target**：可保留為 compatibility、scale-up 或 future option；「也能跑」不代表它是最低需求。

舉證原則：

- 不得只因較低資源 target「可能太緊」、「單核比較危險」、「沒有 PSRAM 比較不保險」就排除；應有官方 SDK/capability limitation、compile/resource evidence、runtime evidence 或其他可審查理由。
- 同樣地，不得只因較高資源 target「比較保險」、「比較好開發」、「之後可能會用到」就 freeze 成 minimum requirement；額外 core、RAM、Flash、PSRAM、radio/peripheral capability 都應有目前需求或 evidence 支持。
- 若較低候選明確缺少 REQUIRED hardware capability（例如必要 radio、peripheral、security primitive 或官方 SDK 支援），可依高權威 upstream evidence 直接排除，不需要為形式先 build/hardware test。
- 若 evidence 尚不足以判定最低 target，保持 `CANDIDATE` / `PROVISIONAL` 或等價 Pending 狀態；不要用 resource-rich target 把未知風險永久藏起來。
- OPTIONAL / FUTURE / OUT_OF_SCOPE capability 不得無條件墊高 v1 minimum target；只有已授權且合理可預期的 growth requirement 才能納入 headroom。

Resource headroom 是 legitimate design budget，但也有成本：BOM、功耗、尺寸、供應、portability，以及讓 implementation 無意識依賴多餘資源的風險。選擇時比較的是**已證明足夠候選中的最低 total engineering / risk / cost**，不是單看硬體價格，也不是單看開發便利性。

Embedded-specific 的 board/module/resource evidence 與 bring-up discipline 另見 `EMBEDDED_PROJECTS.md`。

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

## Evidence 觸發的複雜度升級（Evidence-triggered complexity escalation）

理論上「可能出問題」不等於應立即增加 architecture complexity。對 arbitration、scheduler、cache、queue、distributed lock、retry subsystem、HA/failover、rate limiter、新 HAL / abstraction layer 或其他會增加 ownership / state / operational complexity 的機制，先證明現有設計在代表性情境下確實不足。

推薦流程：

`Potential risk → Existing-behavior evidence → Representative validation → Unacceptable threshold → Confirmed/high-confidence root cause → Architecture escalation`

一般原則：

- 先定義什麼 evidence 才算「現有設計不可接受」，例如 latency、loss、duplicate、retry rate、starvation、availability、resource exhaustion、consistency violation 或 safety/security invariant breach。
- 若現有 recovery / retry / fallback / bounded degradation 在真實 workload 下已足夠可靠，可保留較簡單 architecture；不要只因最佳實務、理論碰撞、假想規模或未驗證未來需求就提前加入新機制。
- 只有 evidence 指向特定缺口，且 root cause 為 `CONFIRMED ROOT CAUSE` 或 `HIGH-CONFIDENCE LIKELY ROOT CAUSE` 時，才把對應 architecture work 從 Deferred 升為 active decision/implementation。
- 若 evidence 不足，先做 validation-only / observability Stage；不要以 speculative redesign 取代量測。
- 新機制若被觸發，仍應選能解決已證實問題的最低充分 complexity，不自動採最完整/最通用方案。

這是 condition-triggered baseline，不要求每個專案預先建立所有 resilience / arbitration / abstraction 機制。

## Failure Domain 最小化（Failure-domain minimization）

若某 operation 不需要某個 stateful、consistency-critical、remote、privileged 或 failure-prone dependency，就不應在沒有實際 ownership / contract 理由時強制經過該 dependency；否則該 dependency 的 failure 會不必要地擴大可用性與 blast radius。

判斷原則：

- 先確認 dependency 是否真正擁有該 operation 所需的 state、authorization、ordering、consistency、security 或 lifecycle contract；有正式 ownership 就不能為了「縮小 failure domain」繞過。
- 若 operation 實際是 stateless / independent，而目前 routing 只是歷史耦合，且已有 failure-domain evidence 或有明確可靠性價值，可考慮 behavior-preserving boundary reduction。
- Boundary reduction 不得破壞 signature/authentication、authorization、persistence、transactionality、ordering、audit、rate-limit 或其他正式 invariant。
- 若看似機械式的 dependency bypass 其實會改變 state ownership、consistency 或 security architecture，STOP，轉成獨立 architecture decision；不要把它當小 refactor 偷做。
- 不因看到 shared dependency 就預設拆分；只有不必要耦合已被 evidence 支持，且可維持 protected invariants 時才處理。

目標是讓 failure domain 與真正 dependency/authority boundary 對齊，而不是追求最多元件或最少共享依賴。

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

### 依 Authority Owner／Lifecycle Boundary 拆分

一條產品功能鏈若跨越多個獨立 provider 或 authority owner，而且各自擁有獨立的 credential、configuration、resource lifecycle、deployment/mutation boundary 或 validation authority，setup/config authority 應依**實際 authority owner / lifecycle boundary** 分離，再以 cross-reference 串接；不要只因多個 provider 共同完成同一產品功能，就把它們塞進同一份 setup 文件。

反過來也不得過度拆分：

- 不是「每個 API / endpoint / token / resource 一份文件」；
- 只有 authority owner、credential owner、configuration lifecycle、deployment/mutation boundary 或 validation authority 真正獨立時才值得拆；
- 同一 provider 內高度耦合、共同生命週期且沒有獨立治理價值的 setup 應保持聚合，避免文件碎片化；
- 文件名稱應反映主要 authority owner / lifecycle，而不是只沿用跨 provider 的產品功能名稱造成責任邊界模糊。

判斷重點是：**按 authority owner / lifecycle boundary 拆，不按產品功能名稱或 API 數量拆。**

一般原則：

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

## 外部 UI／Design System Reference 適配（External UI / Design-system Reference Adaptation）

研究成熟 UI framework、component library、design system 或公開 UI repository 時，應把它們視為**設計 evidence / reference**，不是自動導入 dependency、framework migration 或整套視覺複製的指令。

推薦流程：

`Current UI / stack / resource constraints → External reference inventory → Extract design principles / semantic tokens / interaction patterns → Fit against project constraints → Freeze project-specific UI contract → Project-owned primitives / fixtures → Checkpointed implementation → Automated audit / targeted validation / coverage reconciliation`

一般原則：

- **先保留現有技術棧。** 若目前 vanilla HTML/CSS、embedded server-rendered UI、native UI 或既有 framework 已能安全承載需求，不得只為取得某套外觀而引入 React、Tailwind、CSS-in-JS、animation runtime、external CDN 或其他新 dependency。只有 evidence 顯示現有 stack 無法合理滿足需求，且 migration 的 engineering/resource/security cost 已被評估時，才另開 stack decision。
- **抽象設計語意，不機械照搬 implementation。** 優先研究 typography、spacing rhythm、surface hierarchy、semantic color、radius、control sizing、action hierarchy、focus/disabled/error states、responsive behavior、accessibility 與 feedback semantics；framework-specific component tree、utility class、runtime theme engine 或 build pipeline 不應因 reference 存在就被複製。
- **使用最低充分 design token 層。** 對會跨多個 component / page 重複的值，優先建立 project-owned token / CSS variable / theme primitive，再由 component / page 使用語意名稱；避免每個 surface 各自 hard-code 顏色、間距、圓角與 focus style。實際 token 名稱、數值與 scale 仍由各 repository 決定，不在 common playbook 寫死。
- **Semantic role 優先於固定 palette。** Page/surface/foreground/muted/border/input/primary/secondary/destructive，以及 info/success/warning/error 等狀態應依產品需要以語意角色表達；light/dark 或其他 theme 優先切換 semantic token，而不是在每個 component 分散維護互相衝突的固定色碼。
- **Action hierarchy 必須對應 operation semantics。** Primary、secondary/outline、destructive、link/ghost 或等價層級應反映 action importance/risk，而不是只追求視覺變化；destructive / physical-effect / security-sensitive action 同時遵守上一節 Human UI / Machine Contract 的 confirmation 與文字語意要求。
- **Accessibility 是 design contract 的一部分。** Keyboard focus / `focus-visible`、可讀 contrast、disabled state、label/field 關係、非純色彩 status cue、touch target 與必要的 screen-reader semantics 應隨 component pattern 一起評估；不要只複製 reference 的外觀截圖。
- **Responsive 以實際內容與 target device 為 evidence。** 優先用少量、可解釋的 breakpoint / layout transition 解決真實 overflow、navigation、form、table、action-group 問題；不要因 reference framework 擁有完整 breakpoint scale 就在小型專案機械照搬。
- **Motion / visual effects 必須有 operator value。** Animation、shimmer、blur、gradient、parallax、GPU transform 或其他裝飾效果只有在能改善 state transition、attention、feedback 或 comprehension 時才採用；管理、安全、embedded 或 resource-sensitive UI 預設偏克制，並在適用時尊重 `prefers-reduced-motion`。不要為了「看起來像 reference」增加持續動畫與 runtime/payload burden。
- **Embedded / local-first / offline UI 要把 resource 與 availability 納入設計。** 字型、icon、CSS/JS、image、runtime framework 與 remote asset 都有 flash/RAM/network/startup/failure-domain 成本；若產品需要離線或區網獨立運作，關鍵 UI asset 不應無意依賴外部 CDN/service。具體 budget 由 project evidence 決定。
- **Reference provenance 仍適用。** 借鑑 pattern / design principle 與複製 source code 是不同層級；若實際 reuse component code、CSS、asset 或 algorithm，仍依本文件 Provenance / license 規則記錄來源、revision、license 與 reuse restriction。
- **把 UI consistency 變成可驗證 contract，而不是只靠 implementation session 記憶。** 當專案已有多個重複 component、page、theme、platform 或 operator flow，而且 style/behavior drift 已具有實際維護成本時，優先建立最低充分的 component preview / fixture / representative state matrix，讓 primary/secondary/destructive、normal/hover/focus/disabled/error/loading、light/dark 或其他重要狀態可以被獨立檢查。Preview/fixture 是 evidence surface，不應因此變成 production runtime dependency。
- **能 deterministic audit 的一致性就不要只靠人工目測。** 可依專案技術棧建立 lightweight static verifier / script / test，檢查例如 semantic token 使用、禁止的 hard-coded style、必要 focus/disabled/error semantics、theme/appearance contract、motion policy 或其他可機械判定 invariant。只有 visual diff 真正能降低風險時才導入 screenshot/visual-regression infrastructure；小型或 embedded UI 不要求為形式建立 Storybook、browser farm 或大型 visual test stack。
- **Audit scope 必須對齊 authority。** Theme/color/motion/appearance audit 證明的是其明確檢查的 presentation invariant，不得因 audit PASS 就升格為 runtime behavior、persistence、security、hardware 或完整 usability PASS；同樣地，純 styling change 若未改變較高層 contract，不應無理由使既有 runtime evidence失效。
- **Design research 與 implementation completeness 分離。** UI consistency 往往是 coverage-sensitive work；若 surface 多而分散，依 `CODEX_PROMPT_RULES.md` 的 `Coverage-sensitive work decomposition` 先做 bounded inventory，再以 coherent checkpoints 實作，每個 checkpoint STOP 後做獨立 coverage reconciliation，不讓同一個長 Prompt 同時負責 reference research、全域修改與 completeness self-judgment。

核心原則：**借成熟 design system 的規律，不借它不必要的技術棧；把重要 UI consistency 收斂成 project-owned contract 與最低充分 audit，再實作。**

## 獨立 Domain Repository／組合（Independent domain repos / composition）

Repository boundary 可依 domain ownership；deployment boundary 可依實際執行環境。

不同 domain repo 可透過 shared contract/composition layer 組合，但 domain repo 不應反向依賴 composition。

Same-process 優先 typed interface；跨裝置才適合使用 MQTT/transport contract。不要只為了解耦就在同一 process 自己對自己 MQTT。
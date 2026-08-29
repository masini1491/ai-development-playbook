# UI／UX 方法論（UI / UX Methodology）

本檔保存跨專案共通的 human-facing UI / UX、design-system reference、interaction semantics 與 UI consistency validation 方法。

具體 route namespace、component library、visual style、copywriting、spacing/radius/color 數值、responsive breakpoint 與 device-specific vocabulary 仍由各實際 repository 的 UI/UX contract 決定。

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

## UX 任務流與資訊層級（Task Flow / Information Hierarchy）

UI 結構應先服務使用者／operator 的實際任務，而不是直接映射 backend module、class、database table 或 firmware subsystem 的排列方式。

一般原則：

- 先辨識主要使用者角色、最常見任務、任務頻率、時效性、風險與必要 decision；只有這些 evidence 足以支持時才調整 information architecture。
- Primary task、需要立即判斷的 current status 與常用 action 應比 advanced configuration、rare maintenance、raw diagnostics 或歷史細節更容易被找到。
- Advanced / expert / diagnostic / destructive capability 可以依產品風險與使用頻率採 progressive disclosure、分區或二級頁面；不要為了「全部都看得到」把低頻高複雜度資訊和日常操作塞在同一視覺層級。
- Destructive / security-sensitive / physical-effect action 應與一般 primary workflow 有足夠的語意與視覺區隔，避免操作鄰近、誤觸或把危險行為包裝成普通 navigation。
- Navigation、section、form 與 status grouping 優先依使用者心智模型與 operation lifecycle 組織；若 backend ownership 與人類任務流不同，presentation layer 可以重新分組，但不得改變底層 authority / ownership。
- UI consistency 不等於所有頁面完全同構；共同 pattern 應一致，但 task-specific hierarchy 可以因使用情境、風險與內容密度合理不同。

核心判斷：**先讓人能快速理解「現在是什麼狀態、我能做什麼、做了會發生什麼」，再追求元件數量與視覺整齊。**

## Form／Feedback／Operation Lifecycle

表單與操作 feedback 應反映真實 transaction / operation lifecycle，而不是只在按下按鈕後顯示一個模糊成功訊息。

一般原則：

- Field 應依需要提供清楚 label、required/optional 語意、unit/format、constraint 與必要 helper text；placeholder 不應作為唯一 label 或唯一重要 instruction。
- Validation error 應盡量靠近相關 field / action，說明可修正的問題；若 failure 屬 system/service/runtime 而不是輸入錯誤，不要錯誤標成 field validation。
- 非安全理由不應在 submit failure 後無條件清空使用者已輸入的非 secret data；secret handling 仍服從 write-only / credential policy。
- 操作狀態依實際 contract 區分 `idle → validating → pending/in-progress → success / failure / unknown` 或專案等價狀態；不得因 request dispatch、HTTP 2xx、local state update 或 spinner 結束就自動宣稱底層 operation 完成。
- 當 operation 尚未完成且重複提交會造成 duplicate / race / physical effect 時，應避免 accidental double-submit；但 disabled state 必須能讓使用者理解原因，且不得形成沒有 timeout/recovery 的永久鎖定。
- 長時間 operation 應提供與 observability 相稱的 feedback，例如 pending、phase/progress（若可靠）、timeout、retry/recovery 或重新整理狀態；不知道進度時不要偽造百分比。
- Success / failure feedback 的持續時間與位置應符合重要性。關鍵設定、security、destructive 或 recovery outcome 不應只靠瞬間消失的 toast 作唯一 evidence。
- Error message 優先回答三件事：**發生什麼、目前可相信的狀態是什麼、使用者下一步能做什麼**。不要把 raw exception/code 當作唯一 operator explanation；工程 diagnostics 可以另層提供。

## 外部 UI／Design System Reference 適配（External UI / Design-system Reference Adaptation）

研究成熟 UI framework、component library、design system 或公開 UI repository 時，應把它們視為**設計 evidence / reference**，不是自動導入 dependency、framework migration 或整套視覺複製的指令。

推薦流程：

`Current UI / stack / resource constraints → External reference inventory → Extract design principles / semantic tokens / interaction patterns → Fit against project constraints → Freeze project-specific UI contract → Project-owned primitives / fixtures → Checkpointed implementation → Automated audit / targeted validation / coverage reconciliation`

一般原則：

- **先保留現有技術棧。** 若目前 vanilla HTML/CSS、embedded server-rendered UI、native UI 或既有 framework 已能安全承載需求，不得只為取得某套外觀而引入 React、Tailwind、CSS-in-JS、animation runtime、external CDN 或其他新 dependency。只有 evidence 顯示現有 stack 無法合理滿足需求，且 migration 的 engineering/resource/security cost 已被評估時，才另開 stack decision。
- **抽象設計語意，不機械照搬 implementation。** 優先研究 typography、spacing rhythm、surface hierarchy、semantic color、radius、control sizing、action hierarchy、focus/disabled/error states、responsive behavior、accessibility 與 feedback semantics；framework-specific component tree、utility class、runtime theme engine 或 build pipeline 不應因 reference 存在就被複製。
- **使用最低充分 design token 層。** 對會跨多個 component / page 重複的值，優先建立 project-owned token / CSS variable / theme primitive，再由 component / page 使用語意名稱；避免每個 surface 各自 hard-code 顏色、間距、圓角與 focus style。實際 token 名稱、數值與 scale 仍由各 repository 決定，不在 common playbook 寫死。
- **Semantic role 優先於固定 palette。** Page/surface/foreground/muted/border/input/primary/secondary/destructive，以及 info/success/warning/error 等狀態應依產品需要以語意角色表達；light/dark 或其他 theme 優先切換 semantic token，而不是在每個 component 分散維護互相衝突的固定色碼。
- **Action hierarchy 必須對應 operation semantics。** Primary、secondary/outline、destructive、link/ghost 或等價層級應反映 action importance/risk，而不是只追求視覺變化；destructive / physical-effect / security-sensitive action 同時遵守本文件 Human UI / Machine Contract 的 confirmation 與文字語意要求。
- **Accessibility 是 design contract 的一部分。** Keyboard focus / `focus-visible`、可讀 contrast、disabled state、label/field 關係、非純色彩 status cue、touch target 與必要的 screen-reader semantics 應隨 component pattern 一起評估；不要只複製 reference 的外觀截圖。
- **Responsive 以實際內容與 target device 為 evidence。** 優先用少量、可解釋的 breakpoint / layout transition 解決真實 overflow、navigation、form、table、action-group 問題；不要因 reference framework 擁有完整 breakpoint scale 就在小型專案機械照搬。
- **Motion / visual effects 必須有 operator value。** Animation、shimmer、blur、gradient、parallax、GPU transform 或其他裝飾效果只有在能改善 state transition、attention、feedback 或 comprehension 時才採用；管理、安全、embedded 或 resource-sensitive UI 預設偏克制，並在適用時尊重 `prefers-reduced-motion`。不要為了「看起來像 reference」增加持續動畫與 runtime/payload burden。
- **Embedded / local-first / offline UI 要把 resource 與 availability 納入設計。** 字型、icon、CSS/JS、image、runtime framework 與 remote asset 都有 flash/RAM/network/startup/failure-domain 成本；若產品需要離線或區網獨立運作，關鍵 UI asset 不應無意依賴外部 CDN/service。Embedded-specific self-contained UI contract 另見 `EMBEDDED_PROJECTS.md`。
- **Reference provenance 仍適用。** 借鑑 pattern / design principle 與複製 source code 是不同層級；若實際 reuse component code、CSS、asset 或 algorithm，仍依 `RESEARCH_ARCHITECTURE.md` 的 Provenance / license 規則記錄來源、revision、license 與 reuse restriction。

核心原則：**借成熟 design system 的規律，不借它不必要的技術棧；先建立符合目前產品限制的 project-owned UI contract，再實作。**

## UI Consistency Contract／Preview／Audit

當 UI surface 開始增加時，應把重要一致性從「implementation session 記得全部處理」逐步轉成可驗證、project-owned 的 contract；但只建立足以降低真實 drift / regression risk 的最低充分機制。

一般原則：

- 當專案已有多個重複 component、page、theme、platform 或 operator flow，而且 style/behavior drift 已具有實際維護成本時，優先建立最低充分的 component preview / fixture / representative state matrix，讓 primary/secondary/destructive、normal/hover/focus/disabled/error/loading、light/dark 或其他重要狀態可以被獨立檢查。
- Preview / fixture 是 evidence surface，不應因此變成 production runtime dependency；小型／embedded UI 可以用 static fixture、host-rendered snapshot 或其他低成本形式，不要求特定框架。
- **能 deterministic audit 的一致性就不要只靠人工目測。** 可依專案技術棧建立 lightweight static verifier / script / test，檢查例如 semantic token 使用、禁止的 hard-coded style、必要 focus/disabled/error semantics、theme/appearance contract、motion policy 或其他可機械判定 invariant。
- 只有 visual diff 真正能降低風險時才導入 screenshot/visual-regression infrastructure；小型或 embedded UI 不要求為形式建立 Storybook、browser farm 或大型 visual test stack。
- **Audit scope 必須對齊 authority。** Theme/color/motion/appearance audit 證明的是其明確檢查的 presentation invariant，不得因 audit PASS 就升格為 runtime behavior、persistence、security、hardware 或完整 usability PASS；同樣地，純 styling change 若未改變較高層 contract，不應無理由使既有 runtime evidence失效。
- Automated audit 與 human review 是互補關係：deterministic invariant 交給 verifier；task flow、information hierarchy、wording clarity、perceived affordance 與其他難以機械化的 UX 判斷仍需要 bounded human / independent review evidence。

## Coverage-sensitive UI Implementation

UI consistency 經常是「單項修改不難，但 surface 很多」的 coverage-sensitive work。若 surface 多而分散，不讓同一個長 Prompt 同時負責 external reference research、全域修改與 completeness self-judgment。

依 `CODEX_PROMPT_RULES.md` 的 `Coverage-sensitive work decomposition`：

`bounded inventory → coherent checkpoint → focused implementation → targeted validation → STOP → independent coverage reconciliation → next checkpoint → final closure reconciliation`

各 checkpoint 的 Model / Reasoning 仍按實際風險與內在難度選最低充分設定；不要只因 UI surface 多就自動升級模型。

## Embedded／Local-first UI Routing

如果產品有 local LAN、direct AP、first-setup、provisioning、recovery、Internet unavailable 或 MCU resource constraint，除了本文件外，再讀 `EMBEDDED_PROJECTS.md` 的 `Self-contained offline management UI`。

UI/UX 規則不授權 presentation layer 接管 machine/runtime ownership；physical-effect / safety-critical lifecycle 仍服從 embedded 專案的 safety arbitration 與 hardware evidence boundary。
# Information Integrity Guards

> **Authority**：跨專案 semantic identity、derived artifact authority、durable confirmed fact ownership、evidence provenance precision。
>
> **Read when**：目前工作涉及 aggregate/bundle identity、跨來源 synthesis、evidence metadata、provenance、或把 confirmed fact 保存到 report／analysis／eval 等 derived artifact。
>
> 本檔只保存跨專案 integrity contract；domain-specific ID 格式、lifecycle 名稱與資料 schema 仍由各 project owner 決定。

## Semantic Identity / Container Guard

Physical container 不等於 semantic identity。

若同一檔案、bundle、batch、multi-agent report 或其他容器中包含多個可被獨立詢問、驗證、更新、取代或引用的事實／task／evidence unit：

- 每個獨立 unit 應保留自己的 stable semantic identity 或可唯一定位的 canonical identity；
- 不得只因它們共享一個 physical container，就把原本獨立的 authority、evidence、task identity 壓成單一 aggregate identity；
- container 可以是 storage / transport / presentation unit，但不得因此取得其中所有 child unit 的 authority；
- 若舊 aggregate artifact 已混合多個獨立 identities，修正時優先保留 audit provenance，建立／恢復 per-unit current identity，再把 aggregate 降為 archive、wrapper 或 derived view，而不是重寫歷史。

核心原則：**Container may group identities; it does not merge their authority.**

## Derived Synthesis Authority Guard

由既有 canonical facts、evidence、task records 或多來源結果產生的 summary、comparison、matrix、report、ranking、prompt、eval summary 或其他 synthesis，預設是 **derived artifact**。

- derived synthesis 可以形成新的分析結論，但不得冒充 underlying source fact／execution evidence／task authorization；
- 沒有新增 observation、execution、draw/cast、measurement 或其他 source event 時，不得只因產生一份新總表就創造新的 source-fact identity；
- synthesis 若需要跨來源比較，應保留足以回到各 source identity 的 provenance／pointer；
- 若 synthesis 與 source authority 衝突，先回 canonical source reconciliation，不得讓較方便閱讀的 aggregate view 靜默覆蓋 source truth。

核心原則：**Derived synthesis may add interpretation; it does not inherit or manufacture source authority.**

## Durable Confirmed Fact Ownership Guard

若某 confirmed fact 具有跨 session、跨 task 或未來 decision 的持續價值，它不應只存在 report、analysis、prompt、eval record、conversation summary 或其他 derived artifact 裡。

在 durable reuse 前：

1. 找到該 fact 的合理 canonical factual owner；
2. 若 owner 尚未保存該 confirmed fact，先依 project governance 建立／更新 owner；
3. derived artifact 只引用或 snapshot 該 fact，並保留必要 provenance；
4. 若目前沒有 mutation authority，明確標記 canonical persistence 尚未完成，不得把 derived copy 冒充已 canonicalized。

這不要求每個一次性 observation 都建立新檔案；只有會持續影響未來 decision／retrieval 的 confirmed fact 才需要 durable factual ownership。

核心原則：**A durable confirmed fact needs a canonical factual owner before derived reuse becomes its de facto memory.**

## Provenance Precision Guard

Evidence metadata 必須保存實際可證明的 precision，不得用格式完整度冒充 evidence 完整度。

- 來源只提供分鐘級 timestamp，就保存 minute precision；不得補造秒數。
- 只知道 date、commit、runtime name、tool version 或其他單一 provenance field，不代表其他 provenance fields 已被驗證。
- `source commit known` 不等於 `raw runtime payload verified`；`command reported PASS` 不等於完整 execution environment 已知。
- unavailable／unknown／unverified 應保持原狀；可以明確標記 precision 或 verification boundary，但不得猜值填滿 schema。
- 後續取得更高精度 evidence 時，可以追加／升級 provenance；不得把後來取得的 metadata 回寫成「當時已知」。

核心原則：**Preserve evidence precision; verification does not propagate transitively across provenance fields.**

## Boundary

這些 guards 不要求所有 project 使用 global monotonic ID，也不規定 Tarot/Vault 類的 `reflective_only`、`waiting_for_reality` 等 domain lifecycle。跨專案只採用上面的 identity、authority、durable ownership 與 provenance precision 原則。

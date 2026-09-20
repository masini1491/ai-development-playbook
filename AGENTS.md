# 實戰手冊維護規則（Playbook Maintenance Rules）

本 repository 是公開、可分享的跨專案 AI-assisted development 方法論。維護時優先保持通用、精簡、可路由、可驗證，並控制 AI retrieval / Context 成本。

## 維護責任（Maintenance ownership）

本 repository 是**共通規則來源**，不是一般 product / firmware implementation repository。

固定維護邊界：

- **ChatGPT 是本 repository 的主要 AI maintainer**，可直接讀取、建立、更新、刪除本手冊內的規則與文件。
- ChatGPT 對本 repository 的 direct-write 也包含本手冊自身的最小 deterministic tooling 與其 tests；目前只限 `/tools/playbook_check.py`、`/tests/test_playbook_check.py`、`/tools/adoption_doctor.py`、`/tests/test_adoption_doctor.py`、`/tools/behavioral_eval.py` 與 `/tests/test_behavioral_eval.py`。這是 Playbook maintainer 例外，不授權一般 project 的 ChatGPT 修改 source/tooling，也不授權 Codex 寫入本 repository。
- **本 repository 的 AI 程式執行權只屬於具備目前任務所需 runtime / toolchain 的 ChatGPT session**：只有能實際滿足該 command 的 executable/version/dependency 與必要 filesystem/network capability 的 ChatGPT session，才可執行本 repository 內的 validator、tests 或其他程式／script。ChatGPT 能產生某語言的程式碼，不代表目前 execution environment 一定具備該語言的 runtime。若目前 session 不具備最低必要執行能力，應明確回報無法執行，不得因此交由 Codex、其他 coding agent、GitHub Actions、pre-commit 或其他自動化機制代跑，除非使用者日後明確改變本規則。
- **Codex / coding agent 對本 repository 預設唯讀**：可讀取並遵守本手冊，但不得以一般 project coordination → Codex implementation workflow 修改本 repository，也不得執行本 repository 內的程式／tests。
- 本 repository 的 `TASKS.md` 若存在，只作為 ChatGPT 維護本手冊時的暫時 unfinished-work queue；不代表要交由 Codex 執行。
- 一般 adopter project 的 AI mode selection 與 lower-level actor/path-action authority，分別由 `PROJECT_MODES.md` 與 `REPOSITORY_EXECUTION.md` 擁有；本檔不重述其 mode／fallback／mutation semantics。
- 不得把一般 project 的 ChatGPT coordination write boundary反向套用到本手冊自身。

若使用者日後明確變更本 repository 的維護 ownership，再依最新指示調整。

### Maintainer-only pre-canonical surface routing

`/maintainer/` 是本 repository 的 **maintainer-only、pre-canonical retrieval surface**，不屬於 ordinary Playbook bootstrap / capability discovery / gap review / implementation or validation routing。只有本次 intent 明確屬於 Playbook 自我維護時，才先讀 `/maintainer/README.md` 再進入必要子目錄，例如：Playbook self-review / self-correction、external governance or workflow comparison、Playbook evolution / productization research、suspected Playbook defect investigation、behavioral-evaluation candidate research、possible future-direction review 或 candidate persistence。

普通 capability inventory、repository-level gap / absence review、adopter-project task、implementation routing 或 validation routing **不得為了找更多 evidence 自動進入 `/maintainer/`**。其中內容是 maintainer working material / pre-canonical evidence；被保存、被找到或被引用都不會因此變成 Playbook capability、policy、bug、task、validation result 或 execution authority。Promotion 仍必須回到正常 canonical / work-admission / eval governance。

這是一個 **maintenance-only discovery pointer**，不是 normal canonical routing dependency；移除 `/maintainer/` 不得改變 ordinary Playbook behavior。

### Maintainer tooling execution pointer

本 repository 的 maintainer tooling 仍受上方 Maintenance ownership 約束：只有具備本次 command 所需實際 runtime／dependency／filesystem/network capability 的 ChatGPT session 可執行；Codex／coding agent 預設不得寫入或執行本 repository tooling。

Tool-specific runtime、正式 commands、Adoption Doctor input acquisition／GitHub Snapshot contract，以及 behavioral-eval tooling routing，統一由 [`tools/README.md`](tools/README.md) 擁有。**只有目前工作真的要執行、修改或驗證 maintainer tooling 時才讀該 leaf；普通 Playbook policy／documentation maintenance 不為形式載入。**

## 適用範圍（Scope）

只保存「怎麼開發」的共通方法，不保存任何特定專案的：
- secrets / credentials
- 客戶或個人資料
- 私有 endpoint / key
- 真實部署位址
- 專案專屬 GPIO / wiring
- 未公開 protocol secrets
- 只對單一產品成立的 current state

若某條規則只適用單一 repository，應留在該 repository 的 governance / architecture / coordination surface，而不是搬進本手冊。

## Audience / Surface Contract

`README.md` 是本 repository **唯一以人類閱讀為主要設計目的的 primary surface**。一般人類使用者應能只靠 README 理解本手冊的定位、導入方式、使用方法與主要能力；不要求依序閱讀其餘 canonical 文件才能開始使用。

README 的 human-facing language / layout contract：

- 預設維持單一 `README.md`，不要只因需要 English + Traditional Chinese 就建立平行 translation README。
- 主要主題採 **section-level bilingual semantic units**：English first，緊接 Traditional Chinese counterpart；不要把兩種語言拆成兩個巨大區塊，也不要逐句交錯。
- 維持 **contract-level semantic parity**：產品定位、能力聲明、authority boundary、onboarding、Showcase facts、caveats 與 links 必須語意一致；不要求 sentence parity、相同句數、相同語序、相同修辭或完全相同 heading tree。
- 每次 material README mutation 都在同次變更做 lightweight bilingual parity check；不要依賴日後定期大規模 translation refresh 才補 drift。
- 不用行數、KB、wall-clock age 或單純內容變長作 split-README threshold。只有出現真實 navigation／reading friction、反覆 semantic drift，或 meaningful language-routing user feedback 時，才重開 single-vs-split README judgment；Showcase 膨脹屬獨立 spin-out 問題，不自動觸發語言拆檔。

除 README 外，本 repository 的 canonical Markdown、routing index、adapter、eval、tooling contract 與治理文件主要是 **AI／agent-facing operational information surfaces**：用於 authority resolution、routing、execution、validation、evidence 與 durable project memory。它們仍應保持可被人類檢查與維護，但不以 tutorial-style human reading flow 作為主要最佳化目標。

維護時：

- 不得因「讓人更容易從頭讀完」就在 AI-facing canonical owner 重複 README 已有的介紹、教學或完整 policy；
- human-friendly explanation、導入步驟、產品定位與分享語境優先收斂到 README；
- AI-facing surface 優先最佳化 stable authority、bounded retrieval、exact routing、low duplication、terminology stability 與 machine／agent interpretability；**不要求繁體中文優先，也不要求所有 AI-facing 文件使用同一自然語言**；
- AI-facing wording 若英文、繁中或中英混合其中一種能更精確表達 canonical concept、降低歧義或改善 stable search/retrieval，就使用該表達；不要為語言一致性犧牲 semantic precision；
- README 可以摘要 canonical capability，但不得成為第二份 normative authority；規則語意仍由對應 canonical owner 決定；
- 人類可直接閱讀任何檔案，不代表該檔案因此成為 human-facing primary surface。

核心原則：**Human enters through README; AI enters through project governance / `CHAT_INIT.md` and routed canonical owners. README optimizes bilingual human readability; AI-facing operational surfaces optimize semantic precision, stable terminology, retrieval and authority.**

## 文件責任與讀取紀律（Document ownership / reading discipline）

本檔只擁有**本 repository 的 maintainer governance、maintenance boundary 與早期必須生效的 repo-specific rules**；詳細 task/topic routing 由 `CHAT_INIT.md` 擁有，AI-readable information architecture／retrieval-cost contract 由 `AI_CONTEXT.md` 擁有，各 domain normative semantics 由其 routed canonical owner 擁有。

維護時：

- 保持 **one rule/domain → one primary canonical owner**；若已有 owner，其他 surface只保留最低充分 routing／activation survival wording。
- AI／coding agent 不預設掃描全部 canonical files；從 current project governance／`CHAT_INIT.md` 直達本次最低必要 owner／section，exact target已知時可 direct-leaf。
- `README.md` 仍是唯一 human-facing primary overview；AI-facing canonical owners不為 human tutorial flow複製 policy。
- 新增／搬移／拆分 owner時，依 `AI_CONTEXT.md` 的 Independent Retrieval Intent、Action Contract Closure 與 AI Readability / Retrieval Cost Change Gate確認 routing與成本；不得把 `AGENTS.md` 重新膨脹成第二份 router。

## 權威順序（Authority）

本手冊不覆蓋實際專案的正式 technical source of truth。

一般 authority：
1. 使用者當次明確指示
2. 實際目標 repository 最新正式 governance/technical truth
3. 本手冊
4. 實際專案 current Hot coordination contract
5. 舊 Prompt / 舊聊天 / cached copy / memory

Cold/Candidate item、historical material或 AI 先前建議不因被持久化而升高 authority。

## 變更紀律（Change discipline）

新增規則前先確認：
- 是否真的跨專案重複出現
- 是否可由既有章節吸收
- 是否會和現有規則重複/衝突
- 是否有明確失敗案例或工程收益
- 是否形成獨立 retrieval intent；若沒有，優先更新既有 canonical owner
- 是否會提高 always-on/default-load Context、routing depth、search noise、duplication/reconciliation 或 derived write closure 成本

任何新增、刪除、搬移、拆分、合併 rule / file / router / information surface，都必須通過 `AI_CONTEXT.md` 的 **AI Readability / Retrieval Cost Change Gate**。少字、拆檔或新增 index 本身都不代表 AI 更快。

### Existing mechanism retirement evidence boundary

既有 rule / adapter / always-on mechanism 若因新 model、runtime 或其他 capability 進步而考慮簡化、縮窄適用範圍或退休，可使用 `DEBUG_VALIDATION.md` 的既有 behavioral/comparative evaluation mechanism 做 bounded ablation；但 **ablation PASS 只代表在實際 checked scope 中未觀察到 material marginal behavioral value，不等於該 mechanism globally unnecessary，也不等於 safe global removal 已成立。**

- Control 與 removal candidate 必須維持相同的 canonical invariant、expected behavior 與 forbidden behavior；不得先放寬 rubric／completion contract，再用新標準證明移除後「仍 PASS」。
- Evidence conclusion 與 retirement scope 不得超過實際覆蓋的 model／runtime／environment／scenario scope。只在特定新 model 或 runtime 觀察到冗餘時，最多支持對應 scope 的簡化／activation narrowing；不得自動泛化成跨 runtime／跨 model removal。
- Canonical authority、safety、permission、completion、activation 或 routing responsibility 不能只因模型在沒有明示 instruction 時「通常也會做對」就視為已被替代；behavioral tendency 不是 normative ownership 的替代證據。
- Retirement 前必須先辨識原 mechanism 實際承擔的 normative／routing responsibility，並確認其他 **current canonical mechanism** 已在 intended retirement scope 充分承接；若仍有 unique responsibility、coverage gap 或 authority ambiguity，保留／縮窄該 mechanism，而不是用沒有觀察到 regression 作 global deletion authority。
- 這是 condition-triggered maintainer inference boundary，不建立固定 ablation cadence、feature-debt registry、新 eval family 或全量 regression 義務。實際 evaluation design 仍由 `DEBUG_VALIDATION.md` 擁有；刪除／簡化後的 retrieval、authority 與 information-architecture impact 仍由 `AI_CONTEXT.md` 的 **AI Readability / Retrieval Cost Change Gate** 判斷。

核心原則：**No observed marginal behavioral value in a bounded ablation ≠ globally unnecessary. Safe retirement additionally requires unchanged invariants, scope-matched evidence, and complete transfer of the mechanism's current normative／routing responsibility.**

### ChatGPT direct-write mutation integrity

本 repository 的 ChatGPT direct-write 仍必須以 current canonical state 關閉 mutation evidence；GitHub-specific candidate／promotion／read-back／recovery mechanics由 `GITHUB_OPERATIONS.md` 擁有，generic permission／write boundary由 `REPOSITORY_EXECUTION.md` 擁有。

Repo-specific hard boundary：

- 不得 force push、reset-hard、rewrite history 或丟棄未知 user work。
- high-blast-radius replacement／搬移若出現 unintended deletion／truncation，先 STOP，以最近已知正常的 canonical Git history作恢復基準，再只重套原本授權的 bounded change；不得靠 memory重建。
- completion至少要有與 mutation scope相稱的 current canonical read-back；小型 bounded change不為形式全文重讀。

核心原則：**Direct-write capability does not waive canonical mutation evidence；generic GitHub mechanics stay in their canonical owner。**

優先修改既有主題文件，不要為每個新細節建立新檔。但若跨專案 evidence 顯示已形成穩定、可獨立 retrieval、具有清楚 ownership 的新 information architecture domain，可建立新 canonical owner；建立後其他文件只做 routing。

若 selected mode／current lifecycle 已形成清楚且持續的 ownership boundary，例如 `ChatGPT+Codex` 中 ChatGPT planning 與 Codex execution，應依 owner 分離 canonical policy；**不要因舊檔名或舊 routing 存在就永久保留 ownership mixing**。這是 policy-file ownership guidance，不建立新的 project AI mode。

若規則已存在 canonical topic owner，README、CHAT_INIT、其他文件只保留最低必要 routing；不要因方便閱讀再複製完整 normative policy。

## 禁止重複規則（No duplicated policy）

穩定規則只保留一個主要 authority；其他文件以簡短引用/routing為主，避免同一 policy 在多檔全文複製造成 drift。

Routing metadata 優先只保存穩定 ID/path/owner/entrypoint；除非本身是 canonical owner，不複製 volatile current status、validation result、architecture conclusion 或 evidence。

## 公開安全與可分享性（Public-safety / shareability）

所有新增內容在 commit 前檢查：
- 不含 secrets
- 不含私人身份/生活資料
- 不含 private repository 內容
- 不含未授權第三方程式碼的大段複製
- 外部 reference 若有必要，尊重 license/provenance

任何 evidence-like內容在**第一次 Git write 前**就必須 sanitized；不得先 commit敏感內容再靠後續刪除處理。

## 語言（Language）

Language policy follows the information surface, not a repository-wide translation preference.

- **`README.md`** follows the canonical human-facing language / layout contract in `Audience / Surface Contract` above: English first with a high-quality Traditional Chinese counterpart at section level; audience-aware rewriting is allowed while contract-level semantic parity is preserved.
- **All other canonical Markdown, indexes, adapters, evals, tooling contracts, and governance surfaces are AI／agent-facing.** They have no Traditional-Chinese-first requirement. Use the natural language or bilingual form that maximizes semantic precision, stable terminology, low ambiguity, machine/agent interpretability, and retrieval/search reliability.
- Keep exact identifiers, API/protocol names, status values, schema keys, paths, commands, model/tool names, quoted literals, and externally defined technical terms in their canonical form. Do not translate an exact term when translation would weaken matching or authority resolution.
- Within one canonical concept, prefer one stable term over stylistic synonym rotation. If English is more exact or more standard for the concept, English-first wording is acceptable; if Traditional Chinese is equally precise and clearer, it is also acceptable.
- Do not rewrite or translate existing AI-facing documents merely to make their natural language uniform. Language-only churn needs a concrete precision, ambiguity, routing, retrieval, or maintenance benefit.
- Human inspectability remains useful, but it is not a reason to reduce AI-facing semantic precision.

核心原則：**README optimizes English／Traditional-Chinese human communication under one canonical bilingual contract; AI-facing surfaces optimize semantic precision and reliable retrieval, regardless of natural language.**

## Git 安全（Git safety）

預設 main 是 source of truth。修改前確認 repository identity、branch、HEAD 與 working state；禁止 force push、reset-hard、rewrite history 或丟棄未知 user work。

若遇 permission denial，遵守 `REPOSITORY_EXECUTION.md` 的 Permission-Gated Operation。
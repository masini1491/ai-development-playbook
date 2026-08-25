# Toolchain / Runtime Contract

## General rule

專案依賴的 interpreter、compiler、SDK、CLI、runtime 與主要 build tools，應以**實際支援/驗證的 executable + version contract** 表達；不得只寫模糊產品名稱，也不得假定 OS 內建的同名或相近工具相容。

範例：
- PowerShell 7 → `pwsh`
- Windows PowerShell 5.1 → `powershell.exe`
- Python → `python` / `py` + actual version
- Node.js → `node` + version
- Java → `java` / `javac` + major version
- ESP-IDF → `idf.py` + IDF version
- Arduino CLI → `arduino-cli` + version
- CMake → `cmake` + version

## Windows / PowerShell 7 baseline

若互動式本機開發環境以 Windows 為主，而且 repository 使用自有 `.ps1`：

- 正式 PowerShell runtime 使用 **PowerShell 7 / `pwsh` / `PSEdition Core`**。
- Windows PowerShell 5.1 `powershell.exe` 視為不同 runtime。
- 不得因系統存在 `powershell.exe` 就宣稱已滿足 PowerShell 7 dependency。
- 不得在 `pwsh` 缺失時 silent fallback 到 `powershell.exe`。
- 執行正式 `.ps1` tooling / verifier 前，優先用 `pwsh --version` 做最小 preflight。
- 若 repository 有更精確的 minimum/supported PS7 version，以 repository contract 為準；否則不需無理由 pin 到某個 patch version。

## Failure handling

- `pwsh` 不存在 → `TOOLCHAIN` prerequisite missing。
- `pwsh` version 不符合 contract → `TOOLCHAIN` version mismatch。
- 不得因此修改 production source，或為了 PS5.1 去改寫本來在 PS7 正常的 script。
- `pwsh` 存在但 sandbox/filesystem/execution permission denied → 先走 `Permission-Gated Operation`，不是直接判定 TOOLCHAIN/SOURCE failure。
- `pwsh` 存在、版本正確、權限正常後 script 才真正失敗 → 再依 evidence 判斷 SOURCE / TOOLCHAIN / ENVIRONMENT 等。

## No silent host mutation

Coding agent 不得自行安裝、升級、降級 PowerShell 或其他 host runtime，除非使用者明確授權。

## Validation evidence

需要可重現證據時，記錄：
- actual runtime/tool version
- exact executable/command
- relevant target/FQBN/SDK version
- tested commit SHA
- CI run（若適用）

Validation PASS 不只要證明 script/test 有跑，也要證明**使用的是 intended runtime/toolchain**。

## Windows local != Windows-only CI

本機 Windows baseline 不代表 repository 的所有 CI/host tests 都要改成 Windows。

若既有 Linux/Ubuntu GitHub Actions、CMake host tests、ESP-IDF CI 或其他 cross-platform validation 正常：保留它們。

不要：
- 把非 PowerShell tooling 強迫改寫成 `.ps1`
- 為了統一 host 而移除 cross-platform CI
- 因本機 Windows baseline 宣稱 repository 只支援 Windows，除非 repository 本身就是如此定義

## Windows PowerShell 5.1 compatibility

預設不要求 dual-support。

若未來真的需要 PS5.1：
- 當成獨立 compatibility scope
- 逐支 parser/execution validation
- 不得為相容 5.1 弱化既有 verifier assertions 或正式 PS7 contract

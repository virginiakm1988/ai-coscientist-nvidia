# Evidence-Oriented AI Co-Scientist：快速入門

以研究主張、實驗證據、可執行檢查到引用報告建立完整流程。包含證據一致、缺漏、錯誤引用與數值不符四種情境。NIM 只能解釋檢查結果，不能覆寫工具判定。

## 操作

1. 建立這個 repo 專用的 Python 3.12 環境，避免不同專案的 `project_demo` 套件互相覆蓋。
2. `python -m pip install -e .`
3. `python -m project_demo prepare --output-dir runs/preparation`
4. `python -m project_demo demo --mode fixture --output-dir runs/fixture`
5. 開啟 [互動 Colab](https://colab.research.google.com/github/virginiakm1988/ai-coscientist-nvidia/blob/main/notebooks/01_interactive_demo.ipynb)，先看範例，再依需求切換真實執行。

`fixture` 是教學範例，不是實際模型輸出。`live` 失敗時會保存錯誤，不會自動換成範例成功結果。每次執行都有獨立輸出目錄、設定與時間紀錄。API key 請使用環境變數或 Colab Secrets；不要寫進程式或公開 repo。

真實 agent 執行需安裝 `.[agents]`，設定 NVIDIA_API_KEY 後使用 `--mode live --engine fabric`。Fabric 管理生命週期、Relay 記錄執行；Helix 可在遠端環境重新評分。

完整步驟、驗收、限制與來源請見 [英文 README](README.md) 與 [Playbook](docs/PLAYBOOK.md)。

# STD Statistical Studio v0.6 — CHANGELOG

## Repository baseline — 2026-07-28

- 將目前已驗收的 v0.6 設為唯一開發基底，不再由 v0.5 生成。
- 新增 canonical source：`src/std_statistical_studio.html`。
- 新增無 bundler 的 `scripts/build.py`，同步產生 `dist/std_statistical_studio.html` 與 `docs/index.html`。
- 新增 release structure verification、內嵌 JavaScript syntax check 與 GitHub Actions。
- 新增 GitHub Pages `/docs` 發布結構、專案規則、README、STD Schema 與統計規則文件。
- 此基線不變更已通過的 v0.6 統計公式與 UI 行為。

## 基底與架構

- 以 `std_statistical_studio_v0_5.html` 為唯一基底延伸，保留單一 HTML、純前端與直接開啟的交付形式。
- 未加入 React、Vue、後端、建置期框架或統計套件。
- 保留 SheetJS CDN 作為 Excel 解析器；CSV、示範資料與所有統計運算不依賴 SheetJS。
- 將原本分散的程序標題、欄位角色、最低需求、假設、輸出、圖表、執行函式與防呆條件集中到 `PROCEDURE_REGISTRY`。
- 左側 10 類主選單、Inspector、Method Strip、Procedure Plan 與 Validator 均由 Registry 生成。
- 移除以 `switch(state.activeProc)` 控制全部程序的做法，改由 Registry 的 `execute` 與 `validator` 分派。

## 新增功能

### Procedure Registry 與 Validator

- 建立 39 個具版本的 Procedure 定義。
- 每個 Procedure 都記錄：
  - `id`
  - `version`
  - `category`
  - `label`
  - `description`
  - variable roles
  - minimum requirements
  - assumptions
  - outputs
  - recommended charts
  - execute function
  - validator function
- 執行狀態統一為 `Ready`、`Warning`、`Rejected`、`Completed`。
- 資料不足、群組數錯誤、規格缺漏或 Xbar-R 子組條件不符時會拒絕計算，也不繪製誤導圖。
- Result IR 加入 `procedure_id`、`procedure_version`、engine version、參數、假設、警告及排除列。

### Assumption Advisor

- 新增問題導向選擇、假設檢查與方法推薦。
- 群組診斷包含各組 n、mean、median、SD、IQR、偏態、Q-Q correlation、IQR 離群數、變異數比值與 Brown-Forsythe test。
- 以 deterministic rule engine 推薦 pooled t、Welch t、Mann-Whitney、One-way ANOVA、Welch ANOVA 或 Kruskal-Wallis。
- 畫面同時顯示推薦原因、替代方法、未通過假設、警告與不允許的推論。
- 迴歸診斷包含 X 變異、樣本數、residual vs fitted、residual Q-Q、異質變異指標、leverage 與 Cook's distance 初步高影響點偵測。

### 群組比較與 post-hoc

- 新增 One-sample t-test。
- 新增 pooled two-sample t-test 與 Welch t-test。
- 新增 Paired t-test。
- 新增 Mann-Whitney U 與 Wilcoxon signed-rank。
- 新增 Welch ANOVA。
- 新增 Tukey HSD、Games-Howell、Dunn + Bonferroni。
- Post-hoc 表格包含 Group A、Group B、Difference、Standard Error、Statistic、Raw p-value、Adjusted p-value、95% CI 與 Significant。
- 新增 difference／confidence interval plot 與顯著組合標示。

### SPC Nelson Rule Engine

- 建立獨立 `SPC_RULES` Registry。
- 實作 Nelson Rule 1–6：
  1. 一點超出 3σ
  2. 連續 9 點位於中心線同側
  3. 連續 6 點持續上升或下降
  4. 連續 14 點上下交替
  5. 3 點中有 2 點超過同側 2σ
  6. 5 點中有 4 點超過同側 1σ
- I 與 Xbar 圖套用 Rule 1–6；MR 與 R 圖只套用適用的 Rule 1。
- 不同規則以不同符號呈現，Hover 顯示 Rule ID；Result IR 與摘要列出觸發點。

### Audit Trail

- 每次成功或被拒絕的分析均建立 Audit Record。
- 記錄 engine/procedure version、時間、來源、欄位映射、參數、SPC 常數、排除列、警告、狀態與 deterministic FNV-1a result hash。
- 新增 Audit Trail 輸出頁籤。

### Statistical Self-test

- 新增 Developer → Statistical Self-test。
- 以固定資料與固定預期值驗證 mean、sample SD、quantile、t-test、ANOVA、Welch ANOVA、regression、Cpk、Ppk、I-MR、Xbar-R 與 PCA。
- 18 項測試全部逐筆輸出 expected、actual、absolute error、tolerance 與 PASS/FAIL。

### LLM 分工

- LLM Prompt 明確限制 LLM 只能處理欄位映射、分析計畫與文字轉譯。
- 明確禁止 LLM 計算 p-value、F、Cpk/Ppk、迴歸係數、PCA、管制界線與 SPC violations。
- 固定包含：
  - `Do not calculate statistics.`
  - `Do not invent specifications.`
  - `Do not infer causality.`
  - `Return only schema-compliant JSON.`

## 公式與演算法

- t-test：Student t distribution，包含 one-sample、pooled、Welch 與 paired 版本。
- ANOVA：between/within sum of squares、F distribution、eta squared。
- Welch ANOVA：權重、Welch correction 與 Satterthwaite denominator degrees of freedom。
- Brown-Forsythe：以各組 median absolute deviation 執行 one-way ANOVA。
- Mann-Whitney／Wilcoxon／Dunn：平均秩、tie correction、常態近似與 Bonferroni adjustment。
- Tukey／Games-Howell：以 deterministic studentized-range family-wise approximation計算 adjusted p-value，並以同一臨界值反解 simultaneous CI。
- 迴歸：OLS、斜率 t-test、95% CI、R²、residual diagnostics、leverage 與 Cook's distance。
- Cpk：組內變異採 subgroup `R̄/d2`；Ppk 採 overall sample SD。
- I-MR：`MR̄/1.128` 與固定管制圖常數。
- Xbar-R：依子組 n 使用 `A2`、`D3`、`D4`。
- PCA：標準化後相關矩陣、Jacobi eigen decomposition、eigenvalue/eigenvector 排序與 scores。
- 所有統計數值均由 deterministic JavaScript 產生。

## UI 改動

- 維持 v0.5 深色統計工作站視覺，增加一致的狀態標籤、方法說明、假設項目與輸出頁籤。
- 右側 Inspector 分為 Variable Roles、Procedure Parameters、Assumptions、Execution、Result Summary。
- 左側會自動展開目前 Procedure 所屬類別。
- 針對一般筆電寬度調整響應式版面；空間不足時 Inspector 移至分析區下方，避免裁切。
- 保留列印／PDF、專案 JSON 匯出、Canvas 圖表、示範資料與 Excel／CSV 載入。

## 相容性

- 舊 v0.5 的資料匯入、表頭偵測、STD 欄位映射、規格編輯、描述統計、分布圖、群組圖、相關／迴歸、製程能力、I-MR、Xbar-R、PCA、主管摘要、列印與專案匯出均保留。
- 仍為單一 HTML；無需安裝、後端或 npm。
- 支援現代 Chromium、Edge、Chrome。Excel 匯入需可存取既有 SheetJS CDN；離線時仍可使用 CSV 與內建示範資料。

## 尚未完成項目／已知限制

- 本規格所列驗收項目無阻斷性未完成項目。
- Tukey 與 Games-Howell 的 studentized-range 尾機率使用透明、可重現的 deterministic family-wise approximation；數值不保證與 SAS/R 的高精度 studentized-range implementation 在最後小數位完全相同。
- Mann-Whitney、Wilcoxon 與 Dunn 目前採 tie-corrected large-sample normal approximation，不提供小樣本 exact permutation p-value。
- Excel 解析沿用 v0.5 的 SheetJS CDN；完全離線環境請使用 CSV。

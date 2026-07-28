# CODEX 任務：STD Statistical Studio v0.6

> 專案覆寫（2026-07-28）：目前已完成並驗收的
> `src/std_statistical_studio.html` 為唯一開發基底。本文中要求由 v0.5
> 開始的敘述只保留為歷史規格背景，不得用來覆寫或重新生成目前 v0.6。

## 一、現有專案

請以以下檔案作為唯一基底，不要重寫成另一套框架：

- `std_statistical_studio_v0_5.html`

目前產品定位：

> 一個以瀏覽器執行的統計套裝工具。
> 將 Excel／CSV 轉為 STD 標準資料，經過可驗證的統計 Procedure Engine 計算，再輸出圖表、Result IR、主管報告與 LLM Prompt。

目前技術限制：

- 使用單一 HTML 作為最終交付。
- 前端使用 HTML、CSS、Vanilla JavaScript。
- 目前只有 SheetJS 用於讀取 Excel。
- 不要改成 React、Vue、Angular。
- 不要新增後端。
- 不要加入大量 npm 套件。
- 不要讓 LLM 計算統計結果。
- 所有統計數值必須由 deterministic JavaScript 計算。
- 可以在開發階段拆分 JS 模組，但最後要能輸出單一 HTML。

---

# 二、目前 v0.5 已有功能

## 資料準備

- Excel／CSV 匯入
- 自動猜測表頭
- 欄位型態判斷
- 缺值與唯一值統計
- USER 欄位映射為 STD
- LOT、日期、機台欄位設定
- 量測欄位的 STD ID、USER Label、單位、LSL、USL、Target

## 描述與分布

- 描述統計
- Histogram
- ECDF
- Normal Q-Q plot
- Category count bar
- Pareto chart

## 群組比較

- Grouped box plot
- Mean plot + 95% CI
- One-way ANOVA
- Kruskal–Wallis

## 關聯與迴歸

- Scatter plot
- Pearson correlation
- Spearman correlation
- Simple linear regression
- Residual vs fitted

## SPC

- Capability histogram
- Cpk／Ppk
- I-MR chart
- Xbar-R chart

## 多變量

- Correlation heatmap
- Parallel coordinates
- PCA 2D projection

## STD／LLM

- STD JSON
- Procedure Plan
- Result IR
- Translator Prompt
- Supervisor Report

---

# 三、v0.6 核心目標

不要只增加更多圖表。

v0.6 必須把目前的工具升級為：

> Procedure Registry + Assumption Advisor + Post-hoc + SPC Rule Engine

主要目標有四個：

1. 將所有分析程序資料化為 Procedure Registry。
2. 建立分析前假設檢查與方法推薦。
3. 補上 ANOVA 之後的事後比較。
4. 補上 SPC 的 Nelson／Western Electric 規則。

---

# 四、任務 A：Procedure Registry

目前各 Procedure 的 title、roles、rule 與執行函式散落在程式中。

請改成統一結構，例如：

```javascript
const PROCEDURE_REGISTRY = {
  "compare.anova.one_way": {
    id: "compare.anova.one_way",
    category: "group_comparison",
    label: "One-way ANOVA",
    description: "比較多組平均值。",
    roles: {
      response: {
        type: "numeric",
        required: true
      },
      factor: {
        type: "categorical",
        required: true
      }
    },
    minimumRequirements: {
      groups: 2,
      observationsPerGroup: 2
    },
    assumptions: [
      "independence",
      "approximate_normality",
      "equal_variance"
    ],
    outputs: [
      "anova_table",
      "f_statistic",
      "p_value",
      "eta_squared"
    ],
    recommendedCharts: [
      "group_boxplot",
      "mean_ci_plot",
      "residual_qq"
    ],
    execute: runOneWayAnova
  }
};
```

## 必須達成

- 左側大標題與子選單由 Registry 自動生成。
- Inspector 的欄位角色由 Registry 生成。
- Method Strip 的資料角色與防呆文字由 Registry 生成。
- Result IR 必須記錄 `procedure_id` 和 `procedure_version`。
- 不要再用大 switch 寫死所有 Procedure。
- 每個 Procedure 應有：
  - id
  - version
  - category
  - label
  - description
  - variable roles
  - minimum requirements
  - assumptions
  - outputs
  - recommended charts
  - execute function
  - validator function

---

# 五、任務 B：Assumption Advisor

新增左側主選單：

```text
統計顧問
├─ 問題導向選擇
├─ 假設檢查
└─ 方法推薦
```

## 問題導向選擇

讓使用者先選擇想回答的問題，而不是先選方法：

- 看單一連續變數的分布
- 比較兩組數值
- 比較三組以上
- 比較成對資料
- 找兩個連續變數的關係
- 檢查時間序列穩定性
- 評估製程能力
- 探索多變量結構

## 假設檢查

至少加入：

### 群組比較

- 各組 n
- 各組 mean
- 各組 median
- 各組 SD
- 各組 IQR
- 群組樣本數是否足夠
- 變異數比值
- Brown–Forsythe 或 Levene test
- 每組或殘差 Q-Q 診斷

### 迴歸

- X 是否有變異
- n 是否足夠
- residual vs fitted
- residual Q-Q
- 異質變異警告
- 高影響點初步偵測

## 方法推薦規則

建議使用規則引擎，不要交給 LLM：

```text
兩組、近似常態、變異接近
→ pooled two-sample t-test

兩組、變異不同
→ Welch t-test

兩組、偏態或嚴重離群
→ Mann–Whitney U

三組以上、近似常態、等變異
→ One-way ANOVA

三組以上、變異不同
→ Welch ANOVA

三組以上、偏態或離群
→ Kruskal–Wallis
```

輸出範例：

```json
{
  "recommended_procedure": "compare.anova.welch",
  "confidence": 0.86,
  "reasons": [
    "3 groups detected",
    "Brown-Forsythe p < 0.05",
    "group variances are unequal"
  ],
  "alternatives": [
    "compare.kruskal_wallis"
  ],
  "warnings": [
    "Group sizes are small"
  ]
}
```

畫面必須清楚顯示：

- 推薦方法
- 原因
- 替代方法
- 假設未通過的項目
- 不允許的推論

---

# 六、任務 C：補齊群組比較

v0.6 至少加入：

- One-sample t-test
- Two-sample pooled t-test
- Welch t-test
- Paired t-test
- Mann–Whitney U
- Wilcoxon signed-rank
- Welch ANOVA

## 事後比較

至少加入：

### ANOVA 後

- Tukey HSD

### Welch ANOVA 後

- Games–Howell

### Kruskal–Wallis 後

- Dunn test + Bonferroni adjustment

輸出表格至少包含：

```text
Group A
Group B
Difference
Standard Error
Statistic
Raw p-value
Adjusted p-value
95% CI
Significant
```

## 顯示方式

新增：

- Pairwise comparison table
- Difference plot 或 confidence interval plot
- 顯著組合標示
- 不要只顯示「ANOVA 顯著」

主管摘要應能寫：

```text
整體群組差異達顯著。
Games–Howell 顯示機台 7261 與 7138 有顯著差異，
但 7261 與 119 沒有足夠證據認為平均不同。
```

禁止寫成：

```text
7138 機台造成推力下降。
```

---

# 七、任務 D：SPC Rule Engine

目前只檢查超出 UCL／LCL。

請建立獨立 SPC Rule Engine。

至少加入 Nelson Rules：

1. 一點超出 3σ
2. 連續 9 點位於中心線同一側
3. 連續 6 點持續上升或下降
4. 連續 14 點上下交替
5. 3 點中有 2 點超過同側 2σ
6. 5 點中有 4 點超過同側 1σ

資料結構建議：

```javascript
const SPC_RULES = [
  {
    id: "nelson.rule_1",
    label: "超出 3σ",
    evaluate: detectRule1
  },
  {
    id: "nelson.rule_2",
    label: "連續 9 點同側",
    evaluate: detectRule2
  }
];
```

輸出 Result IR：

```json
{
  "chart": "xbar",
  "violations": [
    {
      "rule_id": "nelson.rule_1",
      "points": ["LOT-08"],
      "message": "LOT-08 超出 UCL"
    },
    {
      "rule_id": "nelson.rule_3",
      "points": ["LOT-09", "LOT-10", "LOT-11", "LOT-12"],
      "message": "連續上升趨勢"
    }
  ]
}
```

圖表要求：

- 不同 Rule 可以用不同符號，不要只靠顏色。
- Hover 或點擊時顯示 Rule ID。
- 報告列出各 Rule 觸發的點。
- Xbar-R 和 I-MR 都套用規則。
- R 或 MR 圖主要仍檢查適用的規則，避免錯誤解讀。

---

# 八、任務 E：Audit Trail

每次分析都建立 Audit Record：

```json
{
  "engine_version": "0.6.0",
  "procedure_id": "spc.xbar_r",
  "procedure_version": "1.0.0",
  "executed_at": "ISO datetime",
  "source": {
    "file_name": "...",
    "sheet_name": "...",
    "row_count": 36
  },
  "mapping": {
    "production.lot_id": "LOT NO.",
    "measurement.push_force": "推力"
  },
  "parameters": {
    "subgroup_size": 3
  },
  "constants": {
    "d2": 1.693,
    "A2": 1.023,
    "D3": 0,
    "D4": 2.574
  },
  "excluded_rows": [],
  "warnings": [],
  "result_hash": "..."
}
```

## UI

新增底部頁籤：

- STD JSON
- Procedure Plan
- Assumption Report
- Result IR
- Audit Trail
- LLM Prompt

---

# 九、任務 F：測試與可信度

新增內建測試資料，不需要額外測試框架也可以。

建立：

```javascript
const TEST_CASES = [
  {
    id: "anova_basic_001",
    procedure: "compare.anova.one_way",
    input: {...},
    expected: {
      F: ...,
      p: ...
    },
    tolerance: 1e-8
  }
];
```

至少覆蓋：

- mean
- sample SD
- quantile
- ANOVA F
- Welch ANOVA
- t-test
- regression slope
- regression R²
- Cpk／Ppk
- I-MR limits
- Xbar-R limits
- PCA eigenvalues

新增隱藏或開發用頁面：

```text
Developer
└─ Statistical Self-test
```

顯示：

```text
PASS 18
FAIL 0
```

不得只測試程式是否執行，必須比對數值誤差。

---

# 十、UI 要求

維持目前統計工具式左側分類，但重新整理成：

```text
01 資料準備
02 統計顧問
03 描述與分布
04 群組比較
05 關聯與迴歸
06 製程與 SPC
07 多變量分析
08 STD／LLM
09 報告輸出
10 Developer
```

## 中央區

每次只顯示目前 Procedure 的：

- Main result
- Main chart
- Diagnostic charts
- Assumption status
- Warnings

不要一次顯示全部圖。

## 右側 Inspector

分區：

```text
Variable Roles
Procedure Parameters
Assumptions
Execution
Result Summary
```

## 狀態標籤

每個 Procedure 顯示：

- Ready
- Warning
- Rejected
- Completed

不要讓資料不足的程序仍然產生空白圖。

---

# 十一、統計原則

必須遵守：

- p-value 不得單獨作結論。
- 顯示 effect size。
- 顯示 confidence interval。
- 顯著不等於因果。
- 不得自動補規格。
- 不得把 missing 當 0。
- 不得默默刪除資料。
- 每個被排除的 row 必須記錄原因。
- 能力分析前顯示穩定性狀態。
- 迴歸必須提供 residual diagnostics。
- ANOVA 顯著後必須引導到 post-hoc。
- 小樣本時必須提出限制。
- 多重比較必須調整 p-value。

---

# 十二、LLM 分工

LLM 只能負責：

- 欄位語意映射
- STD ID 建議
- Procedure Plan 建議
- 已計算結果的文字轉譯
- USER Label 本地化

LLM 不得負責：

- p-value
- F statistic
- Cpk／Ppk
- 迴歸係數
- 管制界線
- PCA
- SPC Rule 判定

Prompt 中必須明寫：

```text
Do not calculate statistics.
Do not invent specifications.
Do not infer causality.
Return only schema-compliant JSON.
```

---

# 十三、開發架構

雖然最終仍輸出單一 HTML，但請在開發過程按邏輯區塊整理：

```text
core/
  procedure-registry.js
  validator.js
  result-ir.js
  audit.js

statistics/
  descriptive.js
  tests.js
  anova.js
  posthoc.js
  regression.js
  spc.js
  multivariate.js

charts/
  distribution.js
  comparison.js
  regression.js
  spc.js

ui/
  navigation.js
  inspector.js
  workspace.js
  output-tabs.js
```

如果不建立實際檔案，也必須在單一 HTML 裡用清楚註解區分模組。

最終仍交付：

```text
std_statistical_studio_v0_6.html
```

---

# 十四、驗收條件

完成後請逐項確認：

- [ ] 舊 v0.5 功能仍可使用
- [ ] 選單由 Procedure Registry 生成
- [ ] 不再以大 switch 控制所有 Procedure
- [ ] Assumption Advisor 可推薦 ANOVA／Welch／Kruskal
- [ ] 有 Levene 或 Brown–Forsythe
- [ ] 有 Welch ANOVA
- [ ] 有 Tukey HSD
- [ ] 有 Games–Howell
- [ ] 有 Dunn + Bonferroni
- [ ] 有兩組與成對比較方法
- [ ] 有 Nelson Rule Engine
- [ ] Xbar-R 和 I-MR 顯示 Rule violations
- [ ] Result IR 具備 procedure version
- [ ] 有 Assumption Report
- [ ] 有 Audit Trail
- [ ] 有數值 Self-test
- [ ] 資料不足會 Rejected，不畫誤導圖
- [ ] 最終輸出為單一 HTML
- [ ] 不新增後端
- [ ] 除 SheetJS 外不要依賴大量套件

---

# 十五、執行方式

請直接開始檢查與修改現有 `std_statistical_studio_v0_5.html`。

工作流程：

1. 先閱讀並整理現有程式結構。
2. 不要先重寫 UI。
3. 先建立 Procedure Registry 與 Validator。
4. 將現有 Procedure 逐步遷移。
5. 加入 Assumption Advisor。
6. 加入群組比較與 post-hoc。
7. 加入 SPC Rule Engine。
8. 加入 Audit Trail 與 Self-test。
9. 最後才整理 UI。
10. 完成後實際在瀏覽器測試所有主選單。

輸出：

- `std_statistical_studio_v0_6.html`
- `CHANGELOG_v0_6.md`
- `TEST_REPORT_v0_6.md`

在 CHANGELOG 說明：

- 新增功能
- 公式與演算法
- UI 改動
- 相容性
- 尚未完成項目

在 TEST_REPORT 列出：

- 每個測試案例
- 預期值
- 實際值
- 誤差
- PASS／FAIL

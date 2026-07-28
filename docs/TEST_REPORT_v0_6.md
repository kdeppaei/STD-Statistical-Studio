# STD Statistical Studio v0.6 — TEST REPORT

## 測試摘要

- 測試日期：2026-07-28
- 測試標的：`std_statistical_studio_v0_6.html`
- 測試方式：內建 Statistical Self-test、JavaScript syntax check、Chromium 實際互動測試、視覺檢查、靜態完整性檢查。
- 內建數值測試：18 PASS / 0 FAIL
- 瀏覽器 console：0 error / 0 warning
- 測試 tolerance：`1e-8`

## Statistical Self-test

| ID | 測試 | 預期值 | 實際值 | 絕對誤差 | 結果 |
|---|---|---:|---:|---:|---|
| mean_001 | Mean | 2.5 | 2.5 | 0 | PASS |
| sd_001 | Sample SD | 1 | 1 | 0 | PASS |
| quantile_025 | Quantile 25% | 1.75 | 1.75 | 0 | PASS |
| quantile_075 | Quantile 75% | 3.25 | 3.25 | 0 | PASS |
| anova_f_001 | ANOVA F | 27 | 27 | 0 | PASS |
| anova_eta_001 | ANOVA eta squared | 0.9 | 0.9 | 0 | PASS |
| welch_anova_001 | Welch ANOVA F | 23.142857142857142 | 23.142857142857142 | 0 | PASS |
| one_sample_t_001 | One-sample t | 0.8660254037844386 | 0.8660254037844385 | 1.1102230246251565e-16 | PASS |
| pooled_t_001 | Pooled t | -3.6742346141747673 | -3.6742346141747673 | 0 | PASS |
| welch_t_001 | Welch t | -3.6742346141747673 | -3.6742346141747673 | 0 | PASS |
| paired_t_001 | Paired t | 4 | 4 | 0 | PASS |
| regression_slope_001 | Regression slope | 1.5 | 1.5 | 0 | PASS |
| regression_r2_001 | Regression R squared | 0.9642857142857143 | 0.9642857142857143 | 0 | PASS |
| cpk_001 | Cpk | 2.6805833333333333 | 2.6805833333333333 | 0 | PASS |
| ppk_001 | Ppk | 3.0192981992777086 | 3.0192981992777086 | 0 | PASS |
| imr_ucl_001 | I-MR individual UCL | 13.546099290780141 | 13.546099290780141 | 0 | PASS |
| xbar_r_ucl_001 | Xbar-R Xbar UCL | 5.046 | 5.045999999999999 | 8.881784197001252e-16 | PASS |
| pca_eigen_001 | PCA eigenvalue | 2 | 1.9999999999999998 | 2.220446049250313e-16 | PASS |

## 功能驗收

| 驗收項目 | 實際結果 | 結果 |
|---|---|---|
| 單一 HTML | 只有一個可直接開啟的應用 HTML；無後端、無 React/Vue | PASS |
| JavaScript syntax | 內嵌主程式 125,156 characters 通過 Node syntax check | PASS |
| Procedure Registry | 39 個具版本 Procedure；左側 10 類主選單由 Registry 生成 | PASS |
| 無大 switch | 靜態檢查找不到 `switch(state.activeProc)` | PASS |
| Inspector / Method Strip | roles、minimum requirements、assumptions、rule 由 Registry 生成 | PASS |
| 空資料 Validator | `data.overview` 顯示 Rejected，未產生圖表 | PASS |
| 示範資料 | 36 rows、3 numeric；資料總覽 Completed | PASS |
| Assumption Advisor | 12 組診斷表；Variance ratio、Brown-Forsythe、Q-Q 與警告正常輸出 | PASS |
| Method recommendation | deterministic recommendation 顯示推薦、信心、原因、替代方法與禁止推論 | PASS |
| Welch ANOVA | 12 組資料 Completed，輸出群組 n/mean/variance/weight 與 F/p/effect size | PASS |
| Tukey HSD | 12 組產生 66 組 pairwise comparisons 與 difference CI plot | PASS |
| Games-Howell | 12 組產生 66 組 pairwise comparisons 與 difference CI plot | PASS |
| Dunn + Bonferroni | 12 組產生 66 組 pairwise comparisons 與 adjusted p-value | PASS |
| exact group Validator | 12 組資料執行 pooled two-sample t-test 時顯示 Rejected；未畫圖 | PASS |
| Xbar-R | 子組 n=3；Completed；Canvas、limits 與 Nelson violations 正常 | PASS |
| I-MR | Completed；Individual 與 Moving Range 圖正常 | PASS |
| Nelson Rule Engine | Rules 1–6 有獨立 ID、符號、觸發點及 Result IR violations | PASS |
| R/MR 規則適用性 | R、MR 只檢查 Rule 1；避免套用不適用 run rules | PASS |
| Result IR | 包含 procedure id/version、engine、parameters、statistics、warnings、excluded rows | PASS |
| Audit Trail | 實際互動產生 12 筆 Audit Records；最後一筆具完整欄位與 result hash | PASS |
| LLM Prompt | 四條必要 guardrails 全部存在；明確禁止統計運算 | PASS |
| Responsive UI | 筆電寬度下分析畫面無右側裁切，Inspector 自動移至下方 | PASS |
| Browser console | error 0、warning 0 | PASS |

## 主選單測試

| 類別 | Procedure 數 | 展開／切換 | 結果 |
|---|---:|---|---|
| 資料準備 | 2 | 正常 | PASS |
| 統計顧問 | 3 | 正常 | PASS |
| 描述與分布 | 6 | 正常 | PASS |
| 群組比較 | 14 | 正常 | PASS |
| 關聯與迴歸 | 4 | 正常 | PASS |
| 製程與 SPC | 3 | 正常 | PASS |
| 多變量分析 | 3 | 正常 | PASS |
| STD／LLM | 2 | 正常 | PASS |
| 報告輸出 | 1 | 正常 | PASS |
| Developer | 1 | 正常 | PASS |

## 輸出頁籤測試

| 頁籤 | 驗證內容 | 結果 |
|---|---|---|
| STD JSON | schema、source、translator、records | PASS |
| Procedure Plan | procedure/version/category/roles/minimum/assumptions/outputs/validator/executor | PASS |
| Assumption Report | 群組診斷與警告 | PASS |
| Result IR | deterministic statistics 與 SPC violations | PASS |
| Audit Trail | 來源、參數、常數、警告、hash | PASS |
| LLM Prompt | 禁算與 schema-only guardrails | PASS |

## 已知數值差異說明

- IEEE-754 浮點誤差出現在 three cases，最大誤差 `8.881784197001252e-16`，遠低於 `1e-8` tolerance。
- Tukey／Games-Howell 尾機率採 deterministic studentized-range family-wise approximation；Dunn 採 tie-corrected normal approximation。這些方法、假設與限制會保留在輸出與 CHANGELOG，不以 LLM 補算或掩飾。

## 結論

v0.6 的規格驗收項目全部通過；數值 Self-test 為 18 PASS / 0 FAIL，瀏覽器功能與視覺測試未發現阻斷問題。

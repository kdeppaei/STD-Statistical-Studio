# Statistical Rules

## Deterministic execution

All reported statistical values are calculated by JavaScript in the browser. LLM output is not accepted as a source for p-values, capability indices, regression coefficients, PCA, control limits, or SPC violations.

## Validation

A Procedure must pass its Registry-defined variable roles and minimum requirements before execution. Rejected procedures do not draw an empty or misleading chart.

## Group comparison

- One-sample, pooled two-sample, Welch, and paired t-tests report uncertainty and effect size.
- One-way ANOVA reports sums of squares, degrees of freedom, mean squares, F, p-value, and eta squared.
- Welch ANOVA uses inverse-variance weights and Satterthwaite-style denominator degrees of freedom.
- Brown-Forsythe uses deviations from each group median.
- Mann-Whitney, Wilcoxon, and Dunn use rank calculations with tie handling.

## Post-hoc

- Tukey HSD and Games-Howell use a deterministic studentized-range family-wise approximation for adjusted p-values and simultaneous confidence intervals.
- Dunn uses Bonferroni-adjusted p-values.
- The current Tukey/Games-Howell approximation may differ from high-precision SAS or R implementations in the final decimal places.
- Current rank-test p-values use large-sample normal approximations rather than exact permutation distributions.

## Regression

Simple OLS reports coefficients, uncertainty, R², residual diagnostics, leverage, and Cook's distance screening. Regression and correlation never establish causality.

## Capability

- Cpk uses within-subgroup sigma estimated from `R-bar / d2`.
- Ppk uses the overall sample standard deviation.
- Specifications must come from user-provided or imported values.
- Capability interpretation must be accompanied by a process-stability warning.

## SPC

- I-MR uses `MR-bar / 1.128` for the individual-chart sigma estimate.
- Xbar-R uses subgroup constants `A2`, `D3`, and `D4`.
- Nelson Rules 1-6 are applied to Individual and Xbar charts.
- Moving Range and Range charts use only Rule 1 because run rules are not interpreted the same way on dispersion charts.

## Multiple testing and causal language

Adjusted p-values are required for post-hoc comparisons. Statistical significance is not narrated as machine, operator, material, or process causality without a design that identifies that effect.

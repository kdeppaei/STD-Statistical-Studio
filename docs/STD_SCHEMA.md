# STD Schema

STD Statistical Studio separates source labels from stable semantic identifiers.

## Core source mapping

| STD ID | Meaning | Typical source label |
|---|---|---|
| `production.lot_id` | Production lot | LOT, LOT NO. |
| `production.machine_id` | Machine identifier | 機台 |
| `sample.measured_at` | Measurement date/time | 日期 |
| `measurement.*` | Numeric measurement | 推力、拉力、厚度 |

The original source label remains available as a USER Label. The mapping layer must not invent units, LSL, USL, or Target values.

## Missing values

- Missing values remain missing.
- Missing numeric values are never converted to zero.
- Excluded rows are recorded with the source row number and reason in Result IR and Audit Trail.

## Result IR

Every execution records:

- engine and procedure versions
- status
- parameters
- assumption status
- deterministic statistics
- warnings
- excluded rows

## LLM boundary

LLM may suggest mappings and localize labels, but it may not calculate statistical values or alter deterministic results.

# Data Quality Report

- Rows: 30
- Columns: 6
- Variables analyzed: X1, X2, X3, X4, X5

## Schema

- `Resp`: `int64`
- `X1`: `int64`
- `X2`: `int64`
- `X3`: `int64`
- `X4`: `int64`
- `X5`: `int64`

## Structural Checks

- Missing values (all columns): 0
- Duplicate rows: 0
- Unique `Resp` IDs: True
- `Resp` equals 1..N exactly: True

## Range and Type Checks (`X1`-`X5`)

- `X1`: non_numeric=0, out_of_0_to_9=0, non_integer=0
- `X2`: non_numeric=0, out_of_0_to_9=0, non_integer=0
- `X3`: non_numeric=0, out_of_0_to_9=0, non_integer=0
- `X4`: non_numeric=0, out_of_0_to_9=0, non_integer=0
- `X5`: non_numeric=0, out_of_0_to_9=0, non_integer=0
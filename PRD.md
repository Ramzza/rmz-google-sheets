# Product requirements

## Outcome

Provide a command-line tool for reading and editing Google Sheets ranges.

## Requirements

- **PRD-001 - Read spreadsheet ranges:** Read the requested spreadsheet ID and A1 range and return its cell matrix, using an empty matrix when the API has no values.
  **Verification:** `tests/sheets.test.ts::PRD-001: reads the requested spreadsheet range as cell values`; `tests/sheets.test.ts::PRD-001: returns an empty matrix when a range has no values`.
- **PRD-002 - Validate and write cell values:** Accept only non-empty matrices of non-empty rows with scalar cells; updates use `USER_ENTERED` and appends use `USER_ENTERED` with `INSERT_ROWS`.
  **Verification:** `tests/cli.test.ts::PRD-002: accepts scalar cell values`; `tests/cli.test.ts::PRD-002: rejects invalid row data`; `tests/sheets.test.ts` tests prefixed `PRD-002`.

# rmz-google-sheets

A small command-line tool for reading and editing Google Sheets ranges.

## Setup

1. Enable the Google Sheets API in your Google Cloud project.
2. Configure Application Default Credentials. For a service account, set
   `GOOGLE_APPLICATION_CREDENTIALS` to its JSON key file and share the target
   spreadsheet with the service account's email address. Alternatively, use
   `gcloud auth application-default login`.
3. Install dependencies and build the CLI:

   ```sh
   npm install
   npm run build
   npm link
   ```

## Usage

Pass the spreadsheet ID from its URL and a Sheets A1 range:

```sh
rmz-sheets get SPREADSHEET_ID 'Sheet1!A1:C10'
rmz-sheets update SPREADSHEET_ID 'Sheet1!A1:B2' --values '[["Name", "Count"], ["Tea", 3]]'
rmz-sheets append SPREADSHEET_ID 'Sheet1!A:B' --values '[["Coffee", 5]]'
```

`--values -` reads a JSON array of rows from standard input:

```sh
printf '[["Coffee", 5]]' | rmz-sheets append SPREADSHEET_ID 'Sheet1!A:B' --values -
```

Updates use the Sheets API's `USER_ENTERED` mode, so values are interpreted as
if entered in the Google Sheets UI. Append inserts new rows after the existing
table. The tool does not store credentials or spreadsheet contents.

## Development

Run the unit tests with:

```sh
npm test
```

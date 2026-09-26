"""Google Sheets API operations."""

from collections.abc import Sequence
from typing import Any

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def build_service() -> Any:
    """Build an authenticated Sheets API service using Application Default Credentials."""
    import google.auth
    from googleapiclient.discovery import build

    credentials, _ = google.auth.default(scopes=SCOPES)
    return build("sheets", "v4", credentials=credentials, cache_discovery=False)


def get_values(service: Any, spreadsheet_id: str, range_name: str) -> list[list[Any]]:
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    return result.get("values", [])


def update_values(
    service: Any,
    spreadsheet_id: str,
    range_name: str,
    values: Sequence[Sequence[Any]],
) -> dict[str, Any]:
    return (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body={"values": values},
        )
        .execute()
    )


def append_values(
    service: Any,
    spreadsheet_id: str,
    range_name: str,
    values: Sequence[Sequence[Any]],
) -> dict[str, Any]:
    return (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": values},
        )
        .execute()
    )

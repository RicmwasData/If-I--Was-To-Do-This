import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_data(spreadsheet_id: str, range_name: str):  # Ensure parameters match expected usage
  """Fetches data from Google Sheets and returns a Pandas DataFrame."""
  SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "C:/Users/Ricmwas/Documents/python_projects/Ifiwastodothis/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=3000)

    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return pd.DataFrame()  # Return an empty DataFrame instead of None

    df = pd.DataFrame(values[1:], columns=values[0])  # Use values[0] as column names
    return df

  except HttpError as err:
    print(f"Error fetching data: {err}")
    return pd.DataFrame()  # Return an empty DataFrame on failure


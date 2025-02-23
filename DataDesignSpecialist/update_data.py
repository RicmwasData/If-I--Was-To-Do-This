import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def update_values(spreadsheet_id, range_name, dataframe):
    """
    Updates a Google Spreadsheet with the contents of a Pandas DataFrame.
    """
    creds = None
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "C:/Users/Ricmwas/Documents/python_projects/Ifiwastodothis/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=3000)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("sheets", "v4", credentials=creds)
        
        # Convert NaN values to string "NAN"
        dataframe = dataframe.fillna("NAN")
        # Convert DataFrame to list of lists
        values = [dataframe.columns.tolist()] + dataframe.values.tolist()
        
        
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


# Example DataFrame
# df = pd.DataFrame({
#     "Column1": ["A", "C"],
#     "Column2": ["B", "D"]
# })

# update_values(
#     "1G6spGBsLR86GSaWcXEPtF8bVi1A51w8DDcZqXK13tCI",
#     "Sheet10!A1",  # Adjust range as needed
#     df,
# )


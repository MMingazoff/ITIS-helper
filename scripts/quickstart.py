import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID_request_activ = '1qPCCiMbWs1EZaK3hNBHvpn86uNx8OmN7UpWSqfv6_jQ'
SAMPLE_SPREADSHEET_ID_du_active = '10AcN0Ygof1TLxuMlBXPK9m-I6vVxpqB5AulkEgw0mBc'
SAMPLE_SPREADSHEET_ID_raskraska = '1bPVQYgPnxienxyENTP1ApNTy4jj4Hbk_f43o5Jsp1Bs'
SAMPLE_RANGE_NAME_request_activ_with_range = '09.11.2021 - 31.03.2022!A1183:C1','04.05.2021 - 08.11.2021!A1188:C1'
SAMPLE_RANGE_NAME_request_activ = ['09.11.2021 - 31.03.2022','04.05.2021 - 08.11.2021']
SAMPLE_RANGE_NAME_du_active = 'Мероприятия'
SAMPLE_RANGE_NAME_raskraska_with_range =[ '1 курс!A1:O43','2 курс!A1:O43','3 курс!A1:L43','4 курс!A1:l43','Магистры!A1:X43']
SAMPLE_RANGE_NAME_raskraska = ['1 курс','2 курс','3 курс','4 курс','Магистры']
sheet = None
path = os.path.abspath(__file__)[:-21]
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('C:\ITIS-helper-1\scripts\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
    global sheet
    sheet = service.spreadsheets()
def download_request_activ():
        result_request_activ = []
        for SAMPLE in SAMPLE_RANGE_NAME_request_activ_with_range:
            result_request_activ.append(sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_request_activ,
                                        range=SAMPLE).execute())
        value_of_request_activ=[]
        for result in result_request_activ:
            value_of_request_activ.append(result.get('values', []))
        dataFrame_of_request_activ = []
        for value in value_of_request_activ:
            dataFrame_of_request_activ.append(pd.DataFrame(value))
        with pd.ExcelWriter(path +"data/request_active.xlsx") as writer:
            dataFrame_of_request_activ[0].to_excel(writer, sheet_name=SAMPLE_RANGE_NAME_request_activ[0], index=False, header=False)
        with pd.ExcelWriter(path +"data/request_active.xlsx", engine='openpyxl', mode='a') as writer:
            dataFrame_of_request_activ[1].to_excel(writer, sheet_name=SAMPLE_RANGE_NAME_request_activ[1], index=False, header=False)
def download_du_activ():    
        result_du_active = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_du_active,
                                    range=SAMPLE_RANGE_NAME_du_active).execute()
        values_du_active = result_du_active.get('values', [])
        df3_du_active = pd.DataFrame(values_du_active)
        with pd.ExcelWriter(path + "data/du_active.xlsx") as writer:
            df3_du_active.to_excel(writer, sheet_name = SAMPLE_RANGE_NAME_du_active, index=False, header=False)
def download_raskraska():
        result_raskraska=[]
        for SAMPLE in SAMPLE_RANGE_NAME_raskraska_with_range:
            result_raskraska.append(sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_raskraska,
                                        range=SAMPLE).execute())
        value_of_raskraska=[]
        for result in result_raskraska:
            value_of_raskraska.append(result.get('values', []))
        dataFrame_of_raskraska = []
        for value in value_of_raskraska:
            dataFrame_of_raskraska.append(pd.DataFrame(value))
        with pd.ExcelWriter(path + "data/raskraska.xlsx") as writer:
                dataFrame_of_raskraska[0].to_excel(writer, sheet_name=SAMPLE_RANGE_NAME_raskraska[0], index=False, header=False)    
        for dataframe,SAMPLE in zip(dataFrame_of_raskraska[1:],SAMPLE_RANGE_NAME_raskraska[1:]):
            with pd.ExcelWriter(path + "data/raskraska.xlsx", engine='openpyxl', mode='a') as writer:
                dataframe.to_excel(writer, sheet_name=SAMPLE, index=False, header=False)
    
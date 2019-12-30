from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SHEET_ID = '1boZJT_4ePXHZBbRs2_LLiUvZl-F6qZm8SDOkOMsPEAg'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

class Service():
    def __init__(self):
        self.creds = None
        self.SCOPES =['https://www.googleapis.com/auth/drive']
        self.getCred()
        self.service=build( 'sheets', 'v4', credentials = self.creds)
    def getCred(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
    def addPurchaseRequest(self):
        title =self.getTitle()
        spreadsheet = {'properties': {'title': title}}
        spreadsheet = self.service.spreadsheets().create(body=spreadsheet,fields='spreadsheetId').execute()
        print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
    def getTitle(self):
        return  str(datetime.date.today().year) +"-"+ str(datetime.date.today().month) +"-"+ str(datetime.date.today().day)
    def addItem(self):
        list = [['Item'], ['Price'], ['Quantity'],['Cost'],['Link']]
        resource = { "majorDimension": "COLUMNS", "values": list }
        range = "A1:E1";
        request = self.service.spreadsheets().values().append(spreadsheetId=SHEET_ID,
            range=range,
            body=resource,
            valueInputOption="USER_ENTERED").execute()

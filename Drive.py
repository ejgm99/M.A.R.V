from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from bs4 import BeautifulSoup as bs
import json

WebContentID = '1YgCNWrbxPUT9bGaNzVYjY0i6itJj1_Hi'
PurchasesID = '14WmsBbl2sbo0ctoGiPPR3Pom-h4PisZz'
DocID = "1549ve2hXhNip_2ofl7MfybbPrkthd-HN"
BigDocID = "1OVgaYiZkLOOzfYxjhm1pf3O2Rm3SsxYViYg7JIHQjco"

class Service:
    def __init__(self):
        self.creds = None
        self.SCOPES =['https://www.googleapis.com/auth/drive']
        self.getCred()
        self.service=build( 'drive', 'v3', credentials = self.creds)
    def getCred(self):
        # flow = InstalledAppFlow.from_client_secrets_file(
        #     'credentials.json', self.SCOPES)
        # self.creds = flow.run_local_server(port=0)
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                print("token not working, trying credentials file")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = build('drive', 'v3', credentials=self.creds) #used in setup to get permission to access google drive
    def MassEdits(self, ids, field, Editor): #edits should take in a service, and ids at the minimum
        for id in ids:
            self.EditField(id[1], 'name', Editor(id[0]))
    def EditField(self, id, field, replacement = None, Editor = None):
        untitled = self.service.files().get(fileId = id,fields=field).execute()
        if Editor:
            untitled[field] = Editor(untitled[field]).out
        if replacement:
            untitled[field] = replacement
        self.service.files().update(fileId = id, body = untitled).execute()
    def getChilds(self, id):#returns id and title of every child in a drive
        out = []
        rChildren = self.service.files().list(q="'"+id+"' in parents", fields='files(id, name, parents)').execute()
        for item in rChildren['files']:
            results = self.service.files().get(fileId = item['id']).execute()
            out = out + [(results['name'],results['id'])]
        return out
    def allChilds(self, id):#goes through every folder in drive file given by id
        out = [];
        for folder in self.getChilds(id): #looks through all children
            out = out + self.getChilds(folder[1])
        return out;
    def getDocHTML(self, id): #returns html of content of google doc by id and saves to a file
        request = self.service.files().export_media(fileId=id, mimeType='text/html').execute().decode("utf-8")
        title = self.service.files().get(fileId = id, fields ="name").execute()['name']
        soup = bs(request,features="html.parser")
        pretty = soup.prettify()
        HTML = open("doc_html/"+title,"w")
        HTML.write(pretty)
        HTML.close()
        return "doc_html/"+title

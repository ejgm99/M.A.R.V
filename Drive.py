from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def MassEdits(service, ids, edits): #edits should take in a service, and ids at the minimum
    for id in ids:
        edits(service, id[1], id[0], NumerifyTitle)

def EditTitles(service, id, title, editor):
    replacement = editor(title);
    untitled = service.files().get(fileId = id,fields='name').execute()
    untitled["name"] = replacement
    service.files().update(fileId = id, body = untitled).execute()



def DriveLS(service, id):
    out = []
    rChildren = service.files().list(q="'"+id+"' in parents", fields='files(id, name, parents)').execute()
    for item in rChildren['files']:
        results = service.files().get(fileId = item['id']).execute()
        out = out + [(results['name'],results['id'])]
    return out

def BigDriveLS(service, id):
    out = [];
    for folder in DriveLS(service, id):
        out = out +DriveLS(service, folder[1])
    return out;

def getDocHTML(service, id):
    request = service.files().export_media(fileId=id, mimeType='text/html').execute().decode("utf-8")
    title = service.files().get(fileId = id, fields ="name").execute()['name']
    soup = bs(request,features="html.parser")
    pretty = soup.prettify()
    HTML = open(title,"w")
    HTML.write(pretty)
    HTML.close()
    return title


def sendData(data):
    url = "http://127.0.0.1:8000/uploads/components/"
    poster = requests.session()
    poster.get(url)
    csrftoken = poster.cookies['csrftoken']
    j = json.dumps(data)
    d = json.loads(j)
    payload = {'csrfmiddlewaretoken': csrftoken, 'd' : j,}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    p = poster.post(url, data = payload, json = j)

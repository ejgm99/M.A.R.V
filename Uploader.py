import requests,json

class Uploader:
    def __init__(self,url):
        self.poster = requests.session()
        self.poster.get(url)
        self.csrftoken = self.poster.cookies['csrftoken']
    def sendData(self, url, data):
        j = json.dumps(data)
        d = json.loads(j)
        payload = {'csrfmiddlewaretoken': self.csrftoken, 'd' : j,}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        p = self.poster.post(url, data = payload, json = j)

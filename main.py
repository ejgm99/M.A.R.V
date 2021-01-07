import Drive
import Sheets
from HTML_Editor1 import HTMLParser
import Uploader
import HTML_Editor

WebContentID = '1YgCNWrbxPUT9bGaNzVYjY0i6itJj1_Hi'
PurchasesID = '14WmsBbl2sbo0ctoGiPPR3Pom-h4PisZz'
DocID = "1OVgaYiZkLOOzfYxjhm1pf3O2Rm3SsxYViYg7JIHQjco"
TestID = "17hOXCgzzCd-dE6CXHbf2U-ltyjrbT8MyN05g0zDU-aQ"
url = "http://127.0.0.1:8000/uploads/inventory/"
#url  = "http://blasterhackers.com/uploads/components/"
inventoryURL = "http://blasterhackers.com/uploads/inventory/"
SHEET_ID = '1boZJT_4ePXHZBbRs2_LLiUvZl-F6qZm8SDOkOMsPEAg'
BigDocID = "1hczIuBEJMP3E4vvdV91h87LrBtnE-w-xUUXqDqPALnc"

purchases2018ID = '1O7ZQ5BRnesuut6zHC1TwllNJIXXihq0b'
purchases2019ID = '1YvRyPvyZe4nIKireP68Nz5QhWL4dYnbu'

u = Uploader.Uploader(url)
d = Drive.Service()
h = HTMLParser()
s = Sheets.Service()


def main():
    # h.parseDoc("samples/Test File.html")
    title = d.getDocHTML(BigDocID)
    # data = HTML_Editor.parseDoc(title)
    docs = d.getChilds(PurchasesID)
    # updateContent(WebContentID)
    # s = Sheets.Service()

def individualTest():
    file_name = d.getDocHTML("1bgD38YbS3znMUDBJpgLFQ1hTg8VnTjNehmZkh0JZiCM")
    content = HTML_Editor.parseDoc("doc_html/Dream Orb")
    for c in content:
        u.sendData(url, c)

def updateContent(folder_id): #this function takes a folder ID and dumps the content on to a website
    docs = d.getChilds(folder_id)
    # content = HTML_Editor.parseDoc("doc_html/Dream Orb")
    for doc in docs:
       print("Parsing: "+doc[0])
       file_name =d.getDocHTML(doc[1])
       content = h.parseDoc(file_name)
       for component in content:
           u.sendData(url,component)
       # for c in content:
       #     u.sendData(url, c)

def getInventoryData():
    purchases2018 = d.getChilds(purchases2018ID)
    purchases2019 = d.getChilds(purchases2019ID)
    purchases = list(purchases2018.values())+list(purchases2019.values())
    #every row of the purchases will be an item, so we need to upload for every item in the spreadsheets
    #might be good to upload large json objects that contain each spreadsheet id
    for purchase in purchases:
        item_info = s.readItems(purchase,'A2:E')
        items_in_sheet = [] #we're going to be uploading items sheet by sheet
        for item in item_info:
            if notToBeIgnored(item):
                items_in_sheet = items_in_sheet+ [getDictFromSheetRow(item)]
        u.sendData('http://127.0.0.1:8000/uploads/inventory/', items_in_sheet)

getInventoryData()

def getDictFromSheetRow(item):
    item_dict = {}
    item_dict['name'] = item[0]
    item_dict['link'] = item[4]
    item_dict['quantity'] = item[2]
    return item_dict

def notToBeIgnored(item):
    try:
        if len(item[4])>5:
            return True
        if item[0] not in ignoredNames:
            return True
    except:
        print(item)
        return False
    return False

purchases2018 = d.getChilds(purchases2018ID)
purchases2019 = d.getChilds(purchases2019ID)
purchases = list(purchases2018.values())+list(purchases2019.values())
#every row of the purchases will be an item, so we need to upload for every item in the spreadsheets
#might be good to upload large json objects that contain each spreadsheet id


for purchase in purchases:
    item_info = s.readItems(purchase,'A3:E')

d1 = getDictFromSheetRow(item_info[0])
d2 = getDictFromSheetRow(item_info[1])
dd = [d1,d2]

import json

json_string = json.dumps(dd)
d = json.loads(json_string)
d
# item_info = s.readItems(purchases[0],'A3:E')
# item_infoLast =  s.readItems(purchase,'A3:E')
# item_info[0][0]
# item_info[0][4]
if __name__ == '__main__':
    main()

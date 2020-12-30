import Drive
import Sheets
from HTML_Editor1 import HTMLParser
import Uploader
import HTML_Editor

WebContentID = '1YgCNWrbxPUT9bGaNzVYjY0i6itJj1_Hi'
PurchasesID = '14WmsBbl2sbo0ctoGiPPR3Pom-h4PisZz'
DocID = "1OVgaYiZkLOOzfYxjhm1pf3O2Rm3SsxYViYg7JIHQjco"
TestID = "17hOXCgzzCd-dE6CXHbf2U-ltyjrbT8MyN05g0zDU-aQ"
url = "http://127.0.0.1:8000/uploads/components/"
#url  = "http://blasterhackers.com/uploads/components/"
SHEET_ID = '1boZJT_4ePXHZBbRs2_LLiUvZl-F6qZm8SDOkOMsPEAg'
BigDocID = "1hczIuBEJMP3E4vvdV91h87LrBtnE-w-xUUXqDqPALnc"

u = Uploader.Uploader(url)
d = Drive.Service()
h = HTMLParser()

def main():
    # h.parseDoc("samples/Test File.html")
    title = d.getDocHTML(BigDocID)
    # data = HTML_Editor.parseDoc(title)
    docs = d.getChilds(WebContentID)
    updateContent(WebContentID)
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



if __name__ == '__main__':
    main()

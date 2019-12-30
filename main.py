import Drive
import Sheets
import HTML_Editor
import Uploader

WebContentID = '1YgCNWrbxPUT9bGaNzVYjY0i6itJj1_Hi'
PurchasesID = '14WmsBbl2sbo0ctoGiPPR3Pom-h4PisZz'
DocID = "1OVgaYiZkLOOzfYxjhm1pf3O2Rm3SsxYViYg7JIHQjco"
TestID = "17hOXCgzzCd-dE6CXHbf2U-ltyjrbT8MyN05g0zDU-aQ"
url = "http://127.0.0.1:8000/uploads/components/"
SHEET_ID = '1boZJT_4ePXHZBbRs2_LLiUvZl-F6qZm8SDOkOMsPEAg'

def main():
    u = Uploader.Uploader(url)
    d = Drive.Service()
    s = Sheets.Service()
    # for content in HTML_Editor.parseDoc(d.getDocHTML(TestID)):
    #     u.sendData(url,content)

if __name__ == '__main__':
    main()

from bs4 import BeautifulSoup as bs
import json


def isTitle(span):
    if span.attrs['style'][(span.attrs['style'].find("font-weight:")+12):][0]=='7': #checking font weight to see if it's in bold
        print(span.attrs)
    return span.attrs['style'][(span.attrs['style'].find("font-weight:")+12):][0]=='7'
def addImageText(src,style, isBeginning):
    txt = '</p><img src="'+src+'"class="center" style="'+style+'"><p>'
    if isBeginning:
        txt = txt+'<p>'
    return txt
def addLinkText(link, text):
    out = '<a href="'+link+'">'+text+'</a>'
    return out
def format(str): #formats  what?
    str = str.replace("\n", "")
    str = str.strip()
    str = " "+str
    return str

def parseDoc(fileName): #webscraping done on exported google doc to upload to webserver
    print("--- Now parsing: '"+fileName+"' ---")
    html = open(fileName, "r")
    soup = bs(html,features="html.parser")
    spans = soup.body.find_all("span")
    ps = soup.body.find_all("p")
    contents = []
    content = {}
    content['title'] = ''
    text = ""
    content['text'] = text
    url_dict = {}
    img_dict = {}
    img_no = 1
    for span in spans:
        if len(span.contents)==3:
            if (span.img):
                src = span.img['src']
                style= span.img['style']
                text = text+addImageText(src, style,len(text))
            if (span.a):
                link = span.a['href']
                text = text + addLinkText(link,format(span.a.contents[0]))
                url_dict[format(span.a.contents[0]).strip()]=link
        else:
            if(isTitle(span)):
                if(len(content['title'])!=0):
                    content['urls'] = url_dict
                    content['images'] = img_dict
                    content['text'] = text
                    content['project'] = fileName
                    contents = contents+ [content.copy()]
                    content['text'] = ""
                    text = ""
                    url_dict = {}
                    img_dict = {}
                    img_no =1
                content['title'] = format(span.contents[0])
            else: #this is where main body text is parsed?
                tex = format(span.contents[0])
                if(len(tex)>1):
                    text = text +"<br>"+ tex
                print(text)
    text = format(text)
    content['urls'] = url_dict
    content['images'] = img_dict
    content['text'] = text
    content['project'] = fileName
    contents = contents+ [content]
    return contents

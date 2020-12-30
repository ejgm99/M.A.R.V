from bs4 import BeautifulSoup as bs
import json


def isTitle(span):
    try:
        if (span.attrs['style'][(span.attrs['style'].find("font-weight:")+12):][0]=='7'): #checking font weight to see if it's in bold
            if (span.contents[0]!='\n'): #checking to make sure it's not just a bolded enter
                return True
    except:
        return False

def addImageText(src,style):
    txt = '</p><img src="'+src+'"class="center" style="'+style+'"><p>'
    return txt

def addLinkText(link, text):
    out = '<a href="'+link+'">'+text+'</a>'
    return out

def format(str): #formats incoming text to nice readable format
    str = str.replace("\\n", "")
    str = str.strip()
    str = " "+str
    return str

def parseDoc(fileName): #webscraping done on exported google doc to upload to webserver
    print("\n--- Now parsing: '"+fileName+"' ---")
    print("\n\n\n")
    html = open(fileName, "r")
    soup = bs(html,features="html.parser")
    spans = soup.body.find_all("span") #Google Docs as html are just a bunch of spans that we'll be able to parse
    print(spans)
    print("\n\n\n")
    components = splitSpansByTitle(spans)
    data = []
    content = {}
    print(components)
    print("\n\n\n")
    for component in components:
        text = parseSpans(component[1],fileName[9:]) #parse spans for text data
        if component[0]=="":
            content['title']=fileName[9:]
        else:
            content['title'] =component[0]
        print("\n\n\nAdding title:  ",content['title'])
        content['text']=text;
        print("With text:  ", content['text'])
        content['project']=fileName[9:]
        print("To project:  ", content['project'])
        data =data+[content.copy()]
    print("\n\n\n\n")
    print(data)
    return data #this returns a data


def isImgOrHref(span):#identifies hyperlinks or images
    print("Testing if img or link",len(span.contents)==3)
    return len(span.contents)==3

def parseImg(span):
    if (span.img):
        src = span.img['src']
        style = span.img['style']
        return addImageText(src, style)

def parseLink(span):
    link = span.a['href']
    text = addLinkText(link, format(span.a.contents[0]))
    return text

def splitSpansByTitle(spans):#splits spans up by bold faced fonts, which will split everything by a step in the components
    #this algorithm tries to keep the order of the spans the same
    components = [] #variable named components because of the nature of the paragraphs
    c =[];
    title = ""
    for span in spans:
        if isTitle(span):
            components = components+ [[title, c.copy()]]
            title = format(span.contents[0])
            c=[]
        else:
            c= c+[span]
    components = components + [[title, c.copy()]]
    return components

def parseSpans(spans, t): #parses all the spans of a file and returns the content in a dictionary
    title=t[9:]
    text = ""
    added_link = False
    spans[0]
    for span in spans:
        if isImgOrHref(span): #check for images or linked text to add
            if (span.img):
                imageAdded = True
                text = text + parseImg(span)
            if (span.a):
                text = text + parseLink(span) #if there's a linked text, do not put in a page break
                added_link = True
        else:
            if (len(span.contents[0]))>1: #if the span contains a lot of text
                if added_link: #if a link's just been added, do not create a new line
                    added_link = False
                    text = text+format(span.contents[0])
                text = text +"<br>"+ format(span.contents[0]) #add new line for new collection of text
    return text[4:]

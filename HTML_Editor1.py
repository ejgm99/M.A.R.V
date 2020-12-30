from bs4 import BeautifulSoup as bs
import json

textFontWeight = 400; #allowed font weight for something to be just text

class HTMLParser:
    def __init__(self):
        self.titleFound=0;
        self.docContent =[]
        self.componentText = ""

    def parseDoc(self,fileName): #webscraping done on exported google doc to upload to webserver
        self.titleFound=0;
        print("\n--- Now parsing: '"+fileName+"' ---")
        projectTitle = fileName[9:]
        print("\n\n\n")
        html = open(fileName, "r")
        soup = bs(html,features="html.parser")
        spans = soup.body.find_all("span") #Google Docs as html are just a bunch of spans that we'll be able to parse
        component = {'project':projectTitle}
        componentBody=""
        docContent=[]
        for span in spans:
            if self.isImage(span):
                componentBody= componentBody + self.parseImage(span)
            elif self.isLink(span):
                componentBody= componentBody + self.parseLink(span)
            elif self.isTitle(span):
                #if we find a title we need to pack up all we have found so far and send it off
                component['text']=componentBody
                if len(docContent)==0:#if we haven't added anything to the document, then we've just parsed the description/picture for project
                    component['title']=component['project']
                else: #
                    component['title']=title
                docContent = docContent+[component]
                title=self.parseTitle(span) #lets grab the title for the next time we need to add a component to the list
                component = {'project':projectTitle} #and reitinalyze the component
                componentBody=""
            elif self.isText(span):
                componentBody= componentBody + self.parseText(span)
        #if we just finished going through all the spans, we probably didn't find a new title
        component['text']=componentBody
        component['title']=title
        docContent = docContent+[component]
        for component in docContent:
            print(component)
        return docContent

    def isImage(self,span):
            return len(span.find_all('img'))==1

    def isLink(self,span):
            return len(span.find_all('a'))==1

    def isTitle(self,span):
            try:
                style= span.attrs['style']
                fontweight = self.getAttribute(style, "font-weight:")
                if int(fontweight) >textFontWeight:
                    if len(span.contents[0].replace('\n',''))>0:
                        return True
                return False
            except(KeyError):
                return False

    def isText(self,span):
            try:
                style= span.attrs['style']
                fontweight = self.getAttribute(style, "font-weight:")
                if int(fontweight) ==textFontWeight:
                    return True
                return False
            except(KeyError):
                return True

    def parseImage(self,span):
        src = span.img['src']
        style = span.img['style']
        imageText = self.addImageText(src, style)
        print("This is an image",imageText[:100])
        return imageText

    def addImageText(self,src,style):
        txt = '<br /> <img src="'+src+'" class="center" style="'+style+'"><br />'
        return txt

    def parseLink(self,span):
        link = span.a['href']
        text=span.a.contents[0]
        text = text.replace('\n', "")
        linkText = self.addLinkText(link,text)
        print("This is a link", text, linkText[70:])
        return linkText

    def addLinkText(self, link, text):
        txt = '<a href"'+link+'"> '+text +' </a>'
        return txt

    def parseTitle(self,span):
        title = span.contents[0].replace('\n','')
        print("This is a title",title)
        return title

    def parseText(self,span):
        text =  span.contents[0].replace('\n',"")
        print("This is just text",text[:50])
        return text

    def getAttribute(self,string,label):
            string = string[string.find(label)+len(label):]
            string = string[:string.find(';')]
            return string;

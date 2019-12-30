
class NumerifyTitle: #String editor that takes a title and returns a numerifyied title
    def __init__(self,title):
        print("----------"+title+"----------")
        title = title.replace('/','-')
        title = title.replace(' ','')
        title = title.replace(',','-')
        title = title.replace('18','2018')
        title = title.replace('19','2019')
        title = self.MonthNameToNumber(title)
        for c in title:
            if c>'9':
                title = title.replace(c,'')
        date = title.split("-")
        print(date)
        out = ""
        noYear=True
        for n in date:
            if len(n)>3:
                if len(n)==6:
                    n = n[2:]
                out = n+out
                noYear = False
            else:
                out = out +"-"+ n
        if noYear:
            out = "2018"+out
        self.out = out
    def MonthNameToNumber(self, title):
        title = title.replace('January','1-')
        title = title.replace('February','2-')
        title = title.replace('Febuary','2-')
        title = title.replace('March','3-')
        title = title.replace('April','4-')
        title = title.replace('May','5-')
        title = title.replace('June','6-')
        title = title.replace('July','7-')
        title = title.replace('August','8-')
        title = title.replace('September','9-')
        title = title.replace('October','10-')
        title = title.replace('November','11-')
        title = title.replace('December','12-')
        return title

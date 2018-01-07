__author__ = 'RIJENS'
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag =='a':
            for(key,value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links =self.links + [newUrl]


    def getLinks(self,url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString,self.links
        else:
            return "",[]

    def spider(url1,url ,word, maxPages):
        pagesToVisit = [url]
        numberVisit = 0
        foundWord = False
        i = 3
        for  x in range(0,3):
            print ("x is ", x) 
            print ("pagesToVisit ", x," ", pagesToVisit)
            print ("foundWord ", x, " ", foundWord)
            
            while numberVisit < maxPages and pagesToVisit != [] and  foundWord == False:
                numberVisit= numberVisit +1
                url = pagesToVisit[0]
                pagesToVisit = pagesToVisit[1:]
                try:
                    print(numberVisit,"Visiting : " , url)
                    parser = LinkParser()
                    data, links = parser.getLinks(url)
                    if data.find(word) > -1:
                        foundWord = True
                    pagesToVisit = pagesToVisit + links
                    print("*Success*")
                    print(pagesToVisit)
                except Exception as ex:
                    print("*Failed*")
                    print(ex)
        if foundWord:
            print("*The Word, " , word , "was found at", url)
                
        else:
            print("Word never found")


if __name__ == '__main__':
    LinkParser().spider("http://www.dreamhost.com","secure",3)

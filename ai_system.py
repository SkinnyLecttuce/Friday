import os
import wolframalpha
import wikipedia
import webbrowser
import urllib.request
import urllib.parse
import re
from requests import get
#import ai_intent_recognizer


class System():
    def __init__(self):
        self.music_path = '\\Music\\'
        self.file_path = ''
        self.key = "4TPUQH-VUJU54TPXK"
        self.chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        self.list_music_dir = os.listdir(self.music_path)

    def call(self,command):
        r = os.system(command)
        print(self.list_music_dir)
        return r

    def browser_video(self,url,mode):
        if(mode == 'auto'):
            webbrowser.open("http://www.youtube.com/watch?v={}".format(url))
            return 0
        if(mode == 'manuel'):
            webbrowser.open("https://www.youtube.com/results?search_query={}".format(url))

    def video(self,text,mode):
        print("video search")
        if(mode == 'auto'):
            query_string = urllib.parse.urlencode({"search_query": text})
            html_content = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query_string)
            strs = html_content.read().decode()
            p = re.compile(r'"videoId":(.*),')
            match = p.search(str(strs))
            g = ''
            if (match):
                g = match.group(1)
                for gs in g.split(','):
                    g = gs
                    break
            search_results = g
            p = re.compile(r'"(.*)"')
            match = p.search(str(search_results))

            if (match):
                g = match.group(1)

            search_results = g
            self.browser_video(search_results,'auto')

        elif(mode == 'manuel'):
            self.browser_video(text,'manuel')

    def play(self,f,entity):
        r=1
        c = re.compile(r'"(.*)"')
        match = c.search(f[0])
        if(match):
            g = match.group(1)
            print("Video_input:",g)
            if(entity['WORK_OF_ART'] == 'None'):
                entity['WORK_OF_ART'] = g

        print('saving:',entity,f)
        if(f[0]=='-'):
            print("r is 1")
            if(entity['WORK_OF_ART']=='None'):
                return 1
            else:
                self.video(entity['WORK_OF_ART'], 'auto')
                return 0

        for files in self.list_music_dir:
            print('files:',files,f[0])
            if(f[0].lower() in files.lower()):
                r=self.call('start '+self.music_path + files)
                break
        print("r is",r)

        if(r==1):
            print("r is 1")
            if (entity['WORK_OF_ART'] == 'None'):
                return 1
            else:
                self.video(entity['WORK_OF_ART'], 'auto')
                return 0

    def open(self,f):
        return self.call('start '+self.file_path + f[0])

    def book(self,f,entity):
        print('booking',f,entity)
        return entity

    def open_browser(self,text,returns):
        url_ = ''
        for texts in text.split(' '):
            url_ =url_+texts+'+'
        url_created = 'https://www.google.com/search?q='+url_
        print("URL:",url_created)
        if(returns == 'url'):
            return url_created
        else:
            webbrowser.get(self.chrome_path).open(url_created)
            return 0

    def browser(self,text):
        r=''
        rr = ''
        try:
            rr=self.open_browser(text,'url')
            client = wolframalpha.Client(self.key)
            output = client.query(text)
            r = next(output.results).text
            print('rr is',rr,text)
            r = r+'\n'
        except:
            try:
                rr=self.open_browser(text,'url')
                r= wikipedia.summary(text, sentences=5)
                print('rr is',rr,text)

            except Exception as error:
                    pass
        print("GOOOGS")
        url = "https://www.google.com/search?q={0}".format(text)
        raw = get(url).text
        s = raw
        result = re.search(
            '<div><div class="BNeawe s3v9rd AP7Wnd"><div><div><div class="BNeawe s3v9rd AP7Wnd">(.*)</div></div></div></div></div></div></div></div><div><div class="ZINbbc xpd O9g5cc uUPGi">',
            s)
        r = 'Found Some Results:\nGoogle Says:\n'+result.group(1).split('<')[0]+'\nInternet Says:\n'+r
        print("GOOGS SCRAPE:", r)
        r = r + '\nMore Details For From Google ' + text + ' :' + rr
        print("GOOGS SAID:", r)
        return r

    def Execute(self,action,entity,text,intent_model,intent_model_build2):
        r=0
        if(action == 'system.play'):
            r=self.play(text,entity)

        if(action == 'system.open'):
            r=self.open(text)

        if(action == 'system.book.flight'):
            r=self.book(text,entity)

        if(action == 'system.book.hotel'):
            r=self.book(text,entity)

        if(action == 'system.rate.book'):
            r=self.book(text,entity)

        if(action == 'system.browser'):
            r=self.browser(text)

        return r

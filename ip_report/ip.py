import web
import os
import time, datetime

urls = (
    '/getip/(.*)', 'getip',
    '/report/(.*)', 'report'
    '/upper_html/(.*)', 'upper_html',
    '/(js|css|images)/(.*)', 'static'
)

app = web.application(urls, globals())
render = web.template.render('templates/')
class upper_html:
    def GET(self, text):
        print('input:' + text)
        return render.hello(content=text.upper())

class static:
    def GET(self, media, file):
        try:
            f = open(media+'/'+file, 'rb')
            return f.read()
        except:
            return ''

class getip:
    def GET(self, text): 
        list = []  
        render=web.template.render("templates")
        return render.index('1','2','2') 

class report:
    def GET(self, text):
        #print('input:' + text) 
        nf = open("ip.txt", "w")
        localtime = time.asctime( time.localtime(time.time()) )
        nf.write(text+"__"+localtime)
        nf.close()  
        return text.lower()

if __name__ == "__main__":
    app.run()

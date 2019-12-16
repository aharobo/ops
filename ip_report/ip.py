import web
import os
import time, datetime
urls = (
    '/getip/(.*)', 'getip',
    '/report/(.*)', 'report'
)
app = web.application(urls, globals())
class getip:
    def GET(self, text): 
        list = [] 
        with open('ip.txt', 'rt', encoding='utf-8') as f:
            for line in f:
                list.append(line) 
        ipss=list[0].split("__")
        print(ipss) 
        render=web.template.render("templates")
        return render.index(ipss[1],ipss[2],ipss[0]) 

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

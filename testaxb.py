import web
import os,json,time
import sqlite3
import base64 
import hashlib
from urllib.parse import unquote,quote
import requests
import json
     
urls = (  
    '/test/test', 'test',
    '/test/testbind', 'testbind',
    '/test/testunbind', 'testunbind', 
    '/test/testaxbbind', 'testaxbbind', 
    '/static/(js|css|images)/(.*)', 'static'
)

app = web.application(urls, globals())
render = web.template.render('templates/')
web.internalerror = web.debugerror  
web.config.debug = False


'''

测试登录
https://developer.7moor.com/data-query/
bjhqht1  4007Wyjv

鉴权
https://developer.7moor.com/v2docs/authorization/

小号
https://developer.7moor.com/dc/#/callCenter/rlSmall


AXB1 
http://m.aharobo.com:8080/test/testaxbbind?midNum=17082753730&called=17150195294&caller=18610980110

AXB2 
http://m.aharobo.com:8080/test/testaxbbind?midNum=17082753730&called=17150145148&caller=18610980110

test unbind xb http://m.aharobo.com:8080/test/testunbind?midNum=17082753730&mappingId=NME201a4467500b53011eaae0765c4cbac5fb5

test xb http://m.aharobo.com:8080/test/testbind?midNum=17082753730&called=18610980110
        http://m.aharobo.com:8080/test/testbind?midNum=17082753730&called=18610980110

axb 绑定到位测试X号 : 
http://m.aharobo.com:8080/test/testaxbbind?midNum=17082753730&called=13269986433&caller=18610980110


入:    到位用户->到位X号->恒通工匠小号->恒通工匠真实号   
出:    工匠APP中拨打->恒通工匠小号(同时改次工匠小号的指向到目标[到位X号]) -> 转向[到位X号]-> 转到[到位客户号码]

AXB 和XB互不影响 AXB只控制呼出方向;  指定呼出AXB情况下 XB也有效 ,即允许三方(其他的订单客户)打进来(到工匠),{我们可以控制小号与真实号连接}

'''

#QIAPI CONFIG

ACCOUNTID="N00000050185"
APISecret="993dabe0-b523-11ea-b6b0-f902e56dd391"
HOST="https://apis.7moor.com/"
PBX="bj.ali-hr.20.4"
proxy_url="https://pbx-bj-hr20.7moor.com"

class QIAPI:
    #company = 'LOL' 
    def getPramas():
        timest=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()));
        
        #Authorization
        Authorization = base64.b64encode((ACCOUNTID+":"+timest).encode("utf-8")).decode('utf-8')
        #SIG
        s1=ACCOUNTID+APISecret+timest
        b = s1.encode(encoding='utf-8')
        m = hashlib.md5()
        m.update(b)
        str_md5 = m.hexdigest()
        SIG=str_md5.upper() 
        return  {'Authorization': Authorization, "SIG":SIG} 

class test:
    def GET(self):
        args=web.input()   
        return QIAPI.getPramas()
        
class testaxbbind:
    def GET(self):
        args=web.input() 
        if not hasattr(args,'midNum') : 
            return "need midNum"
             
        midNum=args.midNum
        called=args.called
        caller=args.caller 
        
        prama=QIAPI.getPramas()
        Authorization=prama["Authorization"]
        SIG=prama["SIG"]
         
        print(Authorization,SIG)
        
        #
        #http://xxx.xxx.com/v20160818/rlxh/midNumBindForAXB/ACCOUNTID?sig=SIG
        call_url = HOST+"v20160818/rlxh/midNumBindForAXB/"+ACCOUNTID+"?sig="+SIG
        print(call_url,caller,"->",midNum,"->",called)
        
        #return "OK"+src+to
        
        body = {"midNum": midNum, "called": called,"caller":caller,"icDisplayFlag": "1", "needRecord": "true","expiration":0}
        headers = {'content-type': "application/json;charset=utf-8", 'Authorization': Authorization} 
        response = requests.post(call_url, data = json.dumps(body), headers = headers) 
        print (response.text) 
        print (response.status_code)
        
        #yyyyMMddHHmmss 
        return response.text
       
#xbbind       
class testbind:
    def GET(self):
        args=web.input() 

        if not hasattr(args,'midNum') : 
            return "need midNum"
             
        midNum=args.midNum
        called=args.called  
        
        
        prama=QIAPI.getPramas()
        Authorization=prama["Authorization"]
        SIG=prama["SIG"]
        
        print(Authorization,SIG)
        
        #
        call_url = HOST+"v20160818/rlxh/midNumBind/"+ACCOUNTID+"?sig="+SIG
        print(call_url)
        
        #return "OK"+src+to
        
        body = {"midNum": midNum, "called": called, "icDisplayFlag": "1", "needRecord": "true","expiration":0}
        headers = {'content-type': "application/json;charset=utf-8", 'Authorization': Authorization} 
        response = requests.post(call_url, data = json.dumps(body), headers = headers) 
        print (response.text) 
        print (response.status_code)
        
        #yyyyMMddHHmmss 
        return response.text
        
class testunbind:
    def GET(self):
        args=web.input() 
        if not hasattr(args,'mappingId') : 
            return "need mappingId"
        
        mappingId=args.mappingId
        midNum=args.midNum

        prama=QIAPI.getPramas()
        Authorization=prama["Authorization"]
        SIG=prama["SIG"]
      
        print(Authorization,SIG)
        
        #
        call_url = HOST+"v20160818/rlxh/midNumUnBinding/"+ACCOUNTID+"?sig="+SIG
        print(call_url)
        
        body = {"midNum": "17082753730", "mappingId": mappingId}
        headers = {'content-type': "application/json;charset=utf-8", 'Authorization': Authorization} 
        response = requests.post(call_url, data = json.dumps(body), headers = headers) 
        print (response.text) 
        print (response.status_code) 
         
        return response.text
        
class static:
    def GET(self, media, file):
        try:
            f = open(media+'/'+file, 'rb')
            return f.read()
        except:
            return ''
 
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

#!/usr/bin/python3  
# -*- coding: utf-8 -*-  
import time, datetime
import hashlib,sys
import urllib.parse
from urllib import request
from urllib import parse
from urllib.request import urlopen

def report_push_ip(ip,info):
 
    base_url='openapi.xg.qq.com/v2/push/account_list'


    timestamp=(str)((int)(time.time()))

    timenow=(str)(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    notify_str='IP:'+ip+',时间:'+timenow
    notify_title="树莓派上线 "+ip

    pramas = {'access_id' : '2100349591',
    'account_list':'["RASPI"]',  
    'environment':'2',
    'message':'{"content":"'+notify_str+'","title":"'+notify_title+'","vibrate":1}',
    'message_type':'1', 
    'timestamp' : timestamp,
    'valid_time':'600'}

    secret_key='c5dc6b03dbc3c27a6710ee03505aa105'

    prama_str='GET'+base_url
    prama_str_for_url=''
    for key in pramas.keys():
        prama_str+=key+'='+pramas[key]
        prama_str_for_url+='&'+key+'='+ urllib.parse.quote(pramas[key], safe='/', encoding=None, errors=None) 
    prama_str+=secret_key
    prama_str_for_url=prama_str_for_url[1:]



    sign = hashlib.md5(prama_str.encode(encoding='UTF-8')).hexdigest()

    print(prama_str,'的签名:',sign,"||",prama_str_for_url) 
    
    url="http://"+base_url+"?"+prama_str_for_url+"&sign="+sign
    return url


#推送IP更新通知
ip='';
if len(sys.argv)>1 :
    ip=sys.argv[1]
else:
    print ('参数不足')
 
print ( report_push_ip(ip,'ext_info') )
 

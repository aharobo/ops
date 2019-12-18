#!/usr/bin/python3  
# -*- coding: utf-8 -*-  
import time, datetime
import hashlib,sys
import socket, fcntl, struct,sys
import urllib.parse
from urllib import request
from urllib import parse
from urllib.request import urlopen 

	
def get_local_ip(ifname):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		r=socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15],'utf-8')))[20:24])
		return r
	except:
		r="0.0.0.0"
		return r 
	
def report_push_ip(ip,info):
 
	base_url='openapi.xg.qq.com/v2/push/account_list'


	timestamp=(str)((int)(time.time()))

	timenow=(str)(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	notify_str='IP:'+ip+',@'+timenow
	notify_title=info

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
	#print(prama_str,'的签名:',sign,"||",prama_str_for_url) 
	
	url="http://"+base_url+"?"+prama_str_for_url+"&sign="+sign
	return url

def print_color (info,color):
	print("\033[7;0;"+str(color)+"m "+info+" \033[0m")

def report_to_remote (ip,reason) :
	#Report to Aha
	url1="http://aharobo.com:8080/report/"   
	req = urllib.request.urlopen(url1+ip+"__"+reason)
	#print("\033[4;32;47m QWE \033[0m")
	r="[OK]"+str(req.getcode())+"Reported to aha :"+str(ip)
	print_color(r,44) 
	
	#PUSH
	url2= report_push_ip(ip,reason)
	#print (url2,ip,sys.argv[2])
	if(sys.argv[2] == 'true'):
		response = request.urlopen(url2,timeout=3)
		res = response.read().decode('utf-8').replace("\r\n","") 
		r="[OK] Push Done:"+str(res)
		print_color(r,33)

#推送IP更新通知
ip='';
retry_times=3
if len(sys.argv)>2 :

	#ARGS
	ip=sys.argv[1] 
	if ip=='auto': 
		for index in range(retry_times) : 
			#print(index) 
			if retry_times<1 :
				break  
			ip=get_local_ip('wlan0')  
			if ip=="0.0.0.0" :
				print("NoIP#WAIT "+str(index))
				time.sleep(2)
			else:
				reason="default" 
				#REASON
				if len(sys.argv)>3:
					reason=sys.argv[3]   
				#REPORT
				report_to_remote(ip,reason)
				break
else:
	print ('参数不足') 
  
 

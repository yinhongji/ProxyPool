#coding:utf-8
import requests
import re
import time
import threading

def init():
	#清空代理ip文件和可用ip文件
	filename1 = 'proxyip.txt'
	with open(filename1,'r+') as fp:
		fp.seek(0)
		fp.truncate()
	filename2 = 'avaip.txt'
	with open(filename2,'r+') as fp:
		fp.seek(0)
		fp.truncate()

def url_get():
	#通过xicidaili获取https代理池
	proxy_ip_list = []
	for page in range(1,10):
		url = 'https://www.xicidaili.com/wt/%s' % page
		#url = 'https://https://www.xicidaili.com/wn/%s' % page
		headers = {
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:67.0) Gecko/20100101 Firefox/67.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
		"Connection": "close",
		"Upgrade-Insecure-Requests": "1",
		"If-None-Match": "W/\"c310cc22feeda8c4f0c60843b62ea2b0\""
		}
		s = requests.get(url=url,headers=headers)
		proxylist = re.findall('<td>(.*?)</td>',s.text)
		
		filename = 'proxyip.txt'
		for i in xrange(0,len(proxylist)/5):
			ip , port , proxy_type , speed = proxylist[i*5] , proxylist[i*5+1] , proxylist[i*5+2] , proxylist[i*5+3] 
			append = ip + ':' + port
			proxy_ip_list.append(str(append))
			with open(filename,'a+') as fp:
				fp.write(append)
				fp.write('\r\n')
		time.sleep(1)
	return proxy_ip_list


def file_get():
	#通过文件获取https代理池
	filename = 'proxyip.txt'
	with open(filename,'r') as fp:
		return fp.readlines()


def ava(proxy_ip):
	#对https代理池做可用性检验
	url = 'http://www.baidu.com'
	proxies = {
	"http" : "http://%s" % proxy_ip.strip()
	#"https" : "https://%s" % proxy_ip.strip()
	}
	filename = 'avaip.txt'
	try:
		s = requests.get(url=url,proxies=proxies,timeout=3)
		
		if s.status_code == 200:
			print 'success : ' + proxy_ip
			with open(filename,'a+') as fp :
				fp.write(proxy_ip)
				fp.write('\r\n')
	except:
		print 'error : ' + proxy_ip
		pass



def main():
	init()
	try:
		proxy_ip_list = url_get()
		print 'url get done...'
	except:
		proxy_ip_list = file_get()
		print 'file get done...'

	proxy_ip_list = list(set(proxy_ip_list))

	available_list = []
	threads = []

	sem=threading.Semaphore(10)

	for x in proxy_ip_list:
		t = threading.Thread(target=ava,args=(x,))
		t.start()
	
if __name__ == '__main__':
	main()
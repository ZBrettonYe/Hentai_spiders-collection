from sys import argv
import requests,re,time,random
def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36','X-Forwarded-For':random_ip(),'referer':'http://91porn.com'}
url=argv[1]
video_url=[]
base_req=requests.get(url=url,headers=headers)
video_url=re.findall(r'<source src="(.*?)" type=\'video/mp4\'>',str(base_req.content,'utf-8',errors='ignore'))
print(video_url[0])
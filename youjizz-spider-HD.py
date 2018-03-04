import requests,re,json,os,random
import threading
class youjizz:
    def __init__(self):
        self.index_url='https://www.youjizz.com'
        self.cat_url='https://www.youjizz.com/highdefinition/'
    def cat_page(self,cat_id):
        return self.cat_url+str(cat_id)+'.html'
    def find_video_page(self,cat_page):
        req=requests.get(cat_page)
        page=[]
        page=re.findall(r'<div class="video-title"><a href=\'(.*?)\'>(.*?)</a>',req.text)
        return page
    def find_video_url(self,page):
        video_page=self.index_url+page
        req=requests.get(video_page)
        url=[]
        url=re.findall(r'var encodings = (.*?);',req.text)
        return json.loads(url[0])
    def download_video_del(self,video_url):
        for i in video_url:
            if i['quality']=='1080':
                return 'https:'+i['filename']
            elif i['quality']=='720':
                return 'https:'+i['filename']
def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))
def Handler(start, end, url, filename):
    headers = {'Range': 'bytes=%d-%d' % (start, end),'X-Forwarded-For':random_ip()}
    with requests.get(url, headers=headers,stream=True) as r:
        with open(filename, "r+b") as fp:
            fp.seek(start)
            var = fp.tell()
            fp.write(r.content)
def download(url,tittle, num_thread = 10):
    r = requests.head(url)
    try:
        file_name = tittle+'.mp4'
        file_size = int(r.headers['content-length'])
    except:
        print("检查URL，或不支持对线程下载")
        return
    fp = open(file_name, "wb")
    fp.truncate(file_size)
    fp.close()
    part = file_size // num_thread
    for i in range(num_thread):
        start = part * i
        if i == num_thread - 1:
            end = file_size
        else:
            end = start + part
 
        t = threading.Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url, 'filename': file_name})
        t.setDaemon(True)
        t.start()
 
    # 等待所有线程下载完成
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    print('%s 下载完成' % file_name)
                 
def main():
    start=youjizz()
    flag=1
    while flag<=2000:
        cat_url=start.cat_page(flag)
        print(cat_url)
        video_page_info=start.find_video_page(cat_url)
        for i in video_page_info:
            if os.path.exists(i[1]+'.mp4')==False:
                base_del=start.find_video_url(i[0])
                finally_del=start.download_video_del(base_del)
                print('开始下载，'+i[1])
                download(finally_del,i[1])
            else:continue
        print('此页已爬完，已爬了'+str(flag)+'页')
        flag+=1
            
if __name__=='__main__':
    try:
        main()
    except:
        sleep(1)
        main()
    

import requests,re,os
import threading,json
'''
1256开始规则变化
'''
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, url, dir, filename,headers):
        threading.Thread.__init__(self)
        self.threadID = filename
        self.url = url
        self.dir = dir
        self.filename=filename
        self.headers=headers
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        download_pic(self.url,self.dir,self.filename,self.headers)
def download_pic(url,dir,filename,headers):
    req=requests.get(url=url,headers=headers)
    if req.status_code==200:
        with open(dir+'/'+str(filename)+'.jpg','wb') as f:
            f.write(req.content)
class spider:
    def __init__(self):
        self.page='http://www.mmjpg.com/mm/'
        self.img='http://img.mmjpg.com/'
        self.file='.jpg'
    def del_main(self):
        flag=1
        while True:
            page_url=self.page+str(flag)
            headers={'Referer':page_url,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
            req=requests.get(page_url,headers=headers)
            if req.status_code==200:
                num_page=[]
                img_tittle=[]
                num_page=re.findall(r'picinfo = \[(.*?),(.*?),(.*?),(.*?)\];',req.text)
                img_tittle=re.findall(r'<h2>(.*?)</h2>',str(req.content,'utf-8'))
                if os.path.exists(str(img_tittle[0]))==False:
                    os.makedirs(img_tittle[0])
                    if num_page[0][3]=='0':
                        threads=[]
                        download_img=self.img+num_page[0][0]+'/'+num_page[0][1]+'/'
                        print('开始下载:'+img_tittle[0])
                        for i in range(1,int(num_page[0][2])+1):
                            download_img_url=download_img+str(i)+self.file
                            thread=myThread(download_img_url,img_tittle[0],str(i),headers)
                            thread.start()
                            threads.append(thread)
                        for t in threads:
                            t.join()
                        print('下载完成')
                    else:
                        data='http://www.mmjpg.com/data.php?id='+num_page[0][1]+'&page=8999'
                        req_data=requests.get(data,headers=headers)
                        names=req_data.text.split(',')
                        threads=[]
                        download_img=self.img+num_page[0][0]+'/'+num_page[0][1]+'/'
                        print('开始下载:'+img_tittle[0])
                        for i in range(1,int(num_page[0][2])+1):
                            download_img_url=download_img+str(i)+'i'+names[i-1]+self.file

                            thread=myThread(download_img_url,img_tittle[0],str(i),headers)
                            thread.start()
                            threads.append(thread)
                        for t in threads:
                            t.join()
                        print('下载完成')
                    print('已下载'+str(flag)+'套图片')
                    flag+=1
                else:
                    print('文件夹已存在，跳过')
                    flag+=1
                    continue
                    
            else:
                print('可能出现错误，或者已经爬完')
                break
            
def main():
    a=spider()
    a.del_main()
    
if __name__=='__main__':
    main()

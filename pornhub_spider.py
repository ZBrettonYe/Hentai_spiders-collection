from bs4 import BeautifulSoup as bs
import requests,re,os,urllib,sys
def download_mp4(url,dir,headers):
    req=requests.get(url=url,headers=headers)
    filename=str(dir)+'/1.mp4'
    with open(filename,'wb') as f:
        f.write(req.content)
cat=sys.argv[1]
flag=1
url_content=[]
find=[]
find_tittle=[]
quality=sys.argv[2]
while flag<=100:
    pornhub_url='https://www.pornhub.com/'
    c_page=pornhub_url+'video?c='+str(cat)
    base_page=c_page+'&page='+str(flag)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':base_page}
    get_base=requests.get(base_page,headers=headers)
    url_soup=bs(get_base.content,'lxml')
    for a_content in url_soup.select('.search-video-thumbs.videos li.videoBox'):
        a_content.a['class']='img js-pop'
        url_content=re.findall(r' href="/(.*?)" title',str(a_content.a))
        url=pornhub_url+url_content[0]
        headers_1={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':url}
        reqpage=requests.get(url,headers=headers_1)
        rfind='"quality":"'+str(quality)+'","videoUrl":"(.*?)"'
        find=re.findall(rfind,str(reqpage.content,'utf-8',errors='ignore'))
        find_tittle=re.findall(r'<span class="inlineFree">(.*?)</span>',str(reqpage.content,'utf-8',errors='ignore'))
        try:
            if os.path.exists(str(find_tittle[0]))==False:
                download_url=find[0].replace('\\','')
                os.makedirs(str(find_tittle[0]))
                print('开始下载：'+str(find_tittle[0]))
                print('下载URL：'+download_url)
                download_mp4(str(download_url),str(find_tittle[0]),headers_1)
                print('下载完成')
            else:
                print('跳过，文件存在')
        except IndexError:
            print('没有此清晰度')
            pass
    flag+=1

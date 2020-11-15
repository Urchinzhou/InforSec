- 啊

import requests
import re

url = 'https://www.x.com'
url_src = requests.get(url)                                     #获取 html
mp4List = re.findall(r'https://.{10,100}\.mp4',url_src.text)    #获取 mp4 url
print(mp4List)
num = 0
for mp4Url in mp4List:
    num += 1
    req = requests.get(mp4Url,stream=True)                      #获取 mp4 资源
    with(open("%d.mp4" %num,'wb')) as f:
        print("%d下载开始" %num)
        for chunk in req.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
        print("%d下载完成" %num)



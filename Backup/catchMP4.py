import requests
import re
import os

url = 'https://www.xxxxx.com'
url_src = requests.get(url)
mp4List = re.findall(r'https://.{10,100}\.mp4',url_src.text)
mp4List = list(set(mp4List))
print(mp4List)

for mp4Url in mp4List:
    name = os.path.basename(mp4Url)
    req = requests.get(mp4Url,stream=True)
    with(open("%s" %name,'wb')) as f:
        print("%s downloading" %name)
        for chunk in req.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
        print("%s finish" %name)

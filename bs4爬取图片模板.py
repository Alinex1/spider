# 爬取优美图库中子链接的高清大图(不是缩略图)

# 1.拿到主页面的源代码,然后提取到子页面的链接地址,href
# 2.通过href拿到子页面的内容,从子页面中找到图片下载地址 img -->src
# 3.下载图片
import requests
from bs4 import BeautifulSoup
import re
import time

url = 'https://www.jj20.com/'
resp = requests.get(url)
resp.encoding = 'gb2312'
# print(resp.text)

main_page = BeautifulSoup(resp.text,"html.parser")
#main_page.find("div",class_="g-box-1200") # 第一次缩小范围
'''定位的标签视情况决定 
    可以是div ,ul (保证标志性)
'''
alist = main_page.find("ul",class_="picbz").find_all("a")
#print(alist)

# 拿到属性href
for a in alist:
    a1 = a.get("href") # 通过get()拿到 a标签 中 属性href 对应的值
    wan_href = url + a1 # 根据实际情况决定是否拼接网址
    #print(wan_href)
    
    #拿到子页面的源代码
    child_page_resp = requests.get(wan_href)
    child_page_resp.encoding = 'gb2312'
    child_page_text = child_page_resp.text
    
    # 从子页面中拿到图片的下载路径
    child_page = BeautifulSoup(child_page_text,"html.parser")
    p = child_page.find("div",class_='photo')
    img = p.find("img")
    down_link = img.get("src")
    
    # 看情况拼接 从网页中查看得到属性src下网址为
    # src="//lmg.jj20.com/up/allimg
    #        /1115/011H2104125/22011G04125-1-1200.jpg
    #          缺少https:
    down_link = "https:"+down_link 
    #print(down_link)
  
    # 下载图片
    img_resp = requests.get(down_link)
    #img_resp.content # 这里拿到的是字节
    # 写入文件
    img_name = down_link.split("/")[-1] # 拿到url中最后一段作为图片名字
                                          #  他是唯一的
    with open("img/"+img_name,'wb') as f:
        f.write(img_resp.content)  # 图片内容写入文件


    print("结束",img_name)
    time.sleep(1)
print("全部结束")































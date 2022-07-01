import requests
import time
import os

from bs4 import BeautifulSoup
from rich.progress import track


def getHtmlDocL(url,headers):
    htmlDoc = ''
    while 1:
        try:
            htmlDoc = requests.get(url,headers = headers)
            break
        except:
            print("将在1秒钟后重试...")
            time.sleep(0.3)
            continue
    soup = BeautifulSoup(htmlDoc.content,'lxml')
    return soup

def getAll():
    # 得到所有页数
    lists = []
    lists.append('https://www.xx3004.cc/meinv')
    strs = 'https://www.xx3004.cc/meinv/page/'
    for i in range(2,51):
        lists.append(strs+str(i))
    return lists

def getMenuList(url):
    
    soup = getHtmlDocL(url,headers)
    pagesUrl = soup.find_all(name='a',attrs={'class': 'thumbnail'})

    lists = []

    for i in pagesUrl:
        lists.append(i.get('href'))

    with open("url.txt", 'r') as f:
        for i in lists:
            f.write(i + '\n')
    with open("urlExist.txt", 'r') as f:
        f.write('\n')

def getPageList(soup):
    pages = soup.find_all(name='a',attrs={'class': 'post-page-numbers'})

    num = int(len(pages) / 2 - 1)
    
    lists = []
    for x in pages[0:num]:
        lists.append(x.get('href'))
    
    return lists

def getImgList(soup):
    #找出所有的img 剔除前三个无用 img
    imgs = soup.find_all('img')

    imgs.pop(0)
    imgs.pop(0)
    imgs.pop(0)

    lists = []

    for i in imgs:
        lists.append(i.get('src'))
    
    return lists

def getTittle(soup,url):
    tittle = soup.find_all(name='a',attrs={'href': url})
    return tittle[0].string

def mkdir(path):
 
	folder = os.path.exists(path)
 
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print("---  new folder...  ---")
 
	else:
		print("---  There is this folder!  ---")
        

def do_work(url,numx,maxL,xxx,filex):
    src = "./"+ filex + "/" + str(numx) + ".jpg"
    pathxx = "./"+ filex + "/" + "No.txt"
    f = open(src,'wb')

    count = 0
    while 1:
        try:
            response = requests.get(url,headers=headersF,stream=True)
            f.write(response.content)
            f.close()
            numx = numx + 1
            break
        except:
            count = count + 1
            f.close()
            print("将在0.5秒钟后重试...第"+ str(count) +"次")
            time.sleep(0.2)

            if count >= 1:
                with open(pathxx, 'a') as f:
                    f.write(str(numx) + '\n')
                    f.write(url + '\n')
                numx = numx + 1
                maxL = 10
                xxx = xxx + 1
                break
            continue
    lists = [numx,maxL,xxx]
    return lists
    

########################################
print("start")

# # 1.写真总页
# tUrl = "url.txt"
# tUrlE = "urlExist.txt"

# tUrlfolder = os.path.exists(tUrl)

# if not tUrl
#     meinvAll = getAll()
#     # 2.获取所有写真的url
#     numbers = 1
#     for i in meinvAll:
#         getMenuList(i)
#         print("以爬取"+ str(numbers) +"页")
#         numbers = numbers+1

#3.提取出一个写真的所有img的url
# 获取 写真 每页 的 url
# 逐行 读取 url.txt
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Connection": "close"
    }

headersF={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Referer':'https://www.xx3004.cc/'
    }

listsUrl = []
#获取需要下载的url
with open("url.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  #去掉列表中每一个元素的换行符
        listsUrl.append(line)
print(len(listsUrl))

##判断是否以下载
listsUrlExist = []
with open("urlExist.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  #去掉列表中每一个元素的换行符
        listsUrlExist.append(line)
print(len(listsUrlExist))

countE = 0
#去重并保存
for i in listsUrlExist:
    if i in listsUrl:
        listsUrl.remove(i)
        countE = countE + 1 
print("存在"+str(countE)+"个一下载连接")


with open("url.txt", 'w') as f:
        for i in listsUrl:
            f.write(i + '\n')
    
# 提取出每页的图片 的 url
num = 1
lists = listsUrl
n = 1
for i in listsUrl:
    print("进行第"+ str(n) + "任务")
    print(i)
    #获取 html 解析
    soup = getHtmlDocL(i,headers)
    #先获取第一个url的 img url 和 其余页数的url
    listsImg = getImgList(soup)

    listsPage = getPageList(soup)

    #遍历其他页 的 img url
    for x in listsPage:
        hSoup = getHtmlDocL(x,headers)
        listsImg += getImgList(hSoup)
    
    #创建文件夹
    tittle = getTittle(soup,i)
    filex = tittle.strip()
    print(tittle)
    mkdir(filex)   

    numx = 1
    maxL = 0
    xxx = 0

    print("需要下载 "+ str(len(listsImg)) +" 张图片")
    
    it = iter(listsImg)
    nm = len(listsImg)
    for nm in track(range(nm), description="download..."):
        url = next(it)

        listsDo = do_work(url,numx,maxL,xxx,filex)
        
        numx = listsDo[0]
        maxL = listsDo[1]
        xxx = listsDo[2]

    # for url in listsImg:
               
    print("下载"+ str(numx- 1 - xxx) +"张图")


    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
    urlN = i
    #修改url.txt 和 urlExsit.txt 值
    lists.remove(urlN)
    with open("url.txt", 'w') as f:
        for z in lists:
            f.write(z + '\n')

    
    listsUrlExist.append(urlN)
    with open("urlExist.txt", 'w') as f:
        for h in listsUrlExist:
            f.write(h + '\n')
    
    n = n + 1

    #控制遍历写真数
    num = num + 1
    if num > 30:      
        break

print("byb.")
#####################################################
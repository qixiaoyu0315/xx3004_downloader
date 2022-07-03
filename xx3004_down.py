import requests
import time
import os
import re
import shutil

from bs4 import BeautifulSoup
from rich.progress import track
from rich.progress import Progress

#获取 soup
def getHtmlSoup(url,headers):
    htmlDoc = ''
    while 1:
        try:
            htmlDoc = requests.get(url,headers = headers)
            break
        except:
            print("**********将在0.3秒钟后重试...*********")
            time.sleep(0.3)
            continue
    soup = BeautifulSoup(htmlDoc.content,'lxml')
    return soup

#获取 总页数 用于生成所有页数的url
### 需要修改
def getAllUrl(numbers):
    # 得到所有页数
    lists = []
    lists.append('https://www.xx3004.cc/meinv')
    strs = 'https://www.xx3004.cc/meinv/page/'
    for i in range(2,numbers+1):
        lists.append(strs+str(i))
    return lists

#获取所有写真的url
def getMenuList(soup):

    pagesUrl = soup.find_all(name='a',attrs={'class': 'thumbnail'})

    lists = []

    for i in pagesUrl:
        lists.append(i.get('href'))

    return lists

#获取写真的所有页面的url
def getPageList(soup):
    pages = soup.find_all(name='a',attrs={'class': 'post-page-numbers'})

    num = int(len(pages) / 2 - 1)

    lists = []
    for x in pages[0:num]:
        lists.append(x.get('href'))

    return lists

#获取写真的图片地址的url
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

#获取写真的 初始标题 得到 姓名 标题
def getTittle(soup,url):
    tittle = soup.find_all(name='a',attrs={'href': url})
    tO = tittle[0].string
    tO.strip()
    tO = tO[1::]

    p = r'(?=《).*(?<=》)'
    s = re.search(p,tO)

    t = s.group()

    name = soup.find_all(name='span',attrs={'class': 'dis'})

    n = name[0].string

    na = re.compile('==>(.*?)（').findall(n)

    if len(na) == 0:
        na = re.compile('==>(.*?)，').findall(n)

    nax = na[0]

    lists = [tO,t,nax]

    return lists

#创建文件夹
def mkdir(path):

	folder = os.path.exists(path)

	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print("---  新建---" + path +"---文件夹  ---")

	else:
		print("---  存在---" + path +"---文件夹  ---")

#移动已存在的文件夹
def move_file(old_path, new_path):
    filelist = os.listdir(old_path) #列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    for file in filelist:
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)
        shutil.move(src, dst)
    print("--- 已经移动文件位置 ---")
    os.removedirs(old_path)

def remkdir(old_tittle,new_tittle,name):

    #判断是否存在 老tittle 路径
    #如果存在
    folder_tittle = os.path.exists(old_tittle)
    if folder_tittle:
        os.rename(old_tittle,new_tittle)
    #判断 是否已经存在姓名文件夹
    pathx = "./"+ name + "/" + new_tittle
    folder_name = os.path.exists(pathx)
    #如果不存在 创建
    if not folder_name:
        os.makedirs(pathx)
    #存在 直接将文件 移入 姓名目录
    old_path = "./" + new_tittle
    new_path = "./" + name + "/" + new_tittle
    move_file(old_path,new_path)

    return True

#读取txt
def readTXT(nameTxt):
    listsUrlExist = []
    with open(nameTxt, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            listsUrlExist.append(line)
    return listsUrlExist

#写入txt
def writeTXT(nameTxt,nameList,post):
    with open(nameTxt, post) as f:
        for i in nameList:
            f.write(i + '\n')

def do_work(url,numx,maxL,xxx,filex,headers):
    src = "./"+ filex + "/" + str(numx) + ".jpg"
    pathxx = "./"+ filex + "/" + "No.txt"
    f = open(src,'wb')

    count = 0
    while 1:
        try:
            response = requests.get(url,headers=headers,stream=True)
            f.write(response.content)
            f.close()
            numx = numx + 1
            break
        except:
            count = count + 1
            f.close()
            print("将在0.2秒钟后重试...第"+ str(count) +"次")
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


#获取最新的所有url
# def getPageAllUrl(soup):
#     pasoup.find_all(name='a',attrs={'class': 'thumbnail'})



##################################################
print("*****************开始*********************")
#设置是否需要联网更新
#默认 False
update = Ture
#一次下载写真数
taskNumber = 30

#获取现在的所有封面
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    'Referer':'https://www.xx3004.cc/'
    }

url = 'https://www.xx3004.cc/meinv'

#得到soup
newSoup = getHtmlSoup(url,headers)
# 获取总页数
# lastPage = newSoup.find_all('span')
# lastPageStr = lastPage[-24]
# s = lastPageStr.strip(" ")

#设置是否 追加更新
if update:
    # 当前51页
    lastPageNumber = 51

    #得到总也数的url
    allPageUrlLists = getAllUrl(lastPageNumber)

    #获取所有写真的Url
    allPageUrlListsIter = iter(allPageUrlLists)

    #所有页面的写真Url
    allUrlLists = []
    for lastPageNumber in track(range(lastPageNumber), description="Processing..."):
        pageUrl = next(allPageUrlListsIter)
        pageUrlSoup = getHtmlSoup(pageUrl,headers)
        allUrlLists = allUrlLists + getMenuList(pageUrlSoup)

    print(len(allUrlLists))

    #与已有的进行对比 urlNew.txt
    urlOldLists = readTXT('urlNew.txt')

    urlNewLists = []
    for i in allUrlLists:
        if i not in urlOldLists:
            urlNewLists.append(i)

    #存储新增url
    writeTXT("urlNew.txt",urlNewLists,'a')

    #添加到下载的文件夹中 追加 url.txt
    writeTXT("url.txt",urlNewLists,'a')

#读取url.txt
urlLists = readTXT("url.txt")
#获取一下载的 urlExist.txt
urlExistLists = readTXT("urlExist.txt")

#对比两个 查看是否有重复 url出现
countE = 0

#去重并保存
z = set(urlLists).intersection(set(urlExistLists))
for i in list(z):
    urlLists.remove(i)
print("存在"+str(len(z))+"个一下载连接,已移除")
#判断 若重复 删除 并同步到 url.txt 中
writeTXT("url.txt",urlLists,'w')

#准备工作完成
#设置本次下载写真数量 tasks
nm = 100
with Progress() as progress:

    task2 = progress.add_task("[green]Processing...", total=taskNumber)

    urlListsCopy = urlLists
    urlListsIter = iter(urlLists)

    num = 0
    while not progress.finished:
    # for urlNow in urlLists:

        #开始循环任务 下载写真
        urlNow = next(urlListsIter)

        soupNow = getHtmlSoup(urlNow,headers)
        #获取写真的 姓名 标题 介绍
        listsT = getTittle(soupNow,urlNow)
        #判断是否 采用老版本 如果是 则重命名 并移动到对应的 姓名目录下
        folder_old = os.path.exists(listsT[0])

        config = False;
        if folder_old:
            config = remkdir(listsT[0],listsT[1],listsT[2])
        #如果 config True 执行 则 直接下一个写真
        if config:
            urlListsCopy.remove(urlNow)
            writeTXT("url.txt",urlListsCopy,'w')

            urlExistLists.append(urlNow)
            writeTXT("urlExist.txt",urlExistLists,'w')

            continue
        #判断姓名是否存在 以姓名创建文件夹
        # folder_name = os.path.exists(listsT[2])
        # if not folder_name:
        #     path_name = "./"+ listsT[2]
        #     mkdir(path_name)

        path = "./"+ listsT[2] + "/" + listsT[1]
        mkdir(path)

        #先获取第一页的所有图片的 url 以及其余页数的url
        listsImg = getImgList(soupNow)

        listsPage = getPageList(soupNow)

        #通过获取其余页数的url 获得各页图片的url
        for x in listsPage:
            hSoup = getHtmlSoup(x,headers)
            listsImg += getImgList(hSoup)

        #通过所有的图片url 获取所有的图片
        numx = 1
        maxL = 0
        xxx = 0

        print("需要下载 "+ str(len(listsImg)) +" 张图片")

        it = iter(listsImg)
        nm = len(listsImg)

        #进度条
        task1 = progress.add_task("[cyan]Downloading...", total=nm)
        for nm in range(nm):
            url = next(it)

            listsDo = do_work(url,numx,maxL,xxx,path,headers)

            numx = listsDo[0]
            maxL = listsDo[1]
            xxx = listsDo[2]
            progress.update(task1, advance=1)

        # for url in listsImg:

        print("下载"+ str(numx- 1 - xxx) +"张图")
            #若出现 图片无法下载
            #则 打印到 改文件夹下的No.txt中
            #No.txt 保存为下载的 图片编号 及 图片URL

        #完成一个写真的下载 则需要
        #修改url.txt 和 urlExsit.txt 值
        urlListsCopy.remove(urlNow)
        writeTXT("url.txt",urlListsCopy,'w')

        urlExistLists.append(urlNow)
        writeTXT("urlExist.txt",urlExistLists,'w')

        #控制遍历写真数
        #判断是否已经完成所有任务
        num = num + 1
        if num > taskNumber:
            break

        progress.update(task2, advance=1)
#结束

print("********************byb.********************")
#####################################################
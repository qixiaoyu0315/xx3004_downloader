# xx3004 图片下载器

用于爬取某站写真，漫画等使用。（可能需要使用魔法才能获取）

使用前需要安装：

- Python3
- bs4
- lxml
- rich

1. 首次运行 需取消注1、2释部分 用于解析全站的地址url
2. url地址用于获取具体的图片地址
3. 文件用途

- `url.txt` :用于存储所有写真集的URL地址
- `urlExist.txt.`:用于存储已经完成下载的URL ，避免重复
- ~~`urlNo.txt`:用于存储存在部分为完全下载的写真文件~~
  - 此项可自行删除
  - 因为在具体文件夹中有 `No.txt`,记录了具体的图面序号及其Url
  - 后续将会写一个用于补下这些图片的工具

- 默认一次执行30次下载任务

==注意，本工具在ubuntu下运行，若在windows下运行，可能需要修改路径格式==

![image-20220701165602520](https://s2.loli.net/2022/07/01/ybd41FzqkEw6PiQ.png)

**本工具只是学习爬虫练手，禁止用于非法环境，后果自负。**

**本工具只是学习爬虫练手，禁止用于非法环境，后果自负。**

**本工具只是学习爬虫练手，禁止用于非法环境，后果自负。**
# 小红书笔记信息自动化获取脚本

## 环境要求
- Python 3.9及以上
- DrissionPage
- BeautifulSoup (bs4)

## 使用方法

1. 在项目代码同目录下创建名为`xhs_urls.txt`的文件。
2. 在`xhs_urls.txt`文件中写入需要抓取的URLs，每行一个URL。
3. 安装所需的包后直接执行代码。

## 安装依赖

```bash
pip install drissionpage beautifulsoup4
```

## 2024/11/18更新：
- 增加了爬取正文内容以及爬取发布时间的功能
- 对于一些易报错的操作进行了try except保护 增强项目鲁棒性
- 简化输入流程 只需要简历input.txt文件 按行分割写入想要搜索的内容即可自动转化

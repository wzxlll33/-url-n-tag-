from DrissionPage import ChromiumPage
from bs4 import BeautifulSoup
import time
import csv


time_lst = []
content_lst = []
tag_lst = []
name_lst = []
count_likes = []
count_stars = []
count_comments = []


def read_file_to_list(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            # 使用列表推导式读取每一行
            content_list = [line.strip() for line in file]
        return content_list


urls = read_file_to_list('xhs_urls.txt')

page = ChromiumPage()

def get_data(url):
    page.get(url)
    flag = 0
        # time.sleep(10)\
    for j in range(1,11):
        # 判断有无多出来的一栏 通过信息正确点入单个视频
            #                /html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/div/div/div/button[1]
        if (page.ele('xpath:/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/div/div/div/button[1]',1,0.3) != None) or (page.ele('xpath:/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/div/div/div/button[1]',1,0.3) != None):
            ele = page.ele(f'xpath:/html/body/div[1]/div[1]/div[2]/div[2]/div/div[4]/section[{j}]/div/div/a/span',1,1)
        else:               
            ele = page.ele(f'xpath:/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/section[{j}]/div/div/a/span',1,1)
        if ele == None:
            flag = 1
            continue

        # 点击笔记名字进入笔记详情页 并且记录此时点击元素的text 这个text即为我们需要的笔记名字
        name_lst.append(ele.text)
        page.actions.click(ele)

        # sleep保证加载完成
        time.sleep(1)
        soup = BeautifulSoup(page.html,"html.parser")                         
        
        # 调用get_likes方法获取点赞量
        count_likes.append(get_likes(soup))
        
        # 调用get_stars方法获取收藏量
        get_stars()

        # 调用get_comments方法获取评论量
        get_comments()

        # 调用get_tag方法获取所有tag
        get_tag(soup)

        # 调用get_content方法获取正文
        get_content()

        # 调用get_time方法获取发布时间
        get_time()
        
        # 将flag重设 保证下一次爬取正常运行
        flag = 0

        # 将页面倒回上一层 保证下一次点击正常进行
        page.back(1)

    if flag == 1:
         # 判断有无多出来的一栏 通过信息正确点入单个视频
        if page.s_ele('xpath:/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/div/div/div/button[1]') != None:
            ele = page.ele(f'xpath:/html/body/div[1]/div[1]/div[2]/div[2]/div/div[4]/section[11]/div/div/a/span',1,1)
        else:               
            ele = page.ele(f'xpath:/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/section[11]/div/div/a/span',1,1)

        # 点击笔记名字进入笔记详情页 并且记录此时点击元素的text 这个text即为我们需要的笔记名字
        name_lst.append(ele.text)
        page.actions.click(ele)

        # sleep保证加载完成
        time.sleep(1)
        soup = BeautifulSoup(page.html,"html.parser")                         
        
        # 调用get_likes方法获取点赞量
        count_likes.append(get_likes(soup))
        
        # 调用get_stars方法获取收藏量
        get_stars()

        # 调用get_tag方法获取所有tag
        get_tag(soup)

        # 调用get_content方法获取正文
        get_content()

        # 调用get_time方法获取发布时间
        get_time()
        

    # print(count_likes)
    # print(name_lst)
    # print(count_comments)
    # print(count_stars)
    # print(tag_lst)


def get_likes(soup):
    likes = soup.select('#noteContainer > div.interaction-container > div.interactions.engage-bar > div > div > div.input-box > div.interact-container > div > div.left > span.like-wrapper.like-active > span.count')
    return likes[0].get_text()


def get_stars():
    ele_stars = page.s_ele('xpath:/html/body/div[5]/div[1]/div[4]/div[3]/div/div/div[1]/div[2]/div/div[1]/span[2]/span')
    if ele_stars.text == '收藏':
        stars_temp = 0
    else:
        stars_temp = ele_stars.text
    count_stars.append(stars_temp)
         

def get_comments():
    ele_comments = page.s_ele('xpath:/html/body/div[5]/div[1]/div[4]/div[3]/div/div/div[1]/div[2]/div/div[1]/span[3]/span')
    if ele_comments.text == '评论':
        comment_temp = 0
    else:
        comment_temp = ele_comments.text
    count_comments.append(comment_temp)


def get_tag(soup):
    lst_temp = []
    temp_tag = soup.findAll("a",{"class":"tag"})
    for tag in temp_tag:
        lst_temp.append(tag.get_text())
    tag_lst.append(lst_temp)
    

def get_content():
    try:
        ele_content = page.s_ele('xpath:/html/body/div[5]/div[1]/div[4]/div[2]/div[1]/div[2]/span/span[1]')
        content_lst.append(ele_content.text)    
    except:
        content_lst.append('None')


def get_time():
    ele_time = page.s_ele('xpath:/html/body/div[5]/div[1]/div[4]/div[2]/div[1]/div[3]/span[1]')
    time_lst.append(ele_time.text)


def __main__():
    for i in range(len(urls)):
        print(f'正在爬取{urls[i]}')
        get_data(urls[i])
        print("done")
    filename = 'xhs_data.csv'

    # 使用'write'模式打开文件
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # 创建一个csv的写入器
        writer = csv.writer(csvfile)
        #标题,内容摘要,点赞量,收藏量,评论量,发布时间,标签
        # 写入标题行（可选）
        writer.writerow(['Name', 'content', 'likes', 'stars', 'comments', 'time', 'tag'])
        print(len(content_lst))
        # 遍历列表并写入数据
        for i in range(len(name_lst)):
            writer.writerow([name_lst[i],content_lst[i], count_likes[i], count_stars[i], count_comments[i], time_lst[i], tag_lst[i]])
            # writer.writerow([name_lst[i]])
            # writer.writerow([content_lst[i]])
            # writer.writerow([count_likes[i]])
            # writer.writerow([count_stars[i]])
            # writer.writerow([count_comments[i]])
            # writer.writerow([time_lst[i]])
            # writer.writerow([tag_lst[i]])

    print(f'数据已写入 {filename}')


__main__()

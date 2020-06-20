"""

@Project: doubanMovieComments
@Author: CoffeeCat
@Time: 2020/6/12 12:41 上午
@File: Douban_Movie_Comments.py
@IDE: PyCharm

"""
import time
import requests
from uaPool import userAgent
from lxml import etree
import csv

def login(name, password):
    """
    模拟登陆豆瓣网
    :return:
    """
    login_url = 'https://accounts.douban.com/passport/login'
    data = {'ck': '', 'name': name, 'password': password, 'remember': 'false', 'ticket': ''}
    status = 'success'
    try:
        r = s.get(url=login_url, headers=headers)
        post = s.post(url=login_url, headers=headers, data=data)
        post.raise_for_status()
    except:
        print('Login failed!')
        return 0
    if status in post.text:
        print('Successfully log in')
        return 1


'''
- 每条数据的字段包括：评论者昵称、评论者所在城市、评论时间、评论分数、评论文本、评论点赞数；
'''


def crawl_comments(ID, page, type):
    """
    爬取短评页面的评论者昵称、评论时间、评论分数、评论文本、评论点赞数
    :param page:
    :param type:
    :return:
    """
    general_url = 'https://movie.douban.com/subject/{}/' \
                  'comments?start={}&limit=20&sort=new_score&status=P&percent_type={}'.format(ID, (page - 1) * 20, type)
    res = s.get(general_url, headers=headers)
    parsed = etree.HTML(res.text)

    personal_page = parsed.xpath('//*[@id="comments"]/div/div[2]/h3/span[2]/a/@href')
    user_city = []
    for i in range(0, len(personal_page)):
        city = crawl_user_city(personal_page[i])
        user_city.append(city)

    user_name = parsed.xpath('//*[@id="comments"]/div/div[2]/h3/span[2]/a/text()')
    comments_score = parsed.xpath('//*[@id="comments"]/div/div[2]/h3/span[2]/span[2]/@title')
    comments_time = parsed.xpath('//*[@id="comments"]/div/div[2]/h3/span[2]/span[3]/@title')
    comments_content = parsed.xpath('//*[@id="comments"]/div/div[2]/p/span/text()')
    comments_like = parsed.xpath('//*[@id="comments"]/div/div[2]/h3/span[1]/span/text()')
    for j in range(0, 19):
        result = []
        result.append(user_name[j])
        result.append(user_city[j])
        result.append(comments_time[j])
        result.append(comments_content[j])
        result.append(comments_score[j])
        result.append(comments_like[j])
        list2csv(result, result_filename)

def crawl_user_city(href):
    """
    爬取评论用户主页链接里的所在城市信息
    :param name:
    :param href:
    :return:
    """
    res = s.get(href, headers=headers)
    parsed = etree.HTML(res.text)
    user_city = []
    if res.status_code == 200:
        user_city = parsed.xpath('//*[@id="profile"]/div/div[2]/div[1]/div/a/text()')
    return user_city


def list2csv(data, filename):
    file_path = 'your file path'+filename
    with open(file_path, 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(data)


if __name__ == '__main__':

    ua = userAgent()
    headers = {'user-agent': ua.get_ua_all_platform()}
    s = requests.Session()
    name = 'your user_name'            #用户名
    password = 'your code'         #密码
    movie_id = 'target movie ID'           #电影ID
    result_filename = 'result.csv'  #数据存储文件名

    if login(name, password):
        positive = 'h'  #好评
        neutral = 'm'   #一般
        negative = 'l'  #差评
        # 爬取正面评论
        time.sleep(1)
        print('Preparing to crawl positive comments')
        time.sleep(1)
        for page in range(1, 26):
            print('Crawling page {}'.format(page))
            time.sleep(5)
            crawl_comments(movie_id, page, negative)
    '''
        #爬取一般评论
        print('Preparing to crawl neutral comments')
        time.sleep(1)
        for page in range(1,5):
            print('Crawling page {}'.format(page))
            crawl_comments(page, neutral)
    
        #爬取负面评论
        print('Preparing to crawl negative comments')
        time.sleep(1)
        for page in range(1,5):
            print('Crawling page {}'.format(page))
            crawl_comments(page, negative)
    '''

#!/usr/bin/python3
# _*_ coding: utf-8 _*_
import os
from bs4 import BeautifulSoup
import requests
import json
import sys
import random
sys.setrecursionlimit(10000)

#问题id
ques_id_list =[]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'referer': 'https: // www.zhihu.com /',
    'cookie': '_zap=5be1e1ef-530e-4b98-a2c5-a74abc65328c; __DAYU_PP=AnJrB73abrJaaAUnRnbqffffffffd4f021478a79; d_c0="ACDgi6Ziaw2PTutstmH1EZlTofQ8yy_sDcI=|1523324808"; _xsrf=vRONRqkfHequ3JiJ6UySgM2Hx5NnU9XO; __utmv=51854390.100--|2=registration_date=20150709=1^3=entry_date=20150709=1; __utma=51854390.1655730157.1544059342.1547004017.1553246228.4; z_c0="2|1:0|10:1561618697|4:z_c0|92:Mi4xZlhQVkFRQUFBQUFBSU9DTHBtSnJEU1lBQUFCZ0FsVk5DYmNCWGdBY3F3SjlTcjdtejdFWXUtQkFZU09JNFI1OVp3|c9c13407693c7aa1191c89b04336502a27175b5410e17829bae2465d8c07bc0f"; tst=r; q_c1=52fdb38e9fc747d599734bd7aad8309f|1573643201000|1522743249000; tgw_l7_route=64ba0a179156dda09fec37a3b2d556ed; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1574772879,1574842181,1574845078,1574845587; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1574845886'
}

poxy_list=[]

def initPoxy():
    poxy_list.append({"http":"223.111.131.100:8080"})
    poxy_list.append({"http": "218.60.8.99:3129"})
    poxy_list.append({"http": "39.137.107.98:80"})
    poxy_list.append({"http": "118.89.234.236:8787"})
    poxy_list.append({"http": "218.22.7.62:53281"})
    poxy_list.append({"http": "117.57.91.235:9999"})
    poxy_list.append({"http": "110.243.23.117:9999"})

def getZhiHu():
    baseurl = "https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=266ffeaebe639cb2631838b446eccd67&desktop=true&page_number=4&limit=6&action=down&after_id="
    url_list = []
    for num in range(1,3):
        url_list.append(baseurl + str(num*5))
    for url in url_list:
        regPoxy(url,1)

def regPoxy(url,num):
    response = requests.get(url, headers=headers, proxies=random.choice(poxy_list))
    if response.status_code == 200:
        if num == 1:
            getzhihutitle(response)
        else:
            getZhiHuItemDetail(response)
    else:
        regPoxy(url)

#获取知乎推荐标题
def getzhihutitle(response):

    html = response.text
    dict_json = json.loads(html)
    dit_list = dict_json['data']
    for ditc in dit_list:
        ditTarget = ditc['target']
        # 标题
        try:
            dict_question = ditTarget['question']
            print(dict_question['title'])
        except:
            print(ditTarget['title'])

        # 回答者
        print('回答者: ' + ditTarget['author']['name'])
        # 回答者个人签名
        print('个人签名: ' + ditTarget['author']['headline'])

        if dict_question['type'] == 'question':
            # 问题具体页面
            print('问题详细url:  https://www.zhihu.com/question/' + str(dict_question['id']))

        # ques_id_list.append(dict_question['id'])

        # 回答内容
        htmls = BeautifulSoup(ditTarget['content'], "html.parser")
        print(htmls.get_text())
        print('')

base_item_url_start = 'https://www.zhihu.com/api/v4/questions/'
base_item_url_end = '/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset=&limit=3&sort_by=default&platform=desktop'

count = 0
#单个问题抓取
def getZhiHuItemDetail(response):

    html = response.text
    dict_json = json.loads(html)
    dit_total = dict_json['paging']
    print('总共回答数：'+ str(dit_total['totals']))

    dit_list = dict_json['data']
    for dictBean in dit_list:
        question_info = []  # 该问题所有数据
        global  count
        if count ==0 :
            print('问题： ' + dictBean['question']['title'])
            count = count + 1
        print('回答者：'+dictBean['author']['name'])
        print('个人签名：' + dictBean['author']['headline'])

        question_info.append('回答者：'+dictBean['author']['name'])
        question_info.append('个人签名：' + dictBean['author']['headline'])

        # 回答内容
        htmls = BeautifulSoup(dictBean['content'], "html.parser")
        print(htmls.get_text())
        question_info.append(htmls.get_text())
        print('')
        saveQuesInfo(question_info,dictBean['question']['title'],dit_total['totals'])

    is_end = dit_total['is_end']
    if is_end :
        print('.................结束......................')
        # exit()
        startSpider()
    else:
        # getZhiHuItemDetail(dit_total['next'])
        regPoxy(dit_total['next'], 2)

#保存某一个问题详情
def saveQuesInfo(question_info,title,totalNum):

    basePath=r"C:/Users/fp/Desktop/zhihu/" #保存爬取的话题地址，自己更改
    file = open(os.path.join(basePath)+"{}.txt".format(title), "a",encoding='utf-8')
    for ques in question_info:
        for i in range(len(ques)):
            file.write(ques[i])
        file.write('\n')
    file.write('\n')
    file.close()


#爬取某一个问题
def startSpider():
    id = input('请输入想要查看的问题id：')
    if id != 'exit':
        url = base_item_url_start + id + base_item_url_end
        regPoxy(url,2)
    else:
        print('.................结束......................')
        exit()

if __name__ == "__main__":
    initPoxy()
    getZhiHu()
    startSpider()


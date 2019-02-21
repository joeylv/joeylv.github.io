import os
import re
import sqlite3

import numpy
import pandas as pandas
import xlrd as xlrd
import xlsxwriter as xlsxwriter
import xlwt
import requests
import xlwt as xlwt
from requests import Request
import xlsxwriter
import pandas
numpy
import xlrd
class coursemd(object):
    def __init__(self):
        self.con = sqlite3.connect('topic.db')
        self.cur = self.con.cursor()

    def search(self):
        sql = "SELECT * FROM topic limit 2"
        try:
            # 执行SQL语句
            self.cur.execute(sql)
            # 获取所有记录列表
            results = self.cur.fetchall()
            for row in results:
                fname = row[0]
                title = row[1]
                body = row[2]
                image = row[3]

                # 下载图片
                for img in image.split(','):
                    # default_headers['referer'] = img
                    if img:
                        print("image_url::::::::::::::" + img)
                        print(img[str.rindex(img, '/') + 1:])
                        html = requests.get(img)
                        if html.status_code == 200:
                            img_path = '../md/img/' + img[str.rindex(img, '/') + 1:]
                            body = body.replace(img, '> ![Alt text](' + img_path + ')<')
                            if os.path.exists(img_path) is False:
                                print('存图片')
                                file = open(img_path, 'wb')
                                file.write(html.content)

                md_path = '../md/' + str(title) + '.md'
                # print(body.find(img))
                with open(md_path, 'a', encoding='utf8') as f:

                    # with open(fname + '.md', 'wa') as f:
                    f.write('##' + title + '\n')

                    dr = re.compile(r'<[^>]+>', re.S)
                    body = body.replace('<p><span style="font-size: large;">', '\n####').replace('<h2>', '>\n##')
                    # dr = re.compile(r'</?\w+[^>]*>', re.S)
                    dd = dr.sub('', body.replace('<pre>', "\t").replace('}', "\t}")).replace('\n', '')
                    f.write(dd.strip())

                    # 打印结果
                    # print(' title {}'.format(title))
                    # with

        except Exception as e:
            print("Error: unable to fecth data {}".format(e))


if __name__ == '__main__':
    coursemd().search()

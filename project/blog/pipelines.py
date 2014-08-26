# -*- coding: utf-8 -*-

import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BlogPipeline(object):
    def __init__(self):
        try:
            conn = MySQLdb.connect(
                host = 'localhost',
                user = 'root',
                passwd = '86185228', # your passwd
                port = 3306,
            )
            cur = conn.cursor()
            cur.execute('DROP DATABASE IF EXISTS blogJobbole_DB')
            cur.execute('CREATE DATABASE blogJobbole_DB CHARACTER SET utf8')
            cur.execute('use blogJobbole_DB')
            cur.execute('CREATE TABLE IF NOT EXISTS article \
                (title varchar(50), link varchar(50), tag varchar(50), \
                content varchar(10000))')
            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print 'MySQLdb Error %d: %s' % (e.args[0], e.args[1])

    def process_item(self, item, spider):
        try:
            conn = MySQLdb.connect(
                host = 'localhost',
                user = 'root',
                passwd = '86185228',
                port = 3306,
                db = 'blogJobbole_DB',
                charset = 'utf8',
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO article VALUES(%s, %s, %s, %s)", \
                    [item['title'], item['link'], item['tag'], item['content']])
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print 'MySQLdb Error %d: %s' % (e.args[0], e.args[1])


# -*- coding:utf-8 -*-

# AccountManager -- Account/password management tool
# Copyright (C) 2016 -- 2021 Binhua Zhang <kosmos_zhang@hotmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3 as sqlite

class InitDao(object):
    '''
    用于系统数据库初始化
    '''
    def __init__(self, conn):
        self.conn = conn

    def execute(self, sqlfile):
        '''
        用于执行生气了脚本文件
        '''
        sql = ''

        for line in open(sqlfile):
            line = line.strip()
            if line.endswith(';'):
                sql += line
                self._executesql(sql)
                sql = ''
            else:
                sql += line + '\n'

    def _executesql(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.close()

class RootDao(object):
    '''
    用于Root用户数据操作管理
    '''
    def __init__(self, conn):
        self.conn = conn

    def getRootPwd(self):
        '''
        获取root用户的密码(md5加密)
        '''
        sql = """SELECT md5String FROM ROOTPASSWORD"""
        cur = self.conn.cursor()
        cur.execute(sql)
        mPwd = cur.fetchone()[0]
        cur.close()
        return mPwd

    def updateRootPwd(self, newMd5):
        sql = """update ROOTPASSWORD set md5String=?"""
        cur = self.conn.cursor()
        cur.execute(sql,(newMd5,))
        cur.close()

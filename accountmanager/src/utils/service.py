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

from dao import *
import config
import util
import datetime
import os

class RemoveTagException: pass

class Service:
    def __init__(self):        
        pass
    
    def getConnection(self):
        return sqlite.connect(config.CONN_PATH)

class InitDataService(Service):
    """
    用于检测数据库文件是否存在，第一次使用的时候创建数据库
    """

    def createDB(self):
        if os.path.exists(config.CONN_PATH):
            return

        dataDir = os.path.dirname(config.CONN_PATH)
        if not os.path.exists(dataDir):
            os.makedirs(dataDir)

        sqlFile = os.path.join(config.PKG_ROOT, "conf/init.sql")
        conn = self.getConnection()
        initDao = InitDao(conn)
        initDao.execute(sqlFile)
        conn.close()

class RootService(Service):
    '''
    用于操作管理Root
    '''
    def __init__(selfparams):
        pass

    def getRootPwd(self):
        '''
        get root passwd (md5 encrypted)
        '''
        conn = self.getConnection()
        rootDao = RootDao(conn)
        result = rootDao.getRootPwd()
        conn.close()
        return result    
    
    def authentication(self, pwd):
        md5String = util.md5Encode(pwd)
        md5Pwd = self.getRootPwd()
        return True if md5String == md5Pwd else False
    
    def changeRootPwd(self, newRootPwd):
        newMd5String = util.md5Encode(newRootPwd)

        conn = self.getConnection()
        rootDao = RootDao(conn)
        rootDao.updateRootPwd(newMd5String)
        conn.commit()
        conn.close()

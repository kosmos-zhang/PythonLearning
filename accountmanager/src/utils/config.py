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

from os import path
import sys, shutil
import ConfigParser


# root password
#Default:password
#MD5:5f4dcc3b5aa765d61d8327deb882cf99 
__ROOT_PWD     = ''

# database path
CONN_PATH      = '' #filled by confighandler

# APP name
APP_NAME       = 'Account Manager'

#APP Root path
# using this complicated assignment because the exe file by py2exe doesn't 
# work with path.dirname(__file__)
PKG_ROOT =  path.dirname(unicode(sys.executable, sys.getfilesystemencoding( ))) \
        if hasattr(sys, "frozen") else path.abspath(path.join(path.dirname(__file__), '../'))

def setRootPwd(newPwd):
    global __ROOT_PWD
    __ROOT_PWD = newPwd

def getRootPwd():
    global __ROOT_PWD
    return __ROOT_PWD

def init():
    global CONN_PATH
    
    configFile = path.join(PKG_ROOT, 'conf/accmgr.conf')

    cf = ConfigParser.ConfigParser()
    if not path.exists(configFile):
        return False
    cf.read(configFile);

    CONN_PATH = cf.get("settings","data.path")
    if not CONN_PATH:
        return False

    CONN_PATH = path.join(PKG_ROOT, CONN_PATH)
    return True

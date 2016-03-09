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

import os
from gui.windows import LoginWindow, MainWindow
import utils.config as config
from utils.service import InitDataService

class AccMgrApp():
    def Run(self):
        pwdDlg = LoginWindow()
        result = pwdDlg.Logon
        
        if result:
            mainWin = MainWindow()
            mainWin.Show()
            return True
        else:
            return False

if __name__ == '__main__':
    if not config.init():
        exit(1)

    initService = InitDataService()
    initService.createDB()

    accMgr = AccMgrApp()
    accMgr.Run()

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import os,pathlib

class OSHelp(object):
    @staticmethod
    def launchPath():
        '''
        起始目錄
        '''
        return os.path.normpath(os.path.abspath(os.path.curdir))

    @staticmethod
    def genPathList(rootPath:str,includeDirectory:bool = True, extList:list = None, lst:list = None) ->list:
        '''產生檔案與目錄集
        ---
        rootPath: 根目錄\n
        includeDirectory: 是否包含目錄\n
        extList: 副檔名 LIst, 如 ['.JPEG','.CR2'],  ['*'] 為包含目錄\n
        lst : <class 'nt.DirEntry'> 物件的 List 集合\n
        '''
        if extList == None:
            extList = ["*"]
        if lst == None:
            lst = []
        try:
            for f in os.scandir(rootPath):
                #print(type(f))
                if f.is_dir():
                    if includeDirectory:
                        lst.append(f)
                    OSHelp.genPathList(f.path, includeDirectory, extList, lst)
                elif f.is_file():
                    if pathlib.Path(f.path).suffix.upper() in extList or extList == ['*']:
                        lst.append(f)
        except Exception as e:
            print("\"{}\" {}:{}".format(rootPath, type(e),str(e)))
        return lst

class BeUI(object):
    @staticmethod
    def doFixSize(ui:QtWidgets.QMainWindow):
        '''固定尺寸
        ---
        ui: QtWidgets元件
        '''
        ui.setFixedSize(ui.frameGeometry().width(),ui.frameGeometry().height())
    
    @staticmethod
    def QCheckBoxStyleShee(isDark:bool = True):
        ''' QCheckBox Mouse Over (hover) StyleShee
        ---
        isDark: 是否為 Dark 模式 
        '''
        if isDark:
            # 亮底暗字
            return "QCheckBox::unchecked:hover \
                        { \
                        color: rgb(32, 32, 32); \
                        background-color: rgb(230, 230, 230); \
                        } \
                        QCheckBox::checked:hover \
                        { \
                        color: rgb(32, 32, 32); \
                        background-color: rgb(230, 230, 230); \
                        }"
        else:
            # 暗底亮字
            return "QCheckBox::unchecked:hover \
                        { \
                        color: rgb(250, 250, 250); \
                        background-color: rgb(80, 80, 80); \
                        } \
                        QCheckBox::checked:hover \
                        { \
                        color: rgb(250, 250, 250); \
                        background-color: rgb(80, 80, 80); \
                        }"
        
        
    @staticmethod
    def toCenter(ui:QtWidgets.QMainWindow):
        qr = ui.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        ui.move(qr.topLeft())

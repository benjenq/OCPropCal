# pyinstaller --add-data "PropDesc.json:." --add-data "File2:." -F --windowed --clean OCPropCal.py
from PyQt5 import QtWidgets,QtGui,QtCore #PyQt5 : pip3 install pyqt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QRegExpValidator, QDesktopServices
from PyQt5.QtCore import QRegExp,QEvent,QUrl
# pip3 install pyqtdarktheme #https://pypi.org/project/pyqtdarktheme/
# for python 3.12:
# pip3 install pyqtdarktheme==2.1.0 --ignore-requires-python
import qdarktheme, darkdetect
import traceback,os #,webbrowser
import UIMainWindow
from BeLib.BeUtility import *
from BeLib.BeConvert import *
from OCLib import *
from OCConfig import *

class mainWin(QtWidgets.QMainWindow,UIMainWindow.Ui_MainWindow):
    def __init__(self,parent=None):
        super(mainWin,self).__init__()
        self.setupUi(self)
        BeUI.toCenter(self)
        BeUI.doFixSize(self)
        '''尋找元件範例
        txt = self.centralwidget.findChild(QPlainTextEdit, "txt1")
        txt.setPlainText("DDDD")
        self.chk_1.setChecked(True)
        '''
        #CSR
        reg_exHex = QRegExp("[0-9a-fA-F]*")
        inputHex_validator = QRegExpValidator(reg_exHex, self.tb_csrData)
        self.tb_csrData.setValidator(inputHex_validator)
        #https://stackoverflow.com/questions/2760206/qvalidator-for-hex-input
        #self.tb_csrData.setInputMask("HHHHHHHH") #用 regex 取代 HEX 遮罩
        #textEdited 取代 textChanged, 限定使用鍵盤編輯才會觸發
        self.tb_csrData.textEdited[str].connect(lambda :self.tbDataEdited(self.tb_csrData,OCPropType.CSR_STATUS))
        #self.tb_csrData.textChanged[str].connect(lambda :self.tbDataEnter(self.tb_csrData,PropertiesType.CSR_STATUS))
        # boot-args 編輯: textEdited 取代 textChanged, 限定使用鍵盤編輯才會觸發
        self.tb_bootargs.textEdited[str].connect(lambda: self.tbBootArgsEdited(self.tb_bootargs))

        #OCA: PickerAttributes
        reg_exNum = QRegExp("[0-9]*")
        inputNum_validator = QRegExpValidator(reg_exNum, self.tb_ocaNumber)
        self.tb_ocaNumber.setValidator(inputNum_validator)
        #self.tb_ocaNumber.setInputMask("###") #用 regex 取代數字遮罩
        self.tb_ocaNumber.textEdited[str].connect(lambda :self.tbNumberEdited(self.tb_ocaNumber,OCPropType.OCA_STATUS))

        #SCP: ScanPolicy
        self.tb_scpNumber.setValidator(inputNum_validator)
        #self.tb_scpNumber.setInputMask("########") #用 regex 取代數字遮罩
        self.tb_scpNumber.textEdited[str].connect(lambda :self.tbNumberEdited(self.tb_scpNumber,OCPropType.SCP_STATUS))

        #ESD: ExposeSensitiveData
        self.tb_esdNumber.setValidator(inputNum_validator)
        #self.tb_esdNumber.setInputMask("##") #用 regex 取代數字遮罩
        self.tb_esdNumber.textEdited[str].connect(lambda :self.tbNumberEdited(self.tb_esdNumber,OCPropType.ESD_STATUS))
        self.ocHelp = OCHelp()
        self.ocConfig = OCConfig('')
        self.bind_CheckBoxText()        
        self.checkEvent(OCPropType.CSR_STATUS,self.CSR_ALLOW_ANY_RECOVERY_OS)
        self.checkEvent(OCPropType.OCA_STATUS,self.OC_ATTR_USE_DISK_LABEL_FILE)
        self.checkEvent(OCPropType.SCP_STATUS,self.OC_SCAN_FILE_SYSTEM_LOCK)
        self.checkEvent(OCPropType.ESD_STATUS,self.OC_EXPOSE_BOOTERPATH_AS_UEFI_VARIABLE)
        # self.actionOpen.setShortcut('Ctrl+O') #use designer
        self.actionOpen.triggered.connect(self.openSelectDialog)
        self.actionSave.triggered.connect(self.saveToFile)
        #self.actionHelp.triggered.connect(lambda: webbrowser.open('http://www.google.com'))
        self.actionHelp.triggered.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/benjenq/OCPropCal')))
        self.actionReset.triggered.connect(lambda: self.resetDefault())
        self.actionOCLPSIP.triggered.connect(lambda: self.oclpSip())
        self.actionExit.triggered.connect(self.exitApp)
        self.btnBootArgsCopy.clicked.connect(self.copyBootArgs) #用 lambda 好像有問題
        # 設定 tabWidget 可拖曳檔案
        #self.tabWidget.setAcceptDrops(True)
        self.tabWidget.installEventFilter(self)
    
    def copyBootArgs(self):
        if self.tb_bootargs.text() != "":
            QApplication.clipboard().setText(self.tb_bootargs.text())


    def openSelectDialog(self):
        dlg = QFileDialog()
        dlg.setDirectory(OSHelp.launchPath())
        chooseFilePath , _ = dlg.getOpenFileName(self,caption="Select OC config File", filter="OC config (*.plist)")
        if(chooseFilePath == ""):
            return
        chooseFilePath = os.path.normpath(chooseFilePath)
        success = self.load_OCConfigPlist(chooseFilePath)
        if not success:
            self.showMessageBox("\"{}\"\n is NOT a valid OC config file".format(chooseFilePath))

    def load_OCConfigPlist(self,filePath:str):
        self.ocConfig = OCConfig(filePath)
        if not self.ocConfig.isRead:
            return False
        self.setWindowTitle('OpenCore Properties Calculator - {} '.format(self.ocConfig.filePath))
        self.actionSave.setEnabled(True)
        self.actionReset.setEnabled(True)
        try:
            self.tb_ocaNumber.setText(str(self.ocConfig.propDict['oca']))
            self.tb_esdNumber.setText(str(self.ocConfig.propDict['esd']))
            self.tb_scpNumber.setText(str(self.ocConfig.propDict['scp']))
            self.tb_csrData.setText(str(self.ocConfig.propDict['csr']))
            self.tb_bootargs.setText(str(self.ocConfig.propDict['boot-args']))
            self.tbNumberEdited(self.tb_ocaNumber,OCPropType.OCA_STATUS)
            self.tbNumberEdited(self.tb_esdNumber,OCPropType.ESD_STATUS)
            self.tbNumberEdited(self.tb_scpNumber,OCPropType.SCP_STATUS)
            self.tbDataEdited(self.tb_csrData,OCPropType.CSR_STATUS)
            self.tbBootArgsEdited(self.tb_bootargs)
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    def saveToFile(self):
        if not self.ocConfig.isRead or not self.actionSave.isEnabled():
            self.statusbar.showMessage("config plist can not save!")
            return
        pDict = {'oca': int(self.tb_ocaNumber.text()),
                 'esd': int(self.tb_esdNumber.text()),
                 'scp': int(self.tb_scpNumber.text()),
                 'csr': str(self.tb_csrData.text()),
                 'boot-args': str(self.tb_bootargs.text())}
        self.ocConfig.bind_propDict(pDict)
        success, msg = self.ocConfig.saveToFile(self.ocConfig.filePath)
        self.statusbar.showMessage(msg)
        if not success:
            self.showMessageBox(msg,True)
        else:
            self.showMessageBox(msg,False)

    def resetDefault(self):
        self.tb_ocaNumber.setText(str(17))
        self.tb_esdNumber.setText(str(6))
        self.tb_scpNumber.setText(str(17760515))
        self.tb_csrData.setText('00000000')
        self.tbNumberEdited(self.tb_ocaNumber,OCPropType.OCA_STATUS)
        self.tbNumberEdited(self.tb_esdNumber,OCPropType.ESD_STATUS)
        self.tbNumberEdited(self.tb_scpNumber,OCPropType.SCP_STATUS)
        self.tbDataEdited(self.tb_csrData,OCPropType.CSR_STATUS)
    
    def oclpSip(self):
        self.tb_csrData.setText('03080000')
        self.tbDataEdited(self.tb_csrData,OCPropType.CSR_STATUS)

    def bind_CheckBoxText(self):
        for item in csr_list:
            chk = self.tab_csr.findChild(QCheckBox,item)
            if chk == None:
                continue
            chk.setText(self.ocHelp.objText(item))
            #chk.stateChanged.connect(lambda:self.checkEvent(PropertiesType.CSR_STATUS, chk)) #connect 會根據 chk 的變化而改變，導致 BUG
            chk.clicked.connect(lambda:self.checkEvent(OCPropType.CSR_STATUS, chk)) #connect 會根據 chk 的變化而改變，導致 BUG
            '''解決 BUG 的寫法
            match chk:
                case self.CSR_ALLOW_UNTRUSTED_KEXTS:
                    chk.stateChanged.connect(lambda: self.chk_Event(self.CSR_ALLOW_UNTRUSTED_KEXTS))
                case self.CSR_ALLOW_UNRESTRICTED_FS:
                    chk.stateChanged.connect(lambda: self.chk_Event(self.CSR_ALLOW_UNRESTRICTED_FS))
            '''
            #https://stackoverflow.com/questions/51456403/mouseover-event-for-a-pyqt5-label
            chk.installEventFilter(self)
        for item in oca_list:
            chk = self.tab_oca.findChild(QCheckBox,item)
            if chk == None:
                continue
            chk.setText(self.ocHelp.objText(item))
            #chk.stateChanged.connect(lambda:self.checkEvent(PropertiesType.OCA_STATUS, chk)) #connect 會根據 chk 的變化而改變，導致 BUG
            chk.clicked.connect(lambda:self.checkEvent(OCPropType.OCA_STATUS, chk)) #connect 會根據 chk 的變化而改變，導致 BUG
            #https://stackoverflow.com/questions/51456403/mouseover-event-for-a-pyqt5-label
            chk.installEventFilter(self)
        for item in esd_list:
            chk = self.tab_esd.findChild(QCheckBox,item)
            if chk == None:
                continue
            chk.setText(self.ocHelp.objText(item))
            #chk.stateChanged.connect(lambda:self.checkEvent(PropertiesType.ESD_STATUS, chk)) #connect 會根據 chk 的變化而改變，導致 BUG
            chk.clicked.connect(lambda:self.checkEvent(OCPropType.ESD_STATUS, chk)) #connect 會根據 chk 的變化而改變，導致 BUG
            #https://stackoverflow.com/questions/51456403/mouseover-event-for-a-pyqt5-label
            chk.installEventFilter(self)
        for item in scp_list:
            chk = self.tab_scp.findChild(QCheckBox,item)
            if chk == None:
                continue
            chk.setText(self.ocHelp.objText(item))
            #chk.stateChanged.connect(lambda:self.checkEvent(PropertiesType.SCP_STATUS, chk)) #connect 會根據 chk 的變化而改變，導致 BUG
            chk.clicked.connect(lambda:self.checkEvent(OCPropType.SCP_STATUS, chk)) #connect 會根據 chk 的變化而改變，導致 BUG
            #https://stackoverflow.com/questions/51456403/mouseover-event-for-a-pyqt5-label
            chk.installEventFilter(self)
        #boot-args
        for item in bootargs_dict.keys():
            chk = self.tab_bootargs.findChild(QCheckBox,item)
            if chk == None:
                continue
            chk.setText(self.ocHelp.objText(item))
            chk.clicked.connect(lambda: self.checkBootArgs(chk))
            chk.installEventFilter(self)

    def tbDataEdited(self,obj:QLineEdit,pType:OCPropType):
        if self.tb_csrData.text().replace(' ','') == '':
            if pType == OCPropType.CSR_STATUS:
                for item in csr_list:
                    chk = self.tab_csr.findChild(QCheckBox,item)
                    chk.setChecked(False)
                self.tb_csrHex.setText('')
            return
        try:
            decVal = int(hexReversed(self.tb_csrData.text()),16)
        except Exception as e:
            return
        lst = self.ocHelp.lstFromDecimal(decVal,pType)
        self.lstBindCheckBox(lst,pType)
        if pType == OCPropType.CSR_STATUS:
            self.tb_csrHex.setText(decimalToHex(decVal,False))

    def tbNumberEdited(self,obj:QLineEdit,pType:OCPropType):
        if obj.text().replace(' ','') == '':
            if pType == OCPropType.OCA_STATUS:
                for item in oca_list:
                    chk = self.tab_oca.findChild(QCheckBox,item)
                    if chk != None:
                        chk.setChecked(False)
                self.tb_ocaHex.setText('')
            elif pType == OCPropType.ESD_STATUS:
                for item in esd_list:
                    chk = self.tab_esd.findChild(QCheckBox,item)
                    if chk != None:
                        chk.setChecked(False)
                self.tb_esdHex.setText('')
            elif pType == OCPropType.SCP_STATUS:
                for item in scp_list:
                    chk = self.tab_scp.findChild(QCheckBox,item)
                    if chk != None:
                        chk.setChecked(False)
                self.tb_scpHex.setText('')
            return
        decVal = int(obj.text())
        lst = self.ocHelp.lstFromDecimal(decVal,pType)
        self.lstBindCheckBox(lst,pType)
        if pType == OCPropType.OCA_STATUS:
            self.tb_ocaHex.setText(decimalToHex(decVal,False))
        elif pType == OCPropType.SCP_STATUS:
            self.tb_scpHex.setText(decimalToHex(decVal,False))
        elif pType == OCPropType.ESD_STATUS:
            self.tb_esdHex.setText(decimalToHex(decVal,False))

    def lstBindCheckBox(self,lst:list, pType:OCPropType):
        '''從 List 綁定 Checkbox
        ---
        lst: List\n
        pType: OCPropType
        '''
        #print(self.tb_csrData.focus())
        if pType == OCPropType.OCA_STATUS:
            for item in oca_list:
                chk = self.tab_oca.findChild(QCheckBox,item)
                if chk != None:
                    chk.setChecked(False)
            for chkItem in lst:
                chkb = self.tab_oca.findChild(QCheckBox,chkItem)
                if chkb != None:
                    chkb.setChecked(True)
        elif pType == OCPropType.ESD_STATUS:
            for item in esd_list:
                chk = self.tab_esd.findChild(QCheckBox,item)
                if chk != None:
                    chk.setChecked(False)
            for chkItem in lst:
                chkb = self.tab_esd.findChild(QCheckBox,chkItem)
                if chkb != None:
                    chkb.setChecked(True)
        elif pType == OCPropType.SCP_STATUS:
            for item in scp_list:
                chk = self.tab_scp.findChild(QCheckBox,item)
                if chk != None:
                    chk.setChecked(False)
            for chkItem in lst:
                chkb = self.tab_scp.findChild(QCheckBox,chkItem)
                if chkb != None:
                    chkb.setChecked(True)
        elif pType == OCPropType.CSR_STATUS:
            for item in csr_list:
                chk = self.tab_csr.findChild(QCheckBox,item)
                if chk != None:
                    chk.setChecked(False)
            for chkItem in lst:
                chkb = self.tab_csr.findChild(QCheckBox,chkItem)
                if chkb != None:
                    chkb.setChecked(True)
        # Boot-Args
        elif pType == OCPropType.BOOT_ARGS:
            for item in bootargs_dict.keys():
                chk = self.tab_bootargs.findChild(QCheckBox,item)
                if chk != None:
                    chk.setChecked(False)
            for bootArg in lst:
                chkName = self.ocHelp.bootValueToKey(bootArg)
                if chkName == None:
                    continue
                chkb = self.tab_bootargs.findChild(QCheckBox,chkName)
                if chkb != None:
                    chkb.setChecked(True)
    
    def checkEvent(self,pType:OCPropType,obj:QCheckBox):
        ''' 點擊 Checkbox 事件
        ---
        pType: OCPropType\n
        '''
        #print(obj.objectName()) #這裡會出現 BUG，
        chkList = []
        if pType == OCPropType.OCA_STATUS:
            for item in oca_list:
                chk = self.tab_oca.findChild(QCheckBox,item)
                if chk == None:
                    continue
                if chk.isChecked():
                    chkList.append(item)
            result = self.ocHelp.lstToDecimal(chkList,pType)
            self.tb_ocaNumber.setText(str(result))
            self.tb_ocaHex.setText(decimalToHex(result,False))
        elif pType == OCPropType.ESD_STATUS:
            for item in esd_list:
                chk = self.tab_esd.findChild(QCheckBox,item)
                if chk == None:
                    continue
                if chk.isChecked():
                    chkList.append(item)
            result = self.ocHelp.lstToDecimal(chkList,pType)
            self.tb_esdNumber.setText(str(result))
            self.tb_esdHex.setText(decimalToHex(result,False))
        elif pType == OCPropType.SCP_STATUS:
            for item in scp_list:
                chk = self.tab_scp.findChild(QCheckBox,item)
                if chk == None:
                    continue
                if chk.isChecked():
                    chkList.append(item)
            result = self.ocHelp.lstToDecimal(chkList,pType)
            self.tb_scpNumber.setText(str(result))
            self.tb_scpHex.setText(decimalToHex(result,False))
        elif pType == OCPropType.CSR_STATUS:
            for item in csr_list:
                chk = self.tab_csr.findChild(QCheckBox,item)
                if chk == None:
                    continue
                if chk.isChecked():
                    chkList.append(item)
            result = self.ocHelp.lstToHex(chkList,pType,False)
            self.tb_csrHex.setText(result)
            self.tb_csrData.setText(hexToData(result))

    # Boot-Args 相關
    def checkBootArgs(self,obj:QCheckBox):
        #找出勾選的 boot-args
        bootChkLst=[]
        for objName in bootargs_dict.keys():
            chk = self.tab_bootargs.findChild(QCheckBox,objName)
            if chk == None:
                continue
            if chk.isChecked():
                bootChkLst.append(bootargs_dict[objName]['value'])
        result = self.ocHelp.bootArgsWithArgs(self.tb_bootargs.text(),bootChkLst)
        self.tb_bootargs.setText(result)

    def tbBootArgsEdited(self,obj:QLineEdit):
        '''編輯 Boot-Args
        ---
        '''
        lst = self.ocHelp.bootArgsStrToList(obj.text())
        self.lstBindCheckBox(lst,OCPropType.BOOT_ARGS)
    def exitApp(self):
        self.close()
    
    #https://stackoverflow.com/questions/51456403/mouseover-event-for-a-pyqt5-label
    def eventFilter(self, obj, event):
        ''' installEventFilter 事件
        '''
        if obj.__class__.__name__ == 'QCheckBox':
            if event.type() == QEvent.Enter:
                #print("{}:Mouse is over the label".format(obj.objectName()))
                self.statusbar.showMessage(obj.text())
                obj.setStyleSheet(BeUI.QCheckBoxStyleShee(darkdetect.isDark()))
                return True
            elif event.type() == QEvent.Leave:
                #print("{}:Mouse is not over the label".format(obj.objectName()))
                #obj.setStyleSheet(BeUI.QCheckBoxStyleShee(''))
                self.statusbar.showMessage('')
        elif obj == self.tabWidget and event.type() == QEvent.DragEnter:
            if darkdetect.isDark():
                obj.setStyleSheet("background-color: rgb(60, 60, 60);")
            else:
                obj.setStyleSheet("background-color: rgb(220, 220, 220);")

            if event.mimeData().hasUrls():
                event.acceptProposedAction()
            else:
                event.ignore()
        elif obj == self.tabWidget and event.type() == QEvent.Drop:
            # 必須有 DragEnter 才會觸發 Drop
            obj.setStyleSheet("")            
            if event.mimeData().hasUrls():
                url = os.path.normpath(event.mimeData().urls()[0].toLocalFile())
                success = self.load_OCConfigPlist(url)
                if not success:
                    self.showMessageBox("\"{}\"\n is NOT a valid OC config file".format(url))
                event.acceptProposedAction()
            else:
                event.ignore()
        elif obj == self.tabWidget and event.type() == QEvent.MouseButtonPress:
            '''
            print('QEvent.MouseButtonPress')
            self.openSelectDialog()
            '''
            pass
        return super(mainWin,self).eventFilter(obj, event)

    def showMessageBox(self,msg:str,isError:bool = True):
        '''Show Message
        ---
        msg: message text
        isError: 是否為錯誤
        '''
        if isError:
            QtWidgets.QMessageBox.critical(self,"Error", msg ,QtWidgets.QMessageBox.Yes )
        else:
            QtWidgets.QMessageBox.information(self,"Information", msg ,QtWidgets.QMessageBox.Yes)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        choose = QtWidgets.QMessageBox.question(self,"Question","This App will close & exit.\nAre you sure?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No )
        if choose == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        #return super().closeEvent(event)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    win = mainWin()
    win.show()
    sys.exit(app.exec_())
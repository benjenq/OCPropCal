import plistlib,os
import traceback

class OCConfig(object):
    def __init__(self,filePath:str = '') -> None:
        self.clear()
        self.readFromFile(filePath)

    def readFromFile(self, filePath:str):
        self.clear()
        if filePath == '' or not os.path.isfile(filePath):
            return
        try:
            with open(filePath, 'rb') as fp:
                self.allConfig = plistlib.load(fp)
                fp.close()
                pDist = {}
                pDist["oca"]=self.allConfig["Misc"]["Boot"]["PickerAttributes"]            
                pDist["esd"]=self.allConfig["Misc"]["Security"]["ExposeSensitiveData"]
                pDist["scp"]=self.allConfig["Misc"]["Security"]["ScanPolicy"]
                csr=self.allConfig["NVRAM"]["Add"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"]["csr-active-config"]
                #bytes to hex https://stackoverflow.com/questions/6624453/whats-the-correct-way-to-convert-bytes-to-a-hex-string-in-python-3
                pDist["csr"] = str(csr.hex())
                #print(pl["Misc"]["Security"]["ScanPolicy"])
                self.propDict = pDist
                self.isRead = True
                self.filePath = filePath
        except Exception as e:
            #traceback.print_exc()
            pass
    
    def bind_propDict(self,pDict:dict):
        self.propDict["oca"] = pDict["oca"]
        self.propDict["esd"] = pDict["esd"]
        self.propDict["scp"] = pDict["scp"]
        self.propDict["csr"] = pDict["csr"]
    
    def syncWithDict(self):
        self.allConfig["Misc"]["Boot"]["PickerAttributes"] = self.propDict["oca"]
        self.allConfig["Misc"]["Security"]["ExposeSensitiveData"] = self.propDict["esd"]
        self.allConfig["Misc"]["Security"]["ScanPolicy"] = self.propDict["scp"]
        #https://www.geeksforgeeks.org/convert-hex-string-to-bytes-in-python/
        self.allConfig["NVRAM"]["Add"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"]["csr-active-config"] = bytes.fromhex(str(self.propDict["csr"]))    

    def saveToFile(self, filePath:str):
        if not self.isRead:
            return False,"File {} did Not read.".format(filePath)
        self.syncWithDict()
        try:
            with open(filePath, 'wb') as fp:
                plistlib.dump(self.allConfig,fp)
                fp.close()
                return True,"Save to {} success".format(filePath)
        except Exception as e:
            return False, str(e)
        
    def clear(self):
        self.isRead = False
        self.filePath = ''
        self.allConfig = None
        self.propDict = {'oca': 0,
                         'esd': 0,
                         'scp': 0,
                         'csr':''}

if __name__ == "__main__":
    cfg = OCConfig('R:/OCDecode/Sample.plist')
    print(cfg.filePath)
    cfg.saveToFile('R:/OCDecode/config.plist')


import math
from BeLib.BeConvert import *
from BeLib.BeUtility import *
from enum import Enum
import os, json, shutil, traceback
class OCPropType(Enum):
    OCA_STATUS = 1
    ESD_STATUS = 2
    SCP_STATUS = 3
    CSR_STATUS = 4

#PickerAttributes
oca_list = [
    "OC_ATTR_USE_VOLUME_ICON",
    "OC_ATTR_USE_DISK_LABEL_FILE",
    "OC_ATTR_USE_GENERIC_LABEL_IMAGE",
    "OC_ATTR_HIDE_THEMED_ICONS",
    "OC_ATTR_USE_POINTER_CONTROL",
    "OC_ATTR_SHOW_DEBUG_DISPLAY",
    "OC_ATTR_USE_MINIMAL_UI",
    "OC_ATTR_USE_FLAVOUR_ICON",
    "OC_ATTR_USE_REVERSED_UI",
    "OC_ATTR_REDUCE_MOTION"
]

#ExposeSensitiveData
#https://dreamwhite-oc-esd.vercel.app/
esd_list = [
    "OC_EXPOSE_BOOTERPATH_AS_UEFI_VARIABLE",
    "OC_EXPOSE_OCVERSION_AS_UEFI_VARIABLE",
    "OC_EXPOSE_OCVERSION_IN_PICKER_NEMU",
    "OC_EXPOSE_OEMINFO_AS_UEFI_VARIABLES"
]
esd_desc =  {
    "OC_EXPOSE_BOOTERPATH_AS_UEFI_VARIABLE" : "expose the printable booter path as a UEFI variable.",
    "OC_EXPOSE_OCVERSION_AS_UEFI_VARIABLE"  :  "expose the OpenCore version as a UEFI variable.",
    "OC_EXPOSE_OCVERSION_IN_PICKER_NEMU" : "expose the OpenCore version in the OpenCore picker menu title.",
    "OC_EXPOSE_OEMINFO_AS_UEFI_VARIABLES" : "expose OEM information as a set of UEFI variables."
}

#ScanPolicy
scp_list = [
    "OC_SCAN_FILE_SYSTEM_LOCK", #0x00000001
    "OC_SCAN_DEVICE_LOCK",      #0x00000002
    "OC_SCAN_RESERVE_0x00000004",
    "OC_SCAN_RESERVE_0x00000008",
    "OC_SCAN_RESERVE_0x00000010",
    "OC_SCAN_RESERVE_0x00000020",
    "OC_SCAN_RESERVE_0x00000040",
    "OC_SCAN_RESERVE_0x00000080",
    "OC_SCAN_ALLOW_FS_APFS",    #0x00000100
    "OC_SCAN_ALLOW_FS_HFS",     #0x00000200
    "OC_SCAN_ALLOW_FS_ESP",     #0x00000400
    "OC_SCAN_ALLOW_FS_NTFS",    #0x00000800
    "OC_SCAN_ALLOW_FS_LINUX_ROOT", #0x00001000
    "OC_SCAN_ALLOW_FS_LINUX_DATA", #0x00002000
    "OC_SCAN_ALLOW_FS_XBOOTLDR",   #0x00004000
    "OC_SCAN_RESERVE_0x00008000",
    "OC_SCAN_ALLOW_DEVICE_SATA",  #0x00010000
    "OC_SCAN_ALLOW_DEVICE_SASEX", #0x00020000
    "OC_SCAN_ALLOW_DEVICE_SCSI",  #0x00040000
    "OC_SCAN_ALLOW_DEVICE_NVME",  #0x00080000
    "OC_SCAN_ALLOW_DEVICE_ATAPI", #0x00100000
    "OC_SCAN_ALLOW_DEVICE_USB",   #0x00200000
    "OC_SCAN_ALLOW_DEVICE_FIREWIRE", #0x00400000
    "OC_SCAN_ALLOW_DEVICE_SDCARD", #0x00800000
    "OC_SCAN_ALLOW_DEVICE_PCI"    #0x01000000
]

#csr-active-config
csr_list = [
    "CSR_ALLOW_UNTRUSTED_KEXTS",
    "CSR_ALLOW_UNRESTRICTED_FS",
    "CSR_ALLOW_TASK_FOR_PID",
    "CSR_ALLOW_KERNEL_DEBUGGER",
    "CSR_ALLOW_APPLE_INTERNAL",
    # "CSR_ALLOW_DESTRUCTIVE_DTRACE (name deprecated)",
    "CSR_ALLOW_UNRESTRICTED_DTRACE",
    "CSR_ALLOW_UNRESTRICTED_NVRAM",
    "CSR_ALLOW_DEVICE_CONFIGURATION",
    "CSR_ALLOW_ANY_RECOVERY_OS",
    "CSR_ALLOW_UNAPPROVED_KEXTS",
    "CSR_ALLOW_EXECUTABLE_POLICY_OVERRIDE",
    "CSR_ALLOW_UNAUTHENTICATED_ROOT"
]

#Properties Description
desc_dict = {
    "OC_ATTR_USE_VOLUME_ICON" : "OC_ATTR_USE_VOLUME_ICON",
    "OC_ATTR_USE_DISK_LABEL_FILE" : "OC_ATTR_USE_DISK_LABEL_FILE",
    "OC_ATTR_USE_GENERIC_LABEL_IMAGE" : "OC_ATTR_USE_GENERIC_LABEL_IMAGE",
    "OC_ATTR_HIDE_THEMED_ICONS" : "OC_ATTR_HIDE_THEMED_ICONS",
    "OC_ATTR_USE_POINTER_CONTROL" : "OC_ATTR_USE_POINTER_CONTROL",
    "OC_ATTR_SHOW_DEBUG_DISPLAY" : "OC_ATTR_SHOW_DEBUG_DISPLAY",
    "OC_ATTR_USE_MINIMAL_UI" : "OC_ATTR_USE_MINIMAL_UI",
    "OC_ATTR_USE_FLAVOUR_ICON" : "OC_ATTR_USE_FLAVOUR_ICON",
    "OC_ATTR_USE_REVERSED_UI" : "OC_ATTR_USE_REVERSED_UI",
    "OC_ATTR_REDUCE_MOTION" : "OC_ATTR_REDUCE_MOTION",
    "OC_EXPOSE_BOOTERPATH_AS_UEFI_VARIABLE" : "expose the printable booter path as a UEFI variable.",
    "OC_EXPOSE_OCVERSION_AS_UEFI_VARIABLE"  :  "expose the OpenCore version as a UEFI variable.",
    "OC_EXPOSE_OCVERSION_IN_PICKER_NEMU" : "expose the OpenCore version in the OpenCore picker menu title.",
    "OC_EXPOSE_OEMINFO_AS_UEFI_VARIABLES" : "expose OEM information as a set of UEFI variables.",
    "OC_SCAN_FILE_SYSTEM_LOCK" : "OC_SCAN_FILE_SYSTEM_LOCK", #0x00000001
    "OC_SCAN_DEVICE_LOCK" : "OC_SCAN_DEVICE_LOCK",      #0x00000002
    "OC_SCAN_RESERVE_0x00000004" : "",
    "OC_SCAN_RESERVE_0x00000008" : "",
    "OC_SCAN_RESERVE_0x00000010" : "",
    "OC_SCAN_RESERVE_0x00000020" : "",
    "OC_SCAN_RESERVE_0x00000040" : "",
    "OC_SCAN_RESERVE_0x00000080" : "",
    "OC_SCAN_ALLOW_FS_APFS" : "OC_SCAN_ALLOW_FS_APFS",    #0x00000100
    "OC_SCAN_ALLOW_FS_HFS" : "OC_SCAN_ALLOW_FS_HFS",     #0x00000200
    "OC_SCAN_ALLOW_FS_ESP" : "OC_SCAN_ALLOW_FS_ESP",     #0x00000400
    "OC_SCAN_ALLOW_FS_NTFS" : "OC_SCAN_ALLOW_FS_NTFS",    #0x00000800
    "OC_SCAN_ALLOW_FS_LINUX_ROOT" : "OC_SCAN_ALLOW_FS_LINUX_ROOT", #0x00001000
    "OC_SCAN_ALLOW_FS_LINUX_DATA" : "OC_SCAN_ALLOW_FS_LINUX_DATA", #0x00002000
    "OC_SCAN_ALLOW_FS_XBOOTLDR" : "OC_SCAN_ALLOW_FS_XBOOTLDR",   #0x00004000
    "OC_SCAN_RESERVE_0x00008000" : "",
    "OC_SCAN_ALLOW_DEVICE_SATA" : "OC_SCAN_ALLOW_DEVICE_SATA",  #0x00010000
    "OC_SCAN_ALLOW_DEVICE_SASEX" : "OC_SCAN_ALLOW_DEVICE_SASEX", #0x00020000
    "OC_SCAN_ALLOW_DEVICE_SCSI" : "OC_SCAN_ALLOW_DEVICE_SCSI",  #0x00040000
    "OC_SCAN_ALLOW_DEVICE_NVME" : "OC_SCAN_ALLOW_DEVICE_NVME",  #0x00080000
    "OC_SCAN_ALLOW_DEVICE_ATAPI" : "OC_SCAN_ALLOW_DEVICE_ATAPI", #0x00100000
    "OC_SCAN_ALLOW_DEVICE_USB" : "OC_SCAN_ALLOW_DEVICE_USB",   #0x00200000
    "OC_SCAN_ALLOW_DEVICE_FIREWIRE" : "OC_SCAN_ALLOW_DEVICE_FIREWIRE", #0x00400000
    "OC_SCAN_ALLOW_DEVICE_SDCARD" : "OC_SCAN_ALLOW_DEVICE_SDCARD", #0x00800000
    "OC_SCAN_ALLOW_DEVICE_PCI" : "OC_SCAN_ALLOW_DEVICE_PCI",    #0x01000000
    "CSR_ALLOW_UNTRUSTED_KEXTS" : "CSR_ALLOW_UNTRUSTED_KEXTS",
    "CSR_ALLOW_UNRESTRICTED_FS" : "CSR_ALLOW_UNRESTRICTED_FS",
    "CSR_ALLOW_TASK_FOR_PID" : "CSR_ALLOW_TASK_FOR_PID",
    "CSR_ALLOW_KERNEL_DEBUGGER" : "CSR_ALLOW_KERNEL_DEBUGGER",
    "CSR_ALLOW_APPLE_INTERNAL" : "CSR_ALLOW_APPLE_INTERNAL",
    # "CSR_ALLOW_DESTRUCTIVE_DTRACE (name deprecated)" : "",
    "CSR_ALLOW_UNRESTRICTED_DTRACE" : "CSR_ALLOW_UNRESTRICTED_DTRACE",
    "CSR_ALLOW_UNRESTRICTED_NVRAM" : "CSR_ALLOW_UNRESTRICTED_NVRAM",
    "CSR_ALLOW_DEVICE_CONFIGURATION" : "CSR_ALLOW_DEVICE_CONFIGURATION",
    "CSR_ALLOW_ANY_RECOVERY_OS" : "CSR_ALLOW_ANY_RECOVERY_OS",
    "CSR_ALLOW_UNAPPROVED_KEXTS" : "CSR_ALLOW_UNAPPROVED_KEXTS",
    "CSR_ALLOW_EXECUTABLE_POLICY_OVERRIDE" : "CSR_ALLOW_EXECUTABLE_POLICY_OVERRIDE",
    "CSR_ALLOW_UNAUTHENTICATED_ROOT" : "CSR_ALLOW_UNAUTHENTICATED_ROOT"
}

class OCHelp(object):
    def __init__(self) -> None:
        # OCA : PickerAttributes
        val = 1
        val_r = 1
        self.oca_dict = {}
        self.oca_dict_r = {}
        for item in oca_list:
            self.oca_dict[val] = item
            self.oca_dict_r[item] = val_r
            val+=1
            val_r <<= 1

        # ESD: ExposeSensitiveData
        val = 1
        val_r = 1
        self.esd_dict = {}
        self.esd_dict_r = {}
        for item in esd_list:
            self.esd_dict[val] = item
            self.esd_dict_r[item] = val_r
            val+=1
            val_r <<= 1

        # SCP: ScanPolicy
        val = 1
        val_r = 1
        self.scp_dict = {}
        self.scp_dict_r = {}
        for item in scp_list:
            if item.find("_RESERVE_") < 0:
                self.scp_dict[val] = item
                self.scp_dict_r[item] = val_r
            val+=1
            val_r <<= 1

        # CSR
        val = 1
        val_r = 1
        self.csr_dict = {}
        self.csr_dict_r = {}
        for item in csr_list:
            self.csr_dict[val] = item
            self.csr_dict_r[item] = val_r
            val+=1
            val_r <<= 1

        self.descDict = None
        descFileName = 'PropDesc.json'
        descPath = os.path.join(OSHelp.launchPath(), descFileName);
        try:
            if not os.path.exists(descPath):
                print(f"copy PropDesc File : {descFileName}")
                shutil.copy2(os.path.join(os.path.dirname(__file__),descFileName),descPath)
            with open(file=descPath, mode='r', encoding='utf8') as f:
                self.descDict = json.load(f)
                f.close
        except Exception as e:
            traceback.print_exc()
        if self.descDict == None:
            self.descDict = desc_dict

    def lstFromHex(self,hexVal:str,pType:OCPropType = OCPropType.CSR_STATUS):
        '''Hex 回傳 CSR 陣列
        ---
        hexVal: Hex 值
        pType: PropertiesType 值 (CSR_STATUS, ESD_STATUS, OCA_STATUS, SCP_STATUS)
        '''
        decVal = hexToDecimal(hexVal)
        return self.lstFromDecimal(decVal,pType)


    def lstFromDecimal(self,decVal:str,pType:OCPropType = OCPropType.CSR_STATUS):
        '''Decimal 十進位回傳陣列
        ---
        decVal: Hex 值\n
        pType: PropertiesType 值 (CSR_STATUS, ESD_STATUS, OCA_STATUS, SCP_STATUS)
        '''
        if(type(decVal) != int):
            decVal = int(decVal)
        binVal = decimalToBinary(decVal)[::-1] #反轉
        result = []
        for i in range(0,len(binVal)):
            try:
                if binVal[i] == '1':
                    if pType == OCPropType.OCA_STATUS :
                        result.append(self.oca_dict[i+1])
                    elif pType == OCPropType.ESD_STATUS :
                        result.append(self.esd_dict[i+1])
                    elif pType == OCPropType.SCP_STATUS :
                        result.append(self.scp_dict[i+1])
                    elif pType == OCPropType.CSR_STATUS :
                        result.append(self.csr_dict[i+1])           
            except Exception as e:
                pass
                #traceback.print_exc()
                #print("{}:{}".format(type(e).__name__,e))
        return result
    
    def lstToDecimal(self,lst:list,pType:OCPropType = OCPropType.CSR_STATUS):
        '''陣列回傳十進位值
        ---
        lst: 字串陣列，例如 ['CSR_ALLOW_TASK_FOR_PID', 'CSR_ALLOW_UNRESTRICTED_NVRAM'] \n
        pType: PropertiesType 值 (CSR_STATUS, ESD_STATUS, OCA_STATUS, SCP_STATUS)
        '''
        val = 0
        for item in lst:
            if pType == OCPropType.OCA_STATUS:
                sList = self.oca_dict_r
            elif pType == OCPropType.ESD_STATUS:
                sList = self.esd_dict_r
            elif pType == OCPropType.SCP_STATUS:
                sList = self.scp_dict_r
            elif pType == OCPropType.CSR_STATUS:
                sList = self.csr_dict_r
            else:
                print('pType no defined')
                return - 1
            try:
                val = val + sList[item]
            except:
                traceback.print_exc()
        return val
    
    def lstToHex(self,lst:list,pType:OCPropType = OCPropType.CSR_STATUS, prefix: bool=True):
        '''陣列回傳 Hex 值
        ---
        lst: 字串陣列，例如 ['CSR_ALLOW_TASK_FOR_PID', 'CSR_ALLOW_UNRESTRICTED_NVRAM'] \n
        pType: PropertiesType,
        prefix: 是否有 0x 前綴
        '''
        return decimalToHex(self.lstToDecimal(lst,pType),prefix)

if __name__ == "__main__":
    oc = OCHelp()
    #i=126
    #print('{} == {}'.format(i,oc.lstFromDecimal(i,PropertiesType.OCA_STATUS)))
    #lst = ['OC_ATTR_USE_DISK_LABEL_FILE', 'OC_ATTR_USE_GENERIC_LABEL_IMAGE', 'OC_ATTR_HIDE_THEMED_ICONS', 'OC_ATTR_USE_POINTER_CONTROL', 'OC_ATTR_SHOW_DEBUG_DISPLAY', 'OC_ATTR_USE_MINIMAL_UI']
    #print(oc.lstToDecimal(lst,PropertiesType.OCA_STATUS))
    i=19858179
    print('{} == {}'.format(i,oc.lstFromDecimal(i,OCPropType.SCP_STATUS)))
    lst = ['OC_SCAN_FILE_SYSTEM_LOCK', 'OC_SCAN_DEVICE_LOCK', 'OC_SCAN_ALLOW_FS_APFS', 'OC_SCAN_ALLOW_FS_HFS', 'OC_SCAN_ALLOW_DEVICE_SATA', 'OC_SCAN_ALLOW_DEVICE_SASEX', 'OC_SCAN_ALLOW_DEVICE_SCSI', 'OC_SCAN_ALLOW_DEVICE_NVME', 'OC_SCAN_ALLOW_DEVICE_USB', 'OC_SCAN_ALLOW_DEVICE_PCI']
    print(oc.lstToDecimal(lst,OCPropType.SCP_STATUS))

    #print(dataToHex("03080000"))

    #a = 0b1001
    #b = 0b1010
    #print(decimalToBinary(a+b))

    #print(oc.lstFromHex('803',PropertiesType.CSR_STATUS))
    '''
    print(decimalToHex(binaryToDecimal('1000000000000000000000000')))
    print(round(math.log(int('0x01000000',0),2)))
    hello = list('hello')
    hello[1] = 'a'
    print(''.join(hello))
    aa='hello'.split('l')
    print(aa)'''
    import locale
    print(locale.getdefaultlocale())
    import os
    print(os.getenv('LANG'))


        

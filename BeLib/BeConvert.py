def hexToDecimal(hexVal:str) -> int:
    '''HEX 值轉 10 進位數值
    ---
    hexVal: Hex 值\n
    '''
    if(type(hexVal) != 'str'):
        hexVal = str(hexVal)
    if hexVal[:2] == '0x':
        return(int(hexVal,0))
    return(int(hexVal,16))

def decimalToHex(num,prefix = True) -> str:
    '''10 進位數值轉 HEX 值
    ---
    num: 10 進位數值\n
    prefix: 是否有 0x 前綴 
    '''
    if(prefix):
        return(hex(num)) #去掉 0x
    return(hex(num)[2:]) #去掉 0x

def decimalToBinary(num) -> str:
    '''10 進位數值轉二進值
    ---
    num: 10 進位值\n
    '''
    return bin(num).replace('0b', '')

def binaryToDecimal(b) -> int:
    '''二進值轉數值
    ---
    b: 二進值\n
    '''
    return int(b,2)

def hexReversed(hexVal:str,prefix = False, g:int = 2) -> str:
    '''反轉 Hex 值, 1a2b3c4d -> 4d3c2b1a
    ---
    hexVal: 輸入的 Hex 字串\n
    g: 字元群組長度
    https://stackoverflow.com/questions/9475241/split-string-every-nth-character
    '''
    if hexVal[0:2] == '0x':
        hexVal = hexVal.replace('0x','')
    if prefix:
        preStr = '0x'
    else:
        preStr = ''
    hexArray = [hexVal[n:n+g] for n in range(0,len(hexVal),g)]
    return ''.join([preStr,''.join(hexArray[::-1])])

def zFillWithLength(inStr:str,inlength:int = 8):
    '''靠右, 左邊填0補長度
    ---
    inStr: 輸入字串\n
    inlength: 總長度\n
    https://blog.csdn.net/weixin_42317507/article/details/93411132
    '''
    if inStr[0:2] == '0x':
        inStr = inStr.replace('0x','')
    return(inStr.rjust(inlength,'0')) #靠右，左邊補0
    #return inStr.zfill(inlength) #靠右，左邊補0
    #return(inStr.ljust(inlength,'0')) #靠左，右邊補0

def hexToData(hexVal:str,hlength:int=8):
    ''' Hex 值轉 Data，例如 0x803 => 03080000
    ---
    hexVal: 輸入的 Hex 字串\n
    hlength: Data 長度\n

    '''
    if hexVal[0:2] == '0x':
        hexVal = hexVal.replace('0x','')
    return(hexReversed(zFillWithLength(hexVal,hlength)))

def dataToHex(dataVal:str, prefix = True):
    ''' Data 值轉 Hex，例如 03080000 => (0x)803
    ---
    dataVal: 輸入的 Hex 字串\n
    dlength: Data 長度\n
    prefix: 是否有 0x 前綴 

    '''
    hexVal = hex(int(hexReversed(dataVal),16))
    if(prefix):
        return hexVal
    return hexVal[2:]

if __name__ == "__main__":
    print(hexReversed('0x1a2b3c4d'))
    
    
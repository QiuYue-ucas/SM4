def strxor( message , key , len ):
	out = ""
	for i in range ( 0 , len ):
		ch = ord(message[i]) ^ ord(key[i])
		out = out + chr(ch)
	return out

def str2hex( string ):
    out = ""
    for i in range ( 0 , len(string) ):
        out = out + " " + hex(ord( string[i] ))
    return out

def strldc( string , bit ):
    byte = bit // 8
    bit = bit % 8
    out = ""
    if bit == 0 :
        out = string[byte:] + string[:byte]
    else :
        reg = string[byte:] + string[:byte+1]
        for i in range (0,len(reg)-1):
            out = out + chr(((ord(reg[i])*(2**bit))+(ord(reg[i+1])//(2**(8-bit))))%256)
        out = out[:len(string)]
    return out

def SearchSbox( reg , Act ):
    out = ""
    Sbox = ['\xd6' , '\x90' , '\xe9' , '\xfe' , '\xcc' , '\xe1' , '\x3d' , '\xb7' , '\x16' , '\xb6' , '\x14' , '\xc2' , '\x28' , '\xfb' , '\x2c' , '\x05',  
    '\x2b' , '\x67' , '\x9a' , '\x76' , '\x2a' , '\xbe' , '\x04' , '\xc3' , '\xaa' , '\x44' , '\x13' , '\x26' , '\x49' , '\x86' , '\x06' , '\x99',  
    '\x9c' , '\x42' , '\x50' , '\xf4' , '\x91' , '\xef' , '\x98' , '\x7a' , '\x33' , '\x54' , '\x0b' , '\x43' , '\xed' , '\xcf' , '\xac' , '\x62',  
    '\xe4' , '\xb3' , '\x1c' , '\xa9' , '\xc9' , '\x08' , '\xe8' , '\x95' , '\x80' , '\xdf' , '\x94' , '\xfa' , '\x75' , '\x8f' , '\x3f' , '\xa6',  
    '\x47' , '\x07' , '\xa7' , '\xfc' , '\xf3' , '\x73' , '\x17' , '\xba' , '\x83' , '\x59' , '\x3c' , '\x19' , '\xe6' , '\x85' , '\x4f' , '\xa8',  
    '\x68' , '\x6b' , '\x81' , '\xb2' , '\x71' , '\x64' , '\xda' , '\x8b' , '\xf8' , '\xeb' , '\x0f' , '\x4b' , '\x70' , '\x56' , '\x9d' , '\x35',  
    '\x1e' , '\x24' , '\x0e' , '\x5e' , '\x63' , '\x58' , '\xd1' , '\xa2' , '\x25' , '\x22' , '\x7c' , '\x3b' , '\x01' , '\x21' , '\x78' , '\x87',  
    '\xd4' , '\x00' , '\x46' , '\x57' , '\x9f' , '\xd3' , '\x27' , '\x52' , '\x4c' , '\x36' , '\x02' , '\xe7' , '\xa0' , '\xc4' , '\xc8' , '\x9e',  
    '\xea' , '\xbf' , '\x8a' , '\xd2' , '\x40' , '\xc7' , '\x38' , '\xb5' , '\xa3' , '\xf7' , '\xf2' , '\xce' , '\xf9' , '\x61' , '\x15' , '\xa1',  
    '\xe0' , '\xae' , '\x5d' , '\xa4' , '\x9b' , '\x34' , '\x1a' , '\x55' , '\xad' , '\x93' , '\x32' , '\x30' , '\xf5' , '\x8c' , '\xb1' , '\xe3',  
    '\x1d' , '\xf6' , '\xe2' , '\x2e' , '\x82' , '\x66' , '\xca' , '\x60' , '\xc0' , '\x29' , '\x23' , '\xab' , '\x0d' , '\x53' , '\x4e' , '\x6f',  
    '\xd5' , '\xdb' , '\x37' , '\x45' , '\xde' , '\xfd' , '\x8e' , '\x2f' , '\x03' , '\xff' , '\x6a' , '\x72' , '\x6d' , '\x6c' , '\x5b' , '\x51',  
    '\x8d' , '\x1b' , '\xaf' , '\x92' , '\xbb' , '\xdd' , '\xbc' , '\x7f' , '\x11' , '\xd9' , '\x5c' , '\x41' , '\x1f' , '\x10' , '\x5a' , '\xd8',  
    '\x0a' , '\xc1' , '\x31' , '\x88' , '\xa5' , '\xcd' , '\x7b' , '\xbd' , '\x2d' , '\x74' , '\xd0' , '\x12' , '\xb8' , '\xe5' , '\xb4' , '\xb0',  
    '\x89' , '\x69' , '\x97' , '\x4a' , '\x0c' , '\x96' , '\x77' , '\x7e' , '\x65' , '\xb9' , '\xf1' , '\x09' , '\xc5' , '\x6e' , '\xc6' , '\x84',  
    '\x18' , '\xf0' , '\x7d' , '\xec' , '\x3a' , '\xdc' , '\x4d' , '\x20' , '\x79' , '\xee' , '\x5f' , '\x3e' , '\xd7' , '\xcb' , '\x39' , '\x48']
    if Act == 1 :
        for i in range (0,4) :
            out = out + Sbox[ord(reg[i])]
    else :
        for i in range (0,4) :
            out = out + chr(Sbox.index(reg[i]))
    return reg

def functionT( Attr , RK , Act , i ) :
    if Act == 1 :
        reg = strxor( strxor( Attr[4:8] , Attr[8:12] , 4 ) , strxor( Attr[12:16] , RK[i] , 4 ) , 4 )
        reg = SearchSbox ( reg , 1 )
    else :
        reg = strxor( strxor( Attr[4:8] , Attr[8:12] , 4 ) , strxor( Attr[12:16] , RK[31-i] , 4 ) , 4 )
        reg = SearchSbox ( reg , -1 )
    reg = strxor( strxor( strxor( reg , strldc(reg,2) , 4 ) , strxor( strldc(reg,10) , strldc(reg,18) , 4 ) , 4 ) , strldc(reg,24) , 4 )
    Attr = Attr[4:16] + strxor(Attr[0:4],reg,4)
    return Attr

def functionTK( Attr , CK , i ) :
    reg = strxor( strxor( Attr[4:8] , Attr[8:12] , 4 ) , strxor( Attr[12:16] , CK[i] , 4 ) , 4 )
    reg = SearchSbox ( reg , 1 )
    reg = strxor( strxor( reg , strldc(reg,13) , 4 ) , strldc(reg,23) , 4 )
    Attr = Attr[4:16] + strxor(Attr[0:4],reg,4)
    return Attr

###################################    MAIN   FUNCTION    ################################
##初始化，载入主密钥、系统参数和固定参数
CK = [ '\x00\x07\x0e\x15' , '\x1c\x23\x2a\x31' , '\x38\x3f\x46\x4d' , '\x54\x5b\x62\x69' , '\x70\x77\x7e\x85' , '\x8c\x93\x9a\xa1' , '\xa8\xaf\xb6\xbd' , '\xc4\xcb\xd2\xd9' ,
    '\xe0\xe7\xee\xf5' , '\xfc\x03\x0a\x11' , '\x18\x1f\x26\x2d' , '\x34\x3b\x42\x49' , '\x50\x57\x5e\x65' , '\x6c\x73\x7a\x81' , '\x88\x8f\x96\x9d' , '\xa4\xab\xb2\xb9' ,
    '\xc0\xc7\xce\xd5' , '\xdc\xe3\xea\xf1' , '\xf8\xff\x06\x0d' , '\x14\x1b\x22\x29' , '\x30\x37\x3e\x45' , '\x4c\x53\x5a\x61' , '\x68\x6f\x76\x7d' , '\x84\x8b\x92\x99' ,
    '\xa0\xa7\xae\xb5' , '\xbc\xc3\xca\xd1' , '\xd8\xdf\xe6\xed' , '\xf4\xfb\x02\x09' , '\x10\x17\x1e\x25' , '\x2c\x33\x3a\x41' , '\x48\x4f\x56\x5d' , '\x64\x6b\x72\x79' ]
MK = ""
while len(MK) < 16 :
    MK = input( "请输入本次服务的SM4主密钥：" )
    ##这里一定要对 MK 的长度进行检测，以确保不会出现错误！
    if len(MK) >= 16 :
        MK = MK[0:16]
    else :
        print( "密钥长度不足，请至少输入128bit数据，我们将截取您的前128bit数据作为主密钥" )
    print ( "MK =" , MK )
    ##↓这是系统参数，由于每个系统在安装时都会确定该值，通常不与用户互动，这里我们直接写一个128bit的常量到代码中即可
FK = "ZhaoWenhao155104"
FK = FK[0:16]
    ##开始进行密钥扩展
print( "轮密钥生成中……" )
RK = []
Attr = strxor( MK , FK , 16 )
for i in range (0,32):
    Attr = functionTK( Attr , CK , i )
    RK.append( Attr[12:16] )
    print( "RK [" , i+1 , "]" , str2hex(RK[i]) )
    ##加密轮函数启动
plain = ""
while len(plain) < 16 :
    plain = input( "正在准备启动SM4算法，请输入明文：" )
    if len(plain) >= 16 :
        plain = plain[0:16]
    else :
        print( "明文长度不足，请至少输入128bit数据，我们将截取您的前128bit数据作为明文" )
    print ( " plain =" , str2hex(plain) )
Attr = plain
for i in range (0,32) :
    Attr = functionT( Attr , RK , 1 , i )
cipher = Attr[12:16] + Attr[8:12] + Attr[4:8] + Attr[0:4]
print( "cipher =" , str2hex(cipher) )
    ##加密轮函数启动
print("测试程序自动验证解密的正确性，正在解密……")
Attr = cipher
for i in range (0,32) :
    Attr = functionT( Attr , RK , 0 , i )
plain_2 = Attr[12:16] + Attr[8:12] + Attr[4:8] + Attr[0:4]
print( "decrypt=" , str2hex(plain_2) )
import itchat
import requests
import time
from itchat.content import TEXT

def getAutoMessage(message=u'你好'):
    tulingUrl='http://www.tuling123.com/openapi/api'
    data = {
        'key'   :'a4813bab8faa4cadbb1a6a298f46c6b0',
        'info'  :message,
        'userid':'wechat-robot'
    }
    data['info']=message
    getmessage=requests.post(tulingUrl,data=data).json()
    return getmessage

itchat.auto_login(enableCmdQR=0.5)
RawRoomList = itchat.get_chatrooms()

RoomList=[]
for room in RawRoomList :
    RoomList.append({'NickName':room['NickName'],'UserName':room['UserName']})
print("\n#####################################群聊列表如下#################################################\n")
for i in range(len(RawRoomList)):
    print(str(i)+':'+RoomList[i]['NickName'])
print("\n#########################输入需要自动回复的群序号(若多个用逗号隔开)#################################\n")
AutoList = list(input())
AutoUserName=[]
AutoNickName=[]
for i in AutoList:
    if i!=',':
        AutoUserName.append(RoomList[int(i)]['UserName'])
        AutoNickName.append(RoomList[int(i)]['NickName'])
AutomemberList = itchat.update_chatroom(AutoUserName,detailedMember=True)
AutomemberAlias=[]
AutomemberNickName=[]
if not isinstance(AutomemberList,list):
    AutomemberList=[AutomemberList]
for i in AutomemberList:
    tempAlias=[]
    temNickName=[]
    for j in i['MemberList'] :
        tempAlias.append(j['Alias'])
        temNickName.append(j['NickName'])
    AutomemberAlias.append(tempAlias)
    AutomemberNickName.append(temNickName)
print("\n################################以下群将开启自动回复###############################################\n")
for i in range(len(AutoUserName)):
    print('群：%-10s 成员：%s 成员昵称：%s' % (AutoNickName[i],AutomemberAlias[i],AutomemberNickName[i]))
print("\n###################################开始自动回复###################################################\n")

@itchat.msg_register(TEXT,isGroupChat = True)
def text_replay(msg):
    if msg['ToUserName'] in AutoUserName :
        toUserName=msg['ToUserName']
    elif msg['FromUserName'] in AutoUserName: 
        toUserName=msg['FromUserName']
    else:
        toUserName=None
    if(toUserName!=None):
        getMessage=getAutoMessage(message=msg['Content'])['text']
        itchat.send_msg(msg=getMessage+'------我是狼崽，我爱笆笆',toUserName=toUserName)
        toNickName=AutoNickName[AutoUserName.index(toUserName)]
        print('%-20s 来自群：%-10s 成员：%-10s 内容：%s   回复:%s' % (time.ctime(msg['CreateTime']),toNickName,msg['ActualNickName'] ,msg['Content'],getMessage))
        f = open('log.txt','a')
        f.write('%-20s 来自群：%-10s 成员：%-10s 内容：%s   回复:%s\n' % (time.ctime(msg['CreateTime']),toNickName,msg['ActualNickName'] ,msg['Content'],getMessage))
        f.close()
itchat.run()


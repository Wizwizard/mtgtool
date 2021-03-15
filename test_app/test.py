import requests

url = "http://0.0.0.0:8888/wx"
# url = "http://47.117.130.253:8888/wx"

response = requests.get(url)
content = "a"
d = {
    'ToUserName': "ToUserName",
    'FromUserName': "FromUserName",
    'CreateTime': '1460537339',
    'MsgType': 'txt',
    'Content': content,
    'MsgId': '6272960105994287618'
}
data_str = '''
<xml>
 <ToUserName><![CDATA[ToUserName]]></ToUserName>
 <FromUserName><![CDATA[FromUserName]]></FromUserName>
 <CreateTime>1460537339</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[%s]]></Content>
 <MsgId>6272960105994287618</MsgId>
</xml>
'''
while True:
    content = input("input:")
    if content == "exit":
        break
    data = data_str % content
    response = requests.post(url, data=data)
    print(response.text)


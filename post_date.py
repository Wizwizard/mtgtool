import requests


url = "http://0.0.0.0:8080/wx"
data = '''<xml><ToUserName><![CDATA[gh_34df0ef31a9e]]></ToUserName>\n<FromUserName><![CDATA[oaFFiwK
g9ehZRRi8PEceOTk7kaeQ]]></FromUserName>\n<CreateTime>1605153417</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n
<Content><![CDATA[%s]]></Content>\n<MsgId>22980272567116370</MsgId>\n</xml>'''

while True:
    content = input()
    send_data = data % content
    requests.post(url, send_data)
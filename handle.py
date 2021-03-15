import hashlib
import web
import lxml
import time
import os
import reply
import receive
import mtgazone_crawler
import db
import math
import CONSTANT
import re

class Handle(object):
    _message_list = []
    # user_id: (level, menu, meta)
    # level: 1-meta select 2-deck select
    # menu: keep current menu str
    # meta: 0-init 1-standard, 2-historic
    META_SELECT = "输入序号查看对应环境最新20套牌\n1.标准\n2.史迹"
    DECK_SELECT = "输入序号获取对应套牌code\n"
    _user_status_list = {}
    _user_list = []
    _meta_list = [0, "standard", "historic"]
    _standard_list = []
    _historic_list = []
    _deck_upd_ts = math.floor(time.time())

    def __init__(self):
        self.init_deck_list()

    def upd_deck_list(self):
        cur_ts = math.floor(time.time()) 
        if (cur_ts - self._deck_upd_ts) > 7200:
            self.init_deck_list()
            self._deck_upd_ts = cur_ts
            print("%s 套牌更新" % cur_ts)

    def init_deck_list(self):
        standard_decks = db.select_deck_name_by_meta(1)
        historic_decks = db.select_deck_name_by_meta(2)

        tmp_standard_list = []
        tmp_historic_list = []

        for deck in standard_decks:
            deck_name = deck[0]
            deck_code = deck[1]
            for keyword_US_CN in CONSTANT.keywords_US_CN:
                deck_name = re.sub(keyword_US_CN[0] + " ", keyword_US_CN[1], deck_name, flags=re.IGNORECASE)
            tmp_standard_list.append((deck_name, deck_code))

        for deck in historic_decks:
            deck_name = deck[0]
            deck_code = deck[1]
            for keyword_US_CN in CONSTANT.keywords_US_CN:
                deck_name = re.sub(keyword_US_CN[0] + " ", keyword_US_CN[1], deck_name, flags=re.IGNORECASE)
            tmp_historic_list.append((deck_name, deck_code))

        self._standard_list = tmp_standard_list
        self._historic_list = tmp_historic_list

    def is_int(self, s):
        try:
            int(s)
            return True
        except ValueError as err:
            pass
        return False

    def deck_menu_generate(self, deck_list):
        deck_menu = Handle.DECK_SELECT
        index = 1
        opt = "%s.%s\n"
        for deck in deck_list:
            deck_name = deck[0]
            deck_menu += opt % (index, deck_name)
            index += 1
        deck_menu += "0.显示当前菜单\n-1.返回环境选择"
        return deck_menu

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "migongzhongdian"
            
            l = [token, timestamp, nonce]
            l.sort()
            sha1 = hashlib.sha1()
            sha1.update("".join(l).encode())
            # map(sha1.update, l)
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            # print("Handle Post webdata is ", webData)
            recMsg = receive.parse_xml(webData)
            # if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            if recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = self.distribute(recMsg)
                if content == "":
                    return "success"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                replyMsg_send = replyMsg.send()
                #print(replyMsg_send)
                return replyMsg_send
            else:
                # print("其他类型暂且不处理")
                return "success"
        except Exception as Argment:
            print(Argment)
            return Argment

    # 处理分配
    def distribute(self, recMsg):
        toUser = recMsg.FromUserName
        content = recMsg.Content
        print("distribute:" + content)
        # print(self._user_list)
        # print(self._message_list)
        if content == "mtg":
            print("开门")
            if toUser not in self._user_list:
                self._user_list.append(toUser)
                # print(self._standard_list)
                # print(self._historic_list)
                level = 1
                meta = 0
                menu = self.META_SELECT
                self._user_status_list[toUser] = (level, menu, meta)
                content = menu
            else:
                # 重置状态
                level = 1
                meta = 0
                menu = self.META_SELECT
                self._user_status_list[toUser] = (level, menu, meta)
                content = menu
        elif toUser in self._user_list:
            print("接待用户")
            if self.is_int(content):
                index = int(content)
                user_status = self._user_status_list[toUser]
                user_level = user_status[0]
                user_menu = user_status[1]
                user_meta = user_status[2]
                # meta select
                if user_level == 1:
                    if index == 0:
                        content = user_menu
                    elif index == 1:
                        user_level = 2
                        user_menu = self.deck_menu_generate(self._standard_list[:20])
                        user_meta = index
                        content = user_menu
                        self._user_status_list[toUser] = (user_level, user_menu, user_meta)
                    elif index == 2:
                        user_level = 2
                        user_menu = self.deck_menu_generate(self._historic_list[:20])
                        user_meta = index
                        content = user_menu
                        self._user_status_list[toUser] = (user_level, user_menu, user_meta)
                    else:
                        content = "请发送菜单选项对应数字！\n发送0可以获取当前菜单"
                # deck select
                elif user_level == 2:
                    # 检查牌表是否过期，过期则更新
                    self.upd_deck_list()
                    if index == 0:
                        content = user_menu
                    elif index == -1:
                        user_level = 1
                        user_menu = self.META_SELECT
                        user_meta = 0
                        self._user_status_list[toUser] = (user_level, user_menu, user_meta)
                        content = user_menu

                    elif 0 < index < 16:
                        if user_meta == 1:
                            deck_code = self._standard_list[index - 1][1]
                            content = deck_code
                        elif user_meta == 2:
                            deck_code = self._historic_list[index - 1][1]
                            content = deck_code
                        else:
                            content = ""
                    else:
                        content = "请发送菜单选项对应数字！\n发送0可以获取当前菜单"
                else:
                    content = "出问题啦，请qq群联系大白!"
            else:
                content = "请发送菜单选项对应数字！\n发送0可以获取当前菜单"
        else:
            content = ""
        return content





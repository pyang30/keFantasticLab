#!/bin/env python
import tornado.ioloop
import tornado.web
from expiringdict import ExpiringDict
from menu import menu
import hashlib
from lxml import etree
import os
from string import Template
import wx_conf

root_menu = None
cache = ExpiringDict(max_len=100, max_age_seconds=4)

def init_menu():
    global root_menu
    root_menu = []
    for m in menu:
        if m['parent_id'] == 0:
            root_menu.append(m)


def get_menu_by_id(mid):
    for m in menu:
        if m['id'] == mid:
            return m


def sub_menu(parent_id):
    subs = []
    for m in menu:
        if m["parent_id"] == parent_id:
            subs.append(m)
    return subs


def sibling_menu(mid):
    m = get_menu_by_id(mid)
    return sub_menu(m['parent_id'])

# 当前menu的上一层menu
def parent_menu(mid):
    m = get_menu_by_id(mid)
    parent_id = m['parent_id']
    if parent_id == 0:
        return root_menu
    return sibling_menu(parent_id)



def current_menu(user):
    # 用户操作超时，从头开始显示菜单
    if cache.get(user) is None:
        cache[user] = root_menu
    return cache[user]

def set_cur_menu(user, menu):
    cache[user] = menu

# 用户操作是否超时
def user_menu_reseted(user):
    return cache.get(user) == False

def print_cur_menu(user):
    cur_menu = current_menu(user)
    for idx in range(len(cur_menu)):
        print("%s: %s" % (idx+1, cur_menu[idx]['menu']))

def cur_menu_text(user):
    cur_menu = current_menu(user)
    str_menu = "请选择(上一层请按*， 主菜单请按#):\n"
    for idx in range(len(cur_menu)):
        str_menu += "%d\t: %s\n" % (idx+1, cur_menu[idx]['menu'])

    return str_menu


def get_user_menu(user, ipt):
    if ipt != "*" and ipt != "#" and not ipt.isdigit():
        return cur_menu_text(user)

    if ipt == "*":
        mid = current_menu(user)[0]['id']
        menus = parent_menu(mid)
        set_cur_menu(user, menus)
        return cur_menu_text(user)

    elif ipt == "#":
        return cur_menu_text(user)

    elif user_menu_reseted(user):
        return cur_menu_text(user)

    elif int(ipt) <= 0 or int(ipt) > len(current_menu(user)):
        return cur_menu_text(user)

    else:
        selected_menu = current_menu(user)[int(ipt)-1]
        if sub_menu(selected_menu['id']):
            set_cur_menu(user, sub_menu(selected_menu['id']))
            return cur_menu_text(user)
        else:
            return cur_menu_text(user)

    # idx = int(ipt)
    # print(cache.get("root")[idx-1])


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')

        token = wx_conf.TOKEN
        tmpl = [token, timestamp, nonce]
        tmpl.sort()
        s = tmpl[0] + tmpl[1] + tmpl[2]
        hashcode = hashlib.sha1(s.encode("utf-8")).hexdigest()

        if hashcode == signature:
            self.write(echostr)

        self.write("")


    def make_response(self, params):
        template = Template(wx_conf.WX_RESP_MSG_TEMPLATE)
        response = template.safe_substitute(**params)
        # print("response = ", response)
        return response

    def post(self):
        body = self.request.body
        xml = etree.fromstring(body)

        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        msgId = xml.find("MsgId").text
        createTime = xml.find("CreateTime").text
        content = xml.find("Content").text  #获得用户所输入的内容

        content = get_user_menu(fromUser, content)

        print("return to %s, msg: \n%s" % (fromUser, content))

        resp = {
            "toUser": fromUser,
            "fromUser": toUser,
            "createTime": createTime,
            "msgType": msgType,
            "content": content
        }

        self.write(self.make_response(resp))


def make_app():
    return tornado.web.Application([
        (r"/wx/", MainHandler),
    ])

if __name__ == "__main__":
    init_menu()

    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()


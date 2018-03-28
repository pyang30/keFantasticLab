#!/bin/env python
import tornado.ioloop
import tornado.web
from expiringdict import ExpiringDict
from menu import menu
import hashlib

root_menu = None
cache = ExpiringDict(max_len=100, max_age_seconds=2)

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


init_menu()

def current_menu():
    # 用户操作超时，从头开始显示菜单
    if cache.get("root") is None:
        cache['root'] = root_menu
    return cache['root']

def set_cur_menu(menu):
    cache['root'] = menu

# 用户操作是否超时
def user_menu_reseted():
    return cache.get('root') == False

def print_cur_menu():
    cur_menu = current_menu()
    for idx in range(len(cur_menu)):
        print("%s: %s" % (idx+1, cur_menu[idx]['menu']))


# print_cur_menu()
# while True:
#     ipt = input("请选择(上一层请按*， 主菜单请按#):")
#     if ipt != "*" and ipt != "#" and not ipt.isdigit():
#         continue

#     if ipt == "*":
#         mid = current_menu()[0]['id']
#         menus = parent_menu(mid)
#         set_cur_menu(menus)
#         print_cur_menu()

#     elif ipt == "#":
#         pass

#     elif user_menu_reseted():
#         continue

#     elif int(ipt) <= 0 or int(ipt) > len(current_menu()):
#         print_cur_menu()

#     else:
#         selected_menu = current_menu()[int(ipt)-1]
#         print(selected_menu)
#         if sub_menu(selected_menu['id']):
#             set_cur_menu(sub_menu(selected_menu['id']))
#             print_cur_menu()
#         else:
#             print_cur_menu()

#     # idx = int(ipt)
#     # print(cache.get("root")[idx-1])


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')

        token = "uiNUKsb"
        tmpl = [token, timestamp, nonce]
        tmpl.sort()
        s = tmpl[0] + tmpl[1] + tmpl[2]
        hashcode = hashlib.sha1(s.encode("utf-8")).hexdigest()

        if hashcode == signature:
            self.write(echostr)

        self.write("")

    def post(self):
        print("post")
        print(self.request.body)
        self.write("")


def make_app():
    return tornado.web.Application([
        (r"/wx/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()


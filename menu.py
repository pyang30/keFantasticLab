#!/bin/env python

# menu format
# id, parent_id, menu, desc

menu = [
    # 0级菜单
    {
        "id": 0,
        "parent_id": -1,
        "menu": "root",
        "desc": "root",
    },

    # 一级菜单
    {
        "id": 1,
        "parent_id": 0,
        "menu": "主菜单1",
        "desc": "root",
    },
    {
        "id": 2,
        "parent_id": 0,
        "menu": "主菜单2",
        "desc": "root",
    },
    {
        "id": 3,
        "parent_id": 0,
        "menu": "主菜单3",
        "desc": "root",
    },
    {
        "id": 4,
        "parent_id": 0,
        "menu": "主菜单4",
        "desc": "root",
    },

    # 二级菜单
    {
        "id": 5,
        "parent_id": 1,
        "menu": "菜单1-1",
        "desc": "root",
    },
    {
        "id": 6,
        "parent_id": 1,
        "menu": "菜单1-2",
        "desc": "root",
    },

    {
        "id": 7,
        "parent_id": 2,
        "menu": "菜单2-1",
        "desc": "root",
    },
    {
        "id": 8,
        "parent_id": 2,
        "menu": "菜单2-2",
        "desc": "root",
    },

    {
        "id": 9,
        "parent_id": 3,
        "menu": "菜单3-1",
        "desc": "root",
    },
    {
        "id": 10,
        "parent_id": 3,
        "menu": "菜单3-2",
        "desc": "root",
    },

    {
        "id": 11,
        "parent_id": 4,
        "menu": "菜单4-1",
        "desc": "root",
    },
    {
        "id": 12,
        "parent_id": 4,
        "menu": "菜单4-2",
        "desc": "root",
    },

]
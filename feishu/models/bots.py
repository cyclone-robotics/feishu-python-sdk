#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bot类型"""
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class BotActivateStatus(int, Enum):
    """
     0: 初始化，租户待安装,
     1: 租户停用,
     2: 租户启用,
     3: 安装后待启用,
     4: 升级待启用,
     5: license过期停用,
     6: Lark套餐到期或降级停用,
    """
    INITIALIZED = 0
    DISABLED = 1
    ENABLED = 2
    INSTALLED = 3
    UPGRADED = 4
    LICENCE_EXPIRED = 5
    SET_EXPIRED = 6


class BotChatType(str, Enum):
    GROUP = "group"
    P2P = "p2p"


class BotInfo(BaseModel):
    """
    {
        "activate_status": 2,
        "app_name": "name",
        "avatar_url": "https://sf1-ttcdn-tos.pstatp.com/obj/lark.avatar/da5xxxx14b16113",
        "ip_white_list": [],
        "open_id": "ou_xxx"
    }
    """
    activate_status: BotActivateStatus
    app_name: str
    avatar_url: str
    ip_white_list: List[str]
    open_id: str


class I18Names(BaseModel):
    zh_cn: str
    en_us: str


class CreateChatRequest(BaseModel):
    """创建群请求
    {
        "name": "group name",
        "description": "group description",
        "user_ids": [
            "33417745",
            "cb93bdca"
        ],
        "open_ids": [
            "ou_4065981088f8ef67a504ba8bd6b24d85",
            "ou_111111111111111111111111111111111"
        ],
        "i18n_names": {
            "zh_cn": "zh_cn name",
            "en_us": "en_us name",
            "ja_jp": "ja_jp name"
        },
        "only_owner_add": false,
        "share_allowed": true,
        "only_owner_at_all": false,
        "only_owner_edit": false
    }
    """
    name: str = ''
    description: str = ''
    open_ids: List[str] = []
    user_ids: List[str] = []
    i18_names: I18Names
    only_owner_add: bool = False
    share_allowed: bool = True
    only_owner_at_all: bool = False
    only_owner_edit: bool = False


class CreateChatResponse(BaseModel):
    """创建群返回
    {
        "chat_id": "oc_4f65b883a624c59414157668c91637ab",
        "invalid_open_ids": [
            "ou_111111111111111111111111111111111"
        ],
        "invalid_user_ids": [
            "33417745"
        ]
    }
    """
    chat_id: str = ''
    invalid_open_ids: List[str] = []
    invalid_user_ids: List[str] = []


AddChatterResponse = CreateChatResponse
RemoveChatterResponse = CreateChatResponse


class ChatMember(BaseModel):
    open_id: str
    user_id: str


class ChatInfo(BaseModel):
    avatar: str = ''
    description: str = ''
    chat_id: str = ''
    name: str = ''
    owner_open_id: str = ''
    owner_user_id: str = ''

    # only available in get_chat_info API
    i18n_names: I18Names = {}
    members: List[ChatMember] = []
    type: BotChatType = "group"


class ChatPagination(BaseModel):
    """
    {
        "groups": [
            {
                "avatar": "http://p3.pstatp.com/origin/78c0000676df676a7f6e",
                "chat_id": "oc_9e9619b938c9571c1c3165681cdaead5",
                "description": "description1",
                "name": "test1",
                "owner_open_id": "ou_194911f90c43ec42d1ba0e93f22b8fb1",
                "owner_user_id": "ca51d83b"
            },
            {
                "avatar": "http://p4.pstatp.com/origin/dae10015cfb346541010",
                "chat_id": "oc_5ce6d572455d361153b7cb51da133945",
                "description": "description2",
                "name": "test2",
                "owner_open_id": "ou_194911f90c43ec42d1ba0e93f22b8fb1",
                "owner_user_id": "ca51d83b"
            }
        ],
        "has_more": false,
        "page_token": "0"
    }
    """
    has_more: bool = False
    page_token: str = '0'
    groups: List[ChatInfo] = []


class ChatUpdateRequest(BaseModel):
    """
    {
        "chat_id": "oc_020ff1d91a0295fc3961032768d41f39",
        "owner_user_id":"cb93bdca",
        "owner_open_id":"ou_4065981088f8ef67a504ba8bd6b24d85",
        "name":"group name",
        "i18n_names":{
            "zh_cn":"zh_cn name",
            "en_us":"en_us name",
            "ja_jp":"ja_jp name"
        },
        "only_owner_add": false,
        "share_allowed": true,
        "only_owner_at_all": false,
        "only_owner_edit": false
    }
    """
    chat_id: str
    owner_open_id: str = ''
    owner_user_id: str = ''
    name: str = ''
    i18n_names: I18Names = {}

    only_owner_add: Optional[bool] = None
    share_allowed: Optional[bool] = None
    only_owner_at_all: Optional[bool] = None
    only_owner_edit: Optional[bool] = None

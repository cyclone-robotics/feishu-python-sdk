#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from typing import List, Union, Optional

from pydantic import BaseModel


class SendMsgType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    POST = "post"
    SHARE_CHAT = "share_chat"
    INTERACTIVE = "interactive"


class PostTag(str, Enum):
    TEXT = "text"
    A = "a"
    AT = "at"
    IMG = "img"


class Content(BaseModel):
    pass


class TextContent(Content):
    text: str


class ImageContent(Content):
    image_key: str


class ShareChatContent(Content):
    share_chat_id: str


class PostElement(BaseModel):
    tag: PostTag


class PostTextElement(PostElement):
    """文本元素
    {
        "tag": "text",
        "un_escape": true,
        "text": "第一行&nbsp;:"
    }
    """
    tag: PostTag = PostTag.TEXT
    text: str
    un_escape: Optional[bool] = None


class PostAElement(PostElement):
    """超链接元素
    {
        "tag": "a",
        "text": "超链接",
        "href": "http://www.feishu.cn"
    }
    """
    tag: PostTag = PostTag.A
    text: str
    href: str
    un_escape: Optional[bool] = None


class PostAtElement(PostElement):
    """AT元素

    user_id可以是open_id/user_id
    {
        "tag": "at",
        "user_id": "ou_18eac85d35a26f989317ad4f02e8bbbb"
    }
    """
    tag: PostTag = PostTag.AT
    user_id: str


class PostImgElement(PostElement):
    """图片元素

    {
        "tag": "img",
        "image_key": "d640eeea-4d2f-4cb3-88d8-c964fab53987",
        "width": 300,
        "height": 300
    }
    """
    tag: PostTag = PostTag.IMG
    image_key: str
    height: int
    width: int


class I18nPost(BaseModel):
    """Post内容

    https://open.feishu.cn/document/ukTMukTMukTM/uMDMxEjLzATMx4yMwETM

    效果:
    https://sf1-ttcdn-tos.pstatp.com/obj/website-img/a3074630f25fb0e7d3df394c1348ba41_cn.png
    {
        "title": "我是一个标题",
        "content": [
            [
                {
                    "tag": "text",
                    "un_escape": true,
                    "text": "第一行&nbsp;:"
                },
                {
                    "tag": "a",
                    "text": "超链接",
                    "href": "http://www.feishu.cn"
                },
                {
                    "tag": "at",
                    "user_id": "ou_18eac85d35a26f989317ad4f02e8bbbb"
                }
            ],
            [
                {
                    "tag": "text",
                    "text": "第二行 :"
                },
                {
                    "tag": "text",
                    "text": "文本测试"
                }
            ],
            [
                {
                    "tag": "img",
                    "image_key": "d640eeea-4d2f-4cb3-88d8-c964fab53987",
                    "width": 300,
                    "height": 300
                }
            ]
        ]
    }
    """
    title: Optional[str] = None
    content: List[List[PostElement]]


class Post(BaseModel):
    """ 这里暂未处理i18n相关, 其实可以都列一下 """
    zh_cn: Optional[Union[I18nPost, dict]] = None
    en_us: Optional[Union[I18nPost, dict]] = None


class PostContent(Content):
    post: Post


class Message(BaseModel):
    """消息基类

    Args:
        chat_id 同下
        open_id 同下
        user_id 同下
        email 如下
            - 私聊的话open_id/user_id/email三个里面要填一个
            - 群聊的话必须填chat_id
            - 如果都提供的话，优先级为 chat_id > open_id > user_id > email
        root_id 回复消息时，对应消息的消息ID，选填
        msg_type 消息类型, 见MsgType
        content 消息内容, 见Content
    """
    chat_id: Optional[str] = None
    open_id: Optional[str] = None
    user_id: Optional[str] = None
    email: Optional[str] = None
    root_id: Optional[str] = None
    msg_type: SendMsgType
    content: Content


class TextMessage(Message):
    """文本消息

    {
       "open_id":"ou_5ad573a6411d72b8305fda3a9c15c70e",
       "root_id":"om_40eb06e7b84dc71c03e009ad3c754195",
       "chat_id":"oc_5ad11d72b830411d72b836c20",
       "user_id": "92e39a99",
       "email":"fanlv@gmail.com",
       "msg_type":"text",
       "content":{
            "text":"text content<at user_id=\"ou_88a56e7e8e9f680b682f6905cc09098e\">test</at>"
        }
    }
    """
    msg_type: SendMsgType = SendMsgType.TEXT
    content: TextContent


class ImageMessage(Message):
    """图片消息

    {
       "open_id":"ou_5ad573a6411d72b8305fda3a9c15c70e",
       "chat_id":"oc_5ad11d72b830411d72b836c20",
       "root_id":"om_40eb06e7b84dc71c03e009ad3c754195",
        "user_id": "92e39a99",
        "email":"fanlv@gmail.com",
        "msg_type":"image",
        "content":{
            "image_key": "1a0c4cb9-c680-4371-924c-ddb5f2750c3d"
        }
    }
    """
    msg_type: SendMsgType = SendMsgType.IMAGE
    content: ImageContent


class PostMessage(Message):
    """富文本消息

    {
       "open_id":"ou_5ad573a6411d72b8305fda3a9c15c70e",
       "root_id":"om_40eb06e7b84dc71c03e009ad3c754195",
       "chat_id":"oc_5ad11d72b830411d72b836c20",
       "user_id": "92e39a99",
       "email":"fanlv@gmail.com",
       "msg_type":"post",
       "content":{
            "post":{
                "zh_cn":{}, // option
                "ja_jp":{}, // option
                "en_us":{} // option
            }
       }
    }
    """
    msg_type: SendMsgType = SendMsgType.POST
    content: PostContent


class ShareChatMessage(Message):
    """群名片

    {
       "open_id":"ou_5ad573a6411d72b8305fda3a9c15c70e",
       "root_id":"om_40eb06e7b84dc71c03e009ad3c754195",
       "chat_id":"oc_5ad11d72b830411d72b836c20",
       "user_id": "92e39a99",
        "msg_type": "share_chat",
        "content":{
            "share_chat_id": "oc_f5b1a7eb27ae2c7b6adc2a74faf339ff"
        }
    }
    """
    msg_type: SendMsgType = SendMsgType.SHARE_CHAT
    content: ShareChatContent


class ReadUser(BaseModel):
    """已读用户

    {
        "open_id": "ou_18eac85d35a26f989317ad4f02e8bbbb",
        "timestamp": "1570697776",
        "user_id": "ca51d83b"
    }
    """
    open_id: str
    timestamp: str
    user_id: Optional[str] = None


class BatchMessage(BaseModel):
    """批量消息

    {
        "department_ids": [
            "od-9d1912863dceba33a33226b52b32a776",
            "od-81d13d502aaa9514059ea570c37d6438"
        ],
        "open_ids": [
            "ou_18eac85d35a26f989317ad4f02e8bbbb",
            "ou_461cf042d9eedaa60d445f26dc747d5e"
        ],
        "user_ids": [
            "7cdcc7c2",
            "ca51d83b"
        ],
        "msg_type": "text",
        "content": {
            "text": "test content"
        }
    }
    """
    department_ids: List[str] = []
    open_ids: List[str] = []
    user_ids: List[str] = []
    msg_type: SendMsgType
    content: Content


class BatchSendResponse(BaseModel):
    """批量发送消息返回

    {
        "invalid_department_ids": [
            "od-d3079cfb6ed783b9bdc2e9eac04e85b41"
        ],
        "invalid_open_ids": [
            "ou_456e168d61cec276083b357f7bd3f1491",
            "ou_f8cbdb26fb2e4eda075e003381a102a41"
        ],
        "invalid_user_ids": ["7cdcc7c22"],
        "message_id": "bm-d4be107c616aed9c1da8ed8068570a9f"
    }
    """
    message_id: str
    message_ids: List[str] = []  # 拆分成多个请求的话会有多个message_id
    invalid_department_ids: List[str] = []
    invalid_open_ids: List[str] = []
    invalid_user_ids: List[str] = []

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""消息卡片

https://open.feishu.cn/document/ukTMukTMukTM/uczM3QjL3MzN04yNzcDN
"""
from enum import Enum
from typing import List, Optional, Union, Literal

from pydantic import BaseModel, Field

from .message import SendMsgType


class CardTag(str, Enum):
    # tag for TextObject
    PLAIN_TEXT = "plain_text"
    LARK_MD = "lark_md"

    # tag for CardModule
    DIV = "div"
    HR = "hr"
    IMG = "img"
    ACTION = "action"
    NOTE = "note"

    # tag for CardElement
    BUTTON = "button"
    SELECT_STATIC = "select_static"
    SELECT_PERSON = "select_person"
    OVERFLOW = "overflow"
    DATE_PICKER = "date_picker"
    PICKER_TIME = "picker_time"
    PICKER_DATETIME = "picker_datetime"

    # tag alias for 美学
    TIME_PICKER = PICKER_TIME
    DATETIME_PICKER = PICKER_DATETIME
    PICKER_DATE = DATE_PICKER


class CardTemplate(str, Enum):
    BLUE = "blue"
    WATHET = "wathet"
    TURQUOISE = "turquoise"
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"
    CARMINE = "carmine"
    VIOLET = "violet"
    PURPLE = "purple"
    INDIGO = "indigo"
    GREY = "grey"


class CardImgMode(str, Enum):
    FIT_HORIZONTAL = "fit_horizontal"
    CROP_CENTER = "crop_center"


class CardLayout(str, Enum):
    BISECTED = "bisected"
    TRISECTION = "trisection"
    FLOW = "flow"


class CardButtonType(str, Enum):
    DEFAULT = "default"
    PRIMARY = "primary"
    DANGER = "danger"


class CardObject(BaseModel):
    """卡片对象

    https://open.feishu.cn/document/ukTMukTMukTM/uUzNwUjL1cDM14SN3ATN
    """


class CardTextObject(CardObject):
    """text对象

    https://open.feishu.cn/document/ukTMukTMukTM/uUzNwUjL1cDM14SN3ATN

    {
        "tag": "plain_text",
        "content": "single line information",
        "lines": 1
    }
    {
        "tag": "plain_text",
        "template":
        "i18n": {
            "zh_cn": "中文文本",
            "en_us": "English text",
            "ja_jp": "日本語文案"
        }
    }
    """
    tag: CardTag = CardTag.PLAIN_TEXT
    content: str
    i18n: Optional[dict] = None
    lines: Optional[int] = None


class CardFieldObject(CardObject):
    """field对象

    https://open.feishu.cn/document/ukTMukTMukTM/uYzNwUjL2cDM14iN3ATN
    {
        "is_short": true,
        "text": {
            "tag": "plain_text",
            "content": "text"
        }
    }
    """
    is_short: bool
    text: CardTextObject


class CardURLObject(CardObject):
    """url对象

    https://open.feishu.cn/document/ukTMukTMukTM/uczNwUjL3cDM14yN3ATN

    {
        "url": "https://www.baidu.com",
        "android_url": "https://developer.android.com/",
        "ios_url": "https://developer.apple.com/",
        "pc_url": "https://www.windows.com"
    }
    """
    url: str
    android_url: str
    ios_url: str
    pc_url: str


class CardOptionObject(CardObject):
    """option对象

    https://open.feishu.cn/document/ukTMukTMukTM/ugzNwUjL4cDM14CO3ATN

    {
        "text": {
            "tag": "plain_text",
            "content": "Option"
        },
        "value": "option"
    }
    """
    text: Optional[CardTextObject] = None
    value: str
    url: Optional[str] = None
    multi_url: Optional[CardURLObject] = None


class CardConfirmObject(CardObject):
    """confirm对象

    https://open.feishu.cn/document/ukTMukTMukTM/ukzNwUjL5cDM14SO3ATN
    {
        "title":{
            "tag":"plain_text",
            "content":"title"
        },
        "text":{
            "tag":"plain_text",
            "content":"content"
        }
    }
    """
    title: CardTextObject
    text: CardTextObject


class CardElement(BaseModel):
    """元素"""
    tag: CardTag


class CardImageElement(CardElement):
    """image元素

    https://open.feishu.cn/document/ukTMukTMukTM/uAzNwUjLwcDM14CM3ATN
    放置在内容模块的extra的图片尺寸固定为64*64
    放置在备注模块的elements的图片尺寸固定为16*16
    {
        "tag": "img",
        "img_key": "f32**************************cf7",
        "alt": {
            "tag": "plain_text",
            "content": "Note image size：16*16"
        }
    }
    """
    tag: Literal[CardTag.IMG] = CardTag.IMG
    img_key: str
    alt: CardTextObject


class CardButtonElement(CardElement):
    """button元素

    https://open.feishu.cn/document/ukTMukTMukTM/uEzNwUjLxcDM14SM3ATN
    Args:
        url 跳转链接，和multi_url互斥
        multi_url 多端跳转链接
        type 样式
        value 交互元素的value字段值仅支持key-value形式的json结构，且key为String类型，示例如下：
                "value":{
                    "key-1":Object-1,
                    "key-2":Object-2,
                    "key-3":Object-3,
                        ······
                }
    整体示例
    {
        "tag":"button",
        "text":{
            "tag":"lark_md",
            "content":"default style"
        },
        "type":"default",
        "value":{
            "key":"value"
        }
    }
    """
    tag: Literal[CardTag.BUTTON] = CardTag.BUTTON
    text: CardTextObject
    url: Optional[str] = None
    multi_url: Optional[CardURLObject] = None
    type: Optional[CardButtonType] = None
    value: Optional[dict] = None
    confirm: Optional[CardConfirmObject] = None


class CardSelectElement(CardElement):
    """selectMenu元素

    https://open.feishu.cn/document/ukTMukTMukTM/uIzNwUjLycDM14iM3ATN
    selectMenu属于交互元素的一种，可用于内容块的extra字段和交互块的elements字段。

    选项模式（"tag":"select_static")：通过options字段配置选项，支持对多个选项进行展示供用户选择。
    选人模式（"tag":"select_person")：通过options字段配置待选人员，无则使用当前群组作为待选人员。

    {
        "tag": "select_static",
        "placeholder": {
            "tag": "plain_text",
            "content": "Option-common mode"
        },
        "value": {
            "key": "value"
        },
        "options": [
            {
                "text": {
                     "tag": "plain_text",
                     "content": "james"
                },
                "value": "james"
            },
            {
                "text": {
                    "tag": "plain_text",
                    "content": "joy"
                },
                "value": "joy"
            },
            {
                "text": {
                    "tag": "plain_text",
                    "content": "james_1"
                },
                "value": "james_1"
            },
            {
                "text": {
                    "tag": "plain_text",
                    "content": "joy_1"
                },
                "value": "joy_1"
            }
        ]
    }
    """
    tag: Literal[CardTag.SELECT_STATIC, CardTag.SELECT_PERSON] = CardTag.SELECT_STATIC
    placeholder: Optional[CardTextObject] = None
    initial_option: Optional[str] = None
    options: Optional[CardOptionObject] = None
    value: Optional[dict] = None
    confirm: Optional[CardConfirmObject] = None


class CardOverflowElement(CardElement):
    """overflow元素

    https://open.feishu.cn/document/ukTMukTMukTM/uMzNwUjLzcDM14yM3ATN
    {
        "tag": "overflow",
        "options": [
            {
                "text": {
                    "tag": "plain_text",
                    "content": "Option-1"
                },
                "value": "option-1"
            },
            {
                "text": {
                    "tag": "plain_text",
                    "content": "Option-2"
                },
                "value": "option-2"
            },
            {
                "text": {
                    "tag": "plain_text",
                    "content": "Option-3”
                },
                "value": "option-3"
            }
        ],
        "value": {
            "key": "value"
        }
    }
    """
    tag: Literal[CardTag.OVERFLOW] = CardTag.OVERFLOW
    options: List[CardOptionObject]
    value: Optional[dict] = None
    confirm: Optional[CardConfirmObject] = None


class CardPickerElement(CardElement):
    """datePicker元素

    https://open.feishu.cn/document/ukTMukTMukTM/uQzNwUjL0cDM14CN3ATN
    Args:
        tag 可以是"date_picker", "picker_time", "picker_datetime"
        initial_date "YYYY-MM-DD"
        initial_time "HH:mm"
        initial_datetime "YYYY-MM-DD HH:mm"
        placeholder 占位符, 无初始值时必填
    {
        "tag": "date_picker",
        "placeholder": {
            "tag": "plain_text",
            "content": "Please select date"
        },
        "value": {
            "key": "value"
        }
    }
    """
    tag: Literal[CardTag.DATE_PICKER] = CardTag.DATE_PICKER
    initial_date: Optional[str] = None
    initial_time: Optional[str] = None
    initial_datetime: Optional[str] = None
    placeholder: Optional[str] = None
    value: Optional[dict] = None
    confirm: Optional[CardConfirmObject] = None


CardGenericElement = Union[
    CardButtonElement, CardPickerElement, CardImageElement, CardSelectElement, CardOverflowElement, dict]


class CardConfig(BaseModel):
    """卡片配置

    https://open.feishu.cn/document/ukTMukTMukTM/uAjNwUjLwYDM14CM2ATN
    """
    wide_screen_mode: Optional[bool] = None
    enable_forward: Optional[bool] = None


class CardHeader(BaseModel):
    """卡片标题

    https://open.feishu.cn/document/ukTMukTMukTM/ukTNwUjL5UDM14SO1ATN
    """
    title: CardTextObject
    template: Optional[CardTemplate] = None


class CardModule(BaseModel):
    """模块"""
    tag: CardTag


class CardDivModule(CardModule):
    """内容模块

    https://open.feishu.cn/document/ukTMukTMukTM/uMjNwUjLzYDM14yM2ATN
    {
        "tag": "div",
        "text": {
            "tag": "plain_text",
            "content": "Content module"
        },
        "fields": [
            {
                "is_short": false,
                "text": {
                    "tag": "lark_md",
                    "content": "**module:**\nContent module（div）"
                }
            },
            {
                "is_short": false,
                "text": {
                    "tag": "lark_md",
                    "content": "**function:**\nNew function"
                }
            }
        ],
        "extra": {
            "tag": "img",
            "img_key": "f32******************5cf7",
            "alt": {
                "tag": "plain_text",
                "content": "alt_content"
            }
        }
    }
    """
    tag: Literal[CardTag.DIV] = CardTag.DIV
    text: CardTextObject
    fields_: List[CardFieldObject] = Field([], alias="fields")
    extra: Optional[CardGenericElement] = None


class CardHrModule(CardModule):
    """分割线模块
    {
        "tag": "hr",
    }
    """
    tag: Literal[CardTag.HR] = CardTag.HR


class CardImgModule(CardModule):
    """图片模块

    https://open.feishu.cn/document/ukTMukTMukTM/uUjNwUjL1YDM14SN2ATN
    {
        "tag":"img",
        "title":{
           "tag":"plain_text",
           "content":"Block-img"
        },
        "img_key":"9f6********************315",
        "alt":{
           "tag":"plain_text",
           "content":"Block-img"
        }
    }
    """
    tag: Literal[CardTag.IMG] = CardTag.IMG
    img_key: str
    alt: CardTextObject
    title: Optional[CardTextObject] = None
    mode: Optional[CardImgMode] = None


class CardActionModule(CardModule):
    """交互模块"""
    tag: Literal[CardTag.ACTION] = CardTag.ACTION
    actions: List[CardGenericElement]
    layout: Optional[CardLayout] = None


CardGenericModule = Union[CardHrModule, CardImgModule, CardActionModule, CardDivModule, dict]


class I18nContent(BaseModel):
    en_us: Optional[List[CardGenericModule]] = None
    zh_cn: Optional[List[CardGenericModule]] = None


class CardContent(BaseModel):
    config: Optional[CardConfig] = None
    header: Optional[CardHeader] = None
    card_link: Optional[CardURLObject] = None
    elements: Optional[List[CardGenericModule]] = None
    i18n_elements: Optional[I18nContent] = None


class CardMessage(BaseModel):
    """卡片消息

    https://open.feishu.cn/document/ukTMukTMukTM/uYTNwUjL2UDM14iN1ATN
    Args:
        chat_id 同下
        open_id 同下
        user_id 同下
        email 如下
            - 私聊的话open_id/user_id/email三个里面要填一个
            - 群聊的话必须填chat_id
            - 如果都提供的话，优先级为 chat_id > open_id > user_id > email
        root_id 回复消息时，对应消息的消息ID，选填
        msg_type 消息类型, = "interactive"
        card 卡片内容, 见CardContent
        update_multi 是否所有用户共享同一张卡片, 默认为False

    示例
    {
        "chat_id": "oc_abcdefg1234567890",
        "msg_type": "interactive",
        "root_id":"om_4*********************ad8",
        "update_multi":false,
        "card": {
                // card content
        }
    }
    """
    chat_id: Optional[str] = None
    open_id: Optional[str] = None
    user_id: Optional[str] = None
    email: Optional[str] = None
    root_id: Optional[str] = None
    msg_type: str = SendMsgType.INTERACTIVE
    card: CardContent
    update_multi: Optional[bool] = None

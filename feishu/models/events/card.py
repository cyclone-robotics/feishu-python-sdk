#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""飞书卡片消息事件

https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN2ATN

卡片消息事件和其他事件不一样，不是继承自base.Event
最明显的区别是
- event_callback事件外层有ts/uuid/token等字段，卡片消息没有
- event_callback中的token是校验token, 卡片消息中的token是用来刷新消息卡片内容的
"""
from typing import Optional

from .base import BaseModel


class Action(BaseModel):
    """交互信息

    Args:
        value 交互元素的value字段, key: value对
        tag 交互元素的tag值
        option 选中option的value(button元素不适用)
    """

    value: Optional[dict] = None
    tag: str
    option: str = ""


class CardAction(BaseModel):
    """卡片互动事件

    https://open.feishu.cn/document/ukTMukTMukTM/uYzMxEjL2MTMx4iNzETM

    Args:
        refresh_token 请求去重,
            需要特别提一下，这个并不是请求体里面的，而是headers['X-Refresh-Token']
            业务方通过验证 headers['X-Refresh-Token'] 来防止按钮事件被重复处理。
            在网络抖动等极端情况下，会出现卡片点击失败但是业务方已经处理过 action 的现象，
            所以业务方接口存在被重复调用的风险。
            X-Refresh-Token 只有在卡片点击事件成功被响应并通知到客户端的时候才会刷新，
            如果业务方的接口非幂等，可以通过缓存并验证该字段防止接口被重复调用。
    """

    open_id: str
    user_id: str
    tenant_key: str
    open_message_id: str
    token: str
    action: Action
    refresh_token: Optional[str]

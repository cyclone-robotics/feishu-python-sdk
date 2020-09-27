#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""飞书日历事件

https://open.feishu.cn/document/ukTMukTMukTM/uEzNxYjLxcTM24SM3EjN
"""

from .base import BaseModel, EventContent


class Attendee(BaseModel):
    open_id: str
    employee_id: str
    union_id: str


class EventReplyEvent(EventContent):
    """日程回复

    {
        "app_id" : "cli_xxxxxx",
        "type" : "event_reply", // 事件类型
        "tenant_key" : "xxxxx",
        "event_id": "xxxx", //日程id
        "attendee" : {
           "open_id":"xxx", // 回复此日程的参与人的open_id
           "employee_id":"yyy", // 回复此日程的参与人的employee_id，仅自建应用才会返回
           "union_id": "zzz" // 用户在ISV下的唯一标识，申请了"获取用户统一ID"权限后返回
        },
        "status": "accept", // 对日程的回复：accept 接受, tentative 待定, decline 拒绝
        "display_name":"xxx",
        "reply_timestmap":"1589097034" // 回复时间
    }
    """
    app_id: str
    type: str
    tenant_key: str
    event_id: str
    attendee: Attendee
    status: str
    display_name: str
    reply_timestamp: str

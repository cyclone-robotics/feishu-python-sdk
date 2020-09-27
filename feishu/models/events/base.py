#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""飞书事件类型声明

参考订阅事件文档 https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM
"""
from enum import Enum
from typing import Union

from pydantic import BaseModel


class EventType(str, Enum):
    APP_OPEN = "app_open"
    APP_STATUS_CHANGE = "app_status_change"
    ORDER_PAID = "order_paid"
    APP_TICKET = "app_ticket"
    APP_UNINSTALLED = "app_uninstalled"

    USER_ADD = "user_add"
    DEPT_ADD = "dept_add"
    USER_STATUS_CHANGE = "user_status_change"
    CONTACT_SCOPE_CHANGE = "contact_scope_change"

    ADD_BOT = "add_bot"
    REMOVE_BOT = "remove_bot"
    P2P_CHAT_CREATE = "p2p_chat_create"
    MESSAGE = "message"
    MESSAGE_READ = "message_read"

    CHAT_DISBAND = "chat_disband"
    GROUP_SETTING_UPDATE = "group_setting_update"

    LEAVE_APPROVAL = "leave_approval"
    LEAVE_APPROVAL_V2 = "leave_approvalV2"
    WORK_APPROVAL = "work_approval"
    SHIFT_APPROVAL = "shift_approval"
    REMEDY_APPROVAL = "remedy_approval"
    TRIP_APPROVAL = "trip_approval"
    OUT_APPROVAL = "out_approval"

    EVENT_REPLY = "event_reply"

    ADD_USER_TO_CHAT = "add_user_to_chat"
    REMOVE_USER_FROM_CHAT = "remove_user_from_chat"
    REVOKE_ADD_USER_FROM_CHAT = "revoke_add_user_from_chat"


class AppStatus(str, Enum):
    START_BY_TENANT = "start_by_tenant"
    STOP_BY_TENANT = "stop_by_tenant"
    STOP_BY_PLATFORM = "stop_by_platform"


class BuyType(str, Enum):
    BUY = "buy"
    UPGRADE = "upgrade"
    RENEW = "renew"


class PricePlanType(str, Enum):
    PER_SEAT_PER_MONTH = "per_seat_per_month"


class UserChatEventType(str, Enum):
    ADD_USER_TO_CHAT = "add_user_to_chat"
    REMOVE_USER_FROM_CHAT = "remove_user_from_chat"
    REVOKE_ADD_USER_FROM_CHAT = "revoke_add_user_from_chat"


class EventContent(BaseModel):
    type: Union[str, EventType]
    user_agent: str = ''
    tenant_key: str = ''
    app_id: str = ''


class Event(BaseModel):
    """事件回调内容

    Args:
        ts 事件发送的时间，一般近似于事件发生的时间
        uuid 事件的唯一标识
        token 即verify_token, 可以和后台配置的token进行校验
        type "event_callback"
    """
    ts: str = ''
    uuid: str = ''
    token: str = ''
    type: str = "event_callback"
    event: Union[dict, EventContent]


class Operator(BaseModel):
    open_id: str
    user_id: str = ''


class User(BaseModel):
    name: str
    open_id: str
    user_id: str = ''

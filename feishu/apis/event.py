#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""订阅事件处理

包含订阅事件的flask/sanic blueprint实现

https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM
"""
import asyncio
import logging
from concurrent.futures import Executor
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Callable, Union, Awaitable

from pydantic import ValidationError

from .base import decrypt_aes
from ..errors import ERRORS, FeishuError
from ..models.events import *

logger = logging.getLogger("feishu")


def setup_event_blueprint(framework: str, blueprint: Union["flask.Blueprint", "sanic.Blueprint"],
                          path: str, on_event: callable, executor: Optional[Executor] = None,
                          verify_token: Optional[str] = None, encrypt_key: Optional[str] = None):
    """配置一个用于接收订阅事件的Blueprint

    https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM
    Args:
        framework: 可选"flask"/"sanic"
        blueprint: flask/sanic的Blueprint对象
        path: 回调路径, 只需包含blueprint后的挂载部分
        on_event:
            有订阅事件时, 接收Event的参数, 无需返回
            当framework="flask"时,
                on_event函数会放在executor线程中单独调用
                注意，为了不卡住线程池，请自行处理完出错信息，否则出错Event会被丢弃
            当framework="sanic"时, on_event函数会被asyncio.create_task添加，
                请确保asyncio的loop配置正确，e.g. set_default_loop, 或者注意运行的先后顺序
                一般情况下直接用sanic不应该出现任何问题
        executor: 用来后台执行event的executor，没有的话默认启动一个2线程的
        verify_token: 校验token, 需和飞书后台配置一致, 不提供则不校验请求来源
        encrypt_key: 加密key, 需和飞书后台配置一致, 不提供则无法解析加密数据
    """
    if framework == "flask":
        return flask_blueprint(blueprint=blueprint, path=path, on_event=on_event, executor=executor,
                               verify_token=verify_token, encrypt_key=encrypt_key)
    elif framework == "sanic":
        return sanic_blueprint(blueprint=blueprint, path=path, on_event=on_event,
                               verify_token=verify_token, encrypt_key=encrypt_key)
    else:
        raise NotImplementedError


def flask_blueprint(blueprint: "flask.Blueprint", path: str,
                    on_event: Callable[[Event], None], executor: Optional[Executor] = None,
                    verify_token: Optional[str] = None, encrypt_key: Optional[str] = None):
    """配置一个用于接收消息交互回调的blueprint

    Args:
        blueprint: flask的Blueprint对象
        path: 回调路径, 只需包含blueprint后的挂载部分
        on_event: 有订阅事件时, 接收Event的参数, 无需返回,
            注意，因为on_event会在executor中实现，请自行处理完出错信息，否则出错Event会被丢弃
        executor: 用来后台执行event的executor，没有的话默认启动一个2线程的
        verify_token: 校验token, 需和飞书后台配置一致, 不提供则不校验请求来源
        encrypt_key: 加密key, 需和飞书后台配置一致, 不提供则无法解析加密数据
    """
    import flask

    if not executor:
        executor = ThreadPoolExecutor(2)

    def on_event_wrapper(event: Event):
        try:
            on_event(event)
        except Exception as e:
            logger.exception(f"执行on_event时失败, event={event}")

    @blueprint.route(path, methods=["POST"])
    def handle_event():
        payload: dict = flask.request.get_json(force=True)
        if "encrypt" in payload:
            payload = decrypt_aes(encrypt_key, payload["encrypt"])

        payload_type = payload.get("type")
        if payload_type == "url_verification":
            return url_verification(payload)
        elif payload_type == "event_callback":
            event = Event(**payload)
            event.event = guess_event(payload.get("event"))
            executor.submit(on_event_wrapper, event)
        return flask.jsonify()

    def url_verification(payload: dict):
        """配置请求网址后飞书会发送的验证请求

        https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM#%E9%85%8D%E7%BD%AE%E8%AF%B7%E6%B1%82%E7%BD%91%E5%9D%80
        """
        if verify_token and verify_token != payload.get("token"):
            return flask.jsonify(challenge="")

        return flask.jsonify(challenge=payload.get("challenge"))


def sanic_blueprint(blueprint: "sanic.Blueprint", path: str,
                    on_event: Callable[[Event], Awaitable[None]],
                    verify_token: Optional[str] = None, encrypt_key: Optional[str] = None):
    """配置一个用于接收消息交互回调的sanic.blueprint

    Args:
        blueprint: sanic的Blueprint对象
        path: 回调路径, 只需包含blueprint后的挂载部分
        on_event: 有Action事件时, 接收Event类型的参数, 无需任何返回
            on_event函数会被asyncio.create_task添加，
            请确保asyncio的loop配置正确，e.g. set_default_loop, 或者注意运行的先后顺序
            一般情况下直接用sanic不应该出现任何问题
        verify_token: 校验token, 需和飞书后台配置一致, 不提供则不校验请求来源
        encrypt_key: 加密key, 需和飞书后台配置一致, 不提供则无法解析加密数据
    """
    from sanic.request import Request
    from sanic import response

    @blueprint.route(path, methods=["POST"])
    async def handle_event(request: Request):
        payload: dict = request.json
        if "encrypt" in payload:
            payload = decrypt_aes(encrypt_key, payload["encrypt"])

        payload_type = payload.get("type")
        if payload_type == "url_verification":
            return url_verification(payload)
        elif payload_type == "event_callback":
            event = Event(**payload)
            event.event = guess_event(payload.get("event"))
            asyncio.create_task(on_event(event))

        return response.json({})

    def url_verification(payload: dict):
        """配置请求网址后飞书会发送的验证请求

        https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM#%E9%85%8D%E7%BD%AE%E8%AF%B7%E6%B1%82%E7%BD%91%E5%9D%80
        """
        if verify_token and verify_token != payload.get("token"):
            return response.json(dict(challenge=""))

        return response.json(dict(challenge=payload.get("challenge")))


def guess_event(event: dict) -> Union[dict, EventContent]:
    """适配event的真实类型"""
    event_type = event.get("type")
    # print("event_type", event_type)
    msg_event_cls: Optional[EventContent] = None
    if event_type == EventType.MESSAGE:
        msg_type = event.get("msg_type")
        # print("msg_type", msg_type)
        msg_event_cls = {
            EventMsgType.TEXT: TextMessageEvent,
            EventMsgType.IMAGE: ImageMessageEvent,
            EventMsgType.POST: PostMessageEvent,
            EventMsgType.FILE: FileMessageEvent,
            EventMsgType.MERGE_FORWARD: MergeForwardMessageEvent
        }.get(msg_type)
        # print("msg_event_cls", msg_event_cls)

    event_cls: Optional[EventContent] = {
        # app
        EventType.APP_OPEN: AppOpenEvent,
        EventType.APP_STATUS_CHANGE: AppStatusChangeEvent,
        EventType.APP_TICKET: AppTicketEvent,
        EventType.APP_UNINSTALLED: AppUninstalledEvent,

        # contact
        EventType.USER_ADD: UserAddEvent,
        EventType.DEPT_ADD: DeptAddEvent,
        EventType.USER_STATUS_CHANGE: UserStatusChangeEvent,
        EventType.CONTACT_SCOPE_CHANGE: ContactScopeChangeEvent,

        # bot
        EventType.ADD_BOT: AddBotEvent,
        EventType.REMOVE_BOT: RemoveBotEvent,
        EventType.P2P_CHAT_CREATE: P2PChatCreateEvent,
        EventType.MESSAGE_READ: MessageReadEvent,
        EventType.MESSAGE: msg_event_cls,

        # chat
        EventType.ADD_USER_TO_CHAT: UserChatEvent,
        EventType.REMOVE_USER_FROM_CHAT: UserChatEvent,
        EventType.REVOKE_ADD_USER_FROM_CHAT: UserChatEvent,
        EventType.CHAT_DISBAND: ChatDisbandEvent,

        # approval
        EventType.LEAVE_APPROVAL: LeaveApprovalEvent,
        EventType.LEAVE_APPROVAL_V2: LeaveApprovalV2Event,
        EventType.WORK_APPROVAL: WorkApprovalEvent,
        EventType.OUT_APPROVAL: OutApprovalEvent,
        EventType.TRIP_APPROVAL: TripApprovalEvent,
        EventType.SHIFT_APPROVAL: ShiftApprovalEvent,
        EventType.REMEDY_APPROVAL: RemedyApprovalEvent,

        # calendar
        EventType.EVENT_REPLY: EventReplyEvent,
    }.get(event_type)

    if event_cls:
        try:
            return event_cls(**event)
        except ValidationError:
            raise FeishuError(ERRORS.VALIDATION_ERROR, f"解析事件失败，原始数据 event = {event}")
    else:
        # 不知道是啥类型，直接返回原始的dict
        return event

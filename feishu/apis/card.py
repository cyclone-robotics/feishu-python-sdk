#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""消息卡片相关

- 发送卡片消息，临时卡片消息，删除临时卡片消息
- flask和sanic的blueprint
"""
import logging
from typing import Union, Callable, Optional, Awaitable

from .base import BaseAPI, allow_async_call, decrypt_aes
from ..models import CardMessage, CardAction, CardContent, SendMsgType, Action


logger = logging.getLogger("feishu")


class CardAPI(BaseAPI):
    @allow_async_call
    def send_card(
        self,
        card: Union[dict, CardMessage],
        update_multi: bool = None,
        open_id: str = "",
        user_id: str = "",
        email: str = "",
        chat_id: str = "",
        root_id: str = "",
    ) -> Optional[str]:
        """发送卡片消息

        https://open.feishu.cn/document/ukTMukTMukTM/uYTNwUjL2UDM14iN1ATN

        Args:
            card: dict或CardMessage类型
            update_multi: 控制卡片是否是共享卡片, 默认位False
            open_id: 用户的飞信ID(自建应用)
            user_id: 用户的应用ID(三方应用)
            email: 用户的邮箱
            chat_id: 群ID, 以上4种ID必须提供一种, 优先级为chat_id>open_id>user_id>email
            root_id: 回复消息所对应的呃消息id, 可选
        Returns:
            message_id

        请求body示例
        {
           "chat_id": "oc_abcdefg1234567890",
           "msg_type": "interactive",
           "root_id":"om_4*********************ad8",
           "update_multi":false,
           "card": {
                // card content
            }
        }

        card参数示例
        {
            "config": {
                "wide_screen_mode": true
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "this is header"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "This is a very very very very very very very long text;"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "Read"
                            },
                            "type": "default"
                        }
                    ]
                }
            ]
        }
        """
        api = "/message/v4/send/"

        msg = CardMessage(
            msg_type=SendMsgType.INTERACTIVE, card=card, update_multi=update_multi
        )
        if root_id:
            msg.root_id = root_id

        if chat_id:
            msg.chat_id = chat_id
        elif open_id:
            msg.open_id = open_id
        elif user_id:
            msg.user_id = user_id
        elif email:
            msg.email = email

        payload = msg.dict(exclude_none=True)
        result = self.client.request("POST", api=api, payload=payload)
        return result.get("data", {}).get("message_id")

    def send_ephemeral_card(self, card: Union[dict, CardMessage]) -> str:
        """发送临时卡片消息

        https://open.feishu.cn/document/ukTMukTMukTM/uETOyYjLxkjM24SM5IjN

        使用场景
            临时消息卡片多用于群聊中用户与机器人交互的中间态。
            例如在群聊中用户需要使用待办事项类bot创建一条提醒，
            bot 发送了可设置提醒日期和提醒内容的一张可交互的消息卡片，
            此卡片在没有设置为临时卡片的情况下为群内全员可见，既群内可看见该用户与 bot 交互的过程。
            而设置为临时卡片后，交互过程仅该用户可见，群内其他成员只会看到最终设置完成的提醒卡片。

        临时消息卡片可降低群消息的信噪比，并间接增加 bot 通知的用户触达。

        注意, card对象必须提供chat_id
        """
        api = "/ephemeral/v1/send"

        if isinstance(card, CardMessage):
            payload = card.dict(exclude_unset=True)
        else:
            payload = dict(card)

        result = self.client.request("POST", api=api, payload=payload)
        return result.get("data", {}).get("message_id")

    def delete_ephemeral_card(self, message_id: str):
        """删除临时卡片

        失败会raise FeishuError, (code和msg对应飞书平台的code/msg)
        """
        api = "/ephemeral/v1/delete"
        payload = {"message_id": message_id}
        self.client.request("POST", api=api, payload=payload)


def setup_action_blueprint(
    framework: str,
    blueprint: Union["flask.Blueprint", "sanic.Blueprint"],
    path: str,
    on_action: callable,
    verify_token: Optional[str] = None,
    encrypt_key: Optional[str] = None,
):
    """配置一个用于接收消息交互回调的Blueprint

    Args:
        framework: 可选"flask"/"sanic"
        blueprint: flask/sanic的Blueprint对象
        path: 回调路径, 只需包含blueprint后的挂载部分
        on_action:
            有Action事件时, 接收CardAction类型的参数, 返回卡片更新信息(CardContent类型)
            注意，在flask需传入同步的on_action，而sanic需传入异步的on_action
        verify_token: 校验token, 需和飞书后台配置一致, 不提供则不校验请求来源
        encrypt_key: 加密key, 需和飞书后台配置一致, 不提供则无法解析加密数据
    """
    if framework == "flask":
        return flask_blueprint(
            blueprint=blueprint,
            path=path,
            on_action=on_action,
            verify_token=verify_token,
            encrypt_key=encrypt_key,
        )
    elif framework == "sanic":
        return sanic_blueprint(
            blueprint=blueprint,
            path=path,
            on_action=on_action,
            verify_token=verify_token,
            encrypt_key=encrypt_key,
        )
    else:
        raise NotImplementedError


def flask_blueprint(
    blueprint: "flask.Blueprint",
    path: str,
    on_action: Callable[[CardAction], Union[dict, CardContent]],
    verify_token: Optional[str] = None,
    encrypt_key: Optional[str] = None,
):
    """配置一个用于接收消息交互回调的blueprint

    Args:
        blueprint: flask的Blueprint对象
        path: 回调路径, 只需包含blueprint后的挂载部分
        on_action: 有Action事件时, 接收CardAction类型的参数, 返回卡片更新信息(CardContent类型)
        verify_token: 校验token, 需和飞书后台配置一致, 不提供则不校验请求来源
        encrypt_key: 加密key, 需和飞书后台配置一致, 不提供则无法解析加密数据
    """
    from flask import request, jsonify

    def on_action_wrapper(action: Action):
        try:
            on_action(action)
        except Exception as e:
            logger.exception(f"执行on_action时失败, action={action}")

    @blueprint.route(path, methods=["POST"])
    def handle_card_action():
        payload: dict = request.get_json(force=True)
        if "encrypt" in payload:
            payload = decrypt_aes(encrypt_key, payload["encrypt"])

        if payload.get("type") == "url_verification":
            return url_verification(payload)

        action = CardAction(**payload)
        action.refresh_token = request.headers.get("X-Refresh-Token")
        card_update = on_action_wrapper(action)
        if isinstance(card_update, CardContent):
            card_update = card_update.dict(exclude_unset=True)
        card_update = card_update or {}
        return jsonify(**card_update)

    def url_verification(payload: dict):
        """配置请求网址后飞书会发送的验证请求

        https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM#%E9%85%8D%E7%BD%AE%E8%AF%B7%E6%B1%82%E7%BD%91%E5%9D%80
        """
        if verify_token and verify_token != payload.get("token"):
            return jsonify(challenge="")

        return jsonify(challenge=payload.get("challenge"))


def sanic_blueprint(
    blueprint: "sanic.Blueprint",
    path: str,
    on_action: Callable[[CardAction], Awaitable[Union[dict, CardContent]]],
    verify_token: Optional[str] = None,
    encrypt_key: Optional[str] = None,
):
    """配置一个用于接收消息交互回调的sanic.blueprint

    Args:
        blueprint: sanic的Blueprint对象
        path: 回调路径, 只需包含blueprint后的挂载部分
        on_action: 有Action事件时, 接收CardAction类型的参数, 返回卡片更新信息(CardContent类型)
        verify_token: 校验token, 需和飞书后台配置一致, 不提供则不校验请求来源
        encrypt_key: 加密key, 需和飞书后台配置一致, 不提供则无法解析加密数据
    """
    from sanic.request import Request
    from sanic import response

    @blueprint.route(path, methods=["POST"])
    async def handle_card_action(request: Request):
        payload: dict = request.json
        if "encrypt" in payload:
            payload = decrypt_aes(encrypt_key, payload["encrypt"])

        if payload.get("type") == "url_verification":
            return url_verification(payload)

        action = CardAction(**payload)
        action.refresh_token = request.headers.get("X-Refresh-Token")
        card_update = await on_action(action)
        if isinstance(card_update, CardContent):
            card_update = card_update.dict(exclude_unset=True)
        return response.json(card_update)

    def url_verification(payload: dict):
        """配置请求网址后飞书会发送的验证请求

        https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM#%E9%85%8D%E7%BD%AE%E8%AF%B7%E6%B1%82%E7%BD%91%E5%9D%80
        """
        if verify_token and verify_token != payload.get("token"):
            return response.json(dict(challenge=""))

        return response.json(dict(challenge=payload.get("challenge")))

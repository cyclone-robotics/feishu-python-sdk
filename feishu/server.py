#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""简易示例回调服务器"""
import asyncio
import logging
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor

import requests

from .apis import setup_event_blueprint, setup_action_blueprint
from .consts import FEISHU_VERIFY_TOKEN, FEISHU_ENCRYPT_KEY
from .models import EventContent, CardAction

PATH_EVENT = "/feishu/callback/event"
PATH_ACTION = "/feishu/callback/action"


def create_simple_flask_server(verify_token: str = '', encrypt_key: str = '') -> "flask.Flask":
    """创建一个基于flask的简单的记录服务器

    记录：
        - 订阅事件(models.Event)
        - 互动消息(models.CardAction)
    """
    from flask import Flask, Blueprint
    app = Flask("feishu")

    def on_event(event: EventContent):
        app.logger.info(f"event: {event}")

    def on_action(action: CardAction):
        app.logger.info(f"action: {action}")

    event_app = Blueprint(name="event_app", import_name=__name__)
    setup_event_blueprint("flask", blueprint=event_app, path=PATH_EVENT,
                          on_event=on_event, verify_token=verify_token, encrypt_key=encrypt_key)

    action_app = Blueprint(name="action_app", import_name=__name__)
    setup_action_blueprint("flask", blueprint=action_app, path=PATH_ACTION,
                           on_action=on_action, verify_token=verify_token, encrypt_key=encrypt_key)

    app.register_blueprint(event_app)
    app.register_blueprint(action_app)

    app.logger.setLevel(logging.INFO)
    return app


def run_simple_flask_server(encrypt_key: str = '', verify_token: str = ''):
    if not encrypt_key:
        encrypt_key = os.environ.get(FEISHU_ENCRYPT_KEY, "").strip()
    if not verify_token:
        verify_token = os.environ.get(FEISHU_VERIFY_TOKEN, "").strip()
    app = create_simple_flask_server(encrypt_key=encrypt_key,
                                     verify_token=verify_token)
    port = 9000
    host = requests.get("http://api.ipify.org/").text

    def print_notice():
        time.sleep(0.5)
        app.logger.info("请确保服务器有公网静态IP!!!")
        app.logger.info(f"请在飞书后台配置订阅信息URL = 'http://{host}:{port}{PATH_EVENT}'")
        app.logger.info(f"请在飞书后台配置卡片互动消息URL = 'http://{host}:{port}{PATH_ACTION}'")

    executor = ThreadPoolExecutor(1)
    executor.submit(print_notice)

    app.run(host='0.0.0.0', port=port)


def create_simple_sanic_server(verify_token: str = '', encrypt_key: str = '') -> "sanic.Sanic":
    """创建一个基于sanic的简单的记录服务器

    记录：
        - 订阅事件(models.Event)
        - 互动消息(models.CardAction)
    """
    from sanic import Sanic, Blueprint
    from sanic.log import logger
    app = Sanic("feishu")

    async def on_event(event: EventContent):
        await asyncio.sleep(2)
        logger.info(f"event: {event}")

    async def on_action(action: CardAction):
        logger.info(f"action: {action}")

    event_app = Blueprint(name="event_app")
    setup_event_blueprint("sanic", blueprint=event_app, path=PATH_EVENT,
                          on_event=on_event, verify_token=verify_token, encrypt_key=encrypt_key)

    action_app = Blueprint(name="action_app")
    setup_action_blueprint("sanic", blueprint=action_app, path=PATH_ACTION,
                           on_action=on_action, verify_token=verify_token, encrypt_key=encrypt_key)

    app.blueprint(event_app)
    app.blueprint(action_app)

    logger.setLevel(logging.INFO)
    return app


def run_simple_sanic_server(encrypt_key: str = '', verify_token: str = ''):
    from sanic.log import logger
    if not encrypt_key:
        encrypt_key = os.environ.get(FEISHU_ENCRYPT_KEY, "").strip()
    if not verify_token:
        verify_token = os.environ.get(FEISHU_VERIFY_TOKEN, "").strip()
    app = create_simple_sanic_server(encrypt_key=encrypt_key,
                                     verify_token=verify_token)
    port = 9000
    host = requests.get("http://api.ipify.org/").text

    async def print_notice():
        logger.info("请确保服务器有公网静态IP!!!")
        logger.info(f"请在飞书后台配置订阅信息URL = 'http://{host}:{port}{PATH_EVENT}'")
        logger.info(f"请在飞书后台配置卡片互动消息URL = 'http://{host}:{port}{PATH_ACTION}'")

    app.add_task(print_notice())
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    # run_simple_flask_server()
    run_simple_sanic_server()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from typing import Union


class FeishuBaseClient(ABC):
    logger = logging.getLogger("feishu")

    app_id: str
    app_secret: str
    run_async: bool
    event_loop: AbstractEventLoop

    @abstractmethod
    def request(self, method: str, api: str, params: dict = {}, payload: dict = {},
                data: dict = {}, files: dict = {}, auth: str = True) -> Union[dict, bytes]:
        """发起请求

        Args:
            method: "GET" or "POST"
            api: 对应功能的API Path, e.g. "/user/v1/union_id/batch_get/list"
            params: HTTP的URL参数
            payload: Body的参数, 会序列化为json
            data: form-data
            files: multipart/form-data
            auth: 是否需要验证, 只有token类API需要设为False

        Returns:
            一个解析好的返回dict，为飞书的标准格式
            code: 0为正常
            msg: 出错信息
            data: 真正的数据信息

        Raises:
            FeishuException
        """

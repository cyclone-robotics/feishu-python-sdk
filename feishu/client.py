#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import logging
import os
import secrets
from asyncio import Future, AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Union, Tuple
import datetime
import threading
import aiohttp
import requests

from .apis import FeishuAPI, _get_or_create_event_loop
from .baseclient import FeishuBaseClient
from .consts import *
from .errors import FeishuError, ERRORS
from .stores import TokenStore, MemoryStore

logger = logging.getLogger("feishu")


class FeishuClient(FeishuBaseClient, FeishuAPI):
    """飞书开放平台客户端"""

    def __init__(self, app_id: Optional[str] = None,
                 app_secret: Optional[str] = None,
                 app_type: AppType = AppType.TENANT,
                 run_async: bool = False,
                 event_loop: Optional[AbstractEventLoop] = None,
                 endpoint: str = "https://open.feishu.cn/open-apis/",
                 timeout: float = 5,
                 token_store: Optional[TokenStore] = None):
        """初始化

        Args:
            app_id: 飞书自建应用的app_id, 默认则取环境变量中的FEISHU_APP_ID
            app_secret: 飞书自建应用的app_secret, 默认则取环境变量中的FEISHU_APP_SECRET
            app_type: "tenant": 用户自建应用/"user": 第三方应用
            run_async: 是否异步模式, 异步模式下所有外部调用都返回一个asyncio.Future, 默认为False
            event_loop: 若run_async=True, 可以提供event_loop作为async方法的loop
                如果不提供的话，请确保在执行API请求前设置默认loop: asyncio.set_event_loop(loop)
            timeout: 连接超时，其中timeout/3为连接超时，timeout*2/3为读取超时
            endpoint: 飞书平台的endpoint, 一般默认就好
            token_store: 飞书的access_token会在2小时后过期，这里
        """
        allowed_types = AppType.__dict__["_value2member_map_"]
        if app_type not in allowed_types or app_type == "user":
            raise NotImplementedError(
                f"不支持app_type={app_type}, 暂时支持了tenant自建应用")

        self.app_id = app_id
        self.app_secret = app_secret
        self.app_type = app_type
        self.run_async = run_async
        self.event_loop: Optional[asyncio.AbstractEventLoop] = event_loop
        self.endpoint = endpoint
        self.timeout = timeout

        if not self.app_id:
            self.app_id = os.environ.get(FEISHU_APP_ID, "").strip()
        if not self.app_secret:
            self.app_secret = os.environ.get(FEISHU_APP_SECRET, "").strip()

        assert self.app_id and self.app_secret, "必须提供app_id/app_secret"

        while self.endpoint.endswith("/"):
            self.endpoint = self.endpoint[:-1]

        # 内部使用时用api作为namespace更清晰些
        self.api = FeishuAPI(self)
        # 但同时因为继承了FeishuAPI, 所以必须为那些方法提供一个client
        self.client = self

        if self.run_async:
            self.event_loop = event_loop  # lazy initialize in self.request/self.fetch
            self.session_async = None  # lazy initialize in self.request/self.fetch
            self.executor = ThreadPoolExecutor(2)
        else:
            self.session = requests.Session()
            self.executor = None
        self.closed = False
        if not token_store:
            self.token_store = {}
        else:
            self.token_store = token_store
        self.user_info_store = {}

    def request(self,
                method: str,
                api: str = None,
                api_url: str = None,
                headers={
                    "Content-Type": "application/json",
                },
                params: dict = {},
                payload: dict = {},
                data: dict = {},
                files: dict = {},
                auth: str = True) -> Union[dict, bytes, Future]:
        """发起请求

        Args:
            method: "GET" or "POST"
            api: 对应功能的API Path, e.g. "/user/v1/union_id/batch_get/list"
            params: HTTP的URL参数
            payload: Body的参数, 会序列化为json
            data: Form-Data格式的参数
            files: Multipart-encoded格式的文件参数
            auth: 是否需要验证, 只有token类API需要设为False

        Returns:
            一个解析好的返回dict，为飞书的标准格式
            code: 0为正常
            msg: 出错信息
            data: 真正的数据信息

        Raises:
            FeishuException
        """
        if self.closed:
            raise FeishuError(ERRORS.CLIENT_CLOSED, "client对象已被关闭")

        if api_url:
            url = api_url
        else:
            if not api:
                raise TypeError(
                    "request() requires one of the positional arguments : 'api' or 'api_url")
            url = self.endpoint + api
        timeout_pair = (self.timeout / 3, self.timeout * 2 / 3)

        if self.run_async:
            async def do_request_async():
                return await self._async_request(
                    method=method, url=url, timeout_pair=timeout_pair, headers=headers,
                    params=params, payload=payload, data=data, files=files)

            future = asyncio.ensure_future(
                do_request_async(),
                loop=self.event_loop,
            )
            return future
        else:
            return self._sync_request(method=method, url=url, timeout_pair=timeout_pair,
                                      headers=headers, params=params, payload=payload, data=data, files=files)

    async def _async_request(self, method: str, url: str, timeout_pair: Tuple[float, float],
                             headers: dict, params: dict, payload: dict, data: dict, files: dict) -> Future:

        if not self.session_async:
            self.session_async = aiohttp.ClientSession()
        if not self.event_loop or self.event_loop.is_closed():
            self.event_loop = _get_or_create_event_loop()
        request_id = secrets.token_hex(4)

        try:
            timeout = aiohttp.ClientTimeout(
                sock_connect=timeout_pair[0], sock_read=timeout_pair[1])
            if method == "GET":
                self.logger.debug(
                    f"GET url={url} params={params} headers={headers} (id={request_id})")
                resp = await self.session_async.get(url, params=params, headers=headers, timeout=timeout)
            elif method == "POST":
                if data or files:
                    # multipart/form-data
                    form = aiohttp.FormData()
                    for key, value in data.items():
                        form.add_field(key, value)
                    for filename, content in files.items():
                        assert not isinstance(
                            content, (tuple, list)), "暂时只支持bytes/str/fileobj等格式的上传数据"
                        data.add_field(filename, content)
                    self.logger.debug(f"POST(form-data) url={url} params={params} "
                                      f"data.keys={data.keys()} headers={headers} (id={request_id})")
                    resp = await self.session_async.post(url, params=params, data=data, headers=headers,
                                                         timeout=timeout)
                else:
                    # application/json
                    self.logger.debug(f"POST url={url} params={params} json={payload} "
                                      f"headers={headers} (id={request_id})")
                    resp = await self.session_async.post(url, params=params, json=payload, headers=headers,
                                                         timeout=timeout)
            else:
                raise FeishuError(ERRORS.UNSUPPORTED_METHOD,
                                  f"不支持的请求method: {method}, 调用上下文: "
                                  f"url={url}, params={params}, payload={payload} "
                                  f"data={data} files.keys={files.keys()}")
        except aiohttp.ClientError as e:
            raise FeishuError(
                ERRORS.FAILED_TO_ESTABLISH_CONNECTION, f"建立和服务器的请求失败: {e}")

        try:
            result = await resp.json(content_type=None)
        except ValueError:
            raise FeishuError(ERRORS.UNABLE_TO_PARSE_SERVER_RESPONSE,
                              f"服务器返回格式有问题，无法解析成JSON: {resp.text}")

        if result.get("code") != 0:
            raise FeishuError(result.get("code") or ERRORS.UNKNOWN_SERVER_ERROR,
                              result.get("msg") or f"无有效出错信息，返回JSON数据为: {result}")

        self.logger.debug(f"response={result} (id={request_id})")
        return result

    def _sync_request(self, method: str, url: str, timeout_pair: Tuple[float, float],
                      headers: dict, params: dict, payload: dict, data: dict, files: dict) -> dict:
        request_id = secrets.token_hex(4)
        try:
            if method == "GET":
                self.logger.debug(
                    f"GET url={url} params={params} headers={headers} (id={request_id})")
                resp = self.session.get(
                    url, params=params, headers=headers, timeout=timeout_pair)
            elif method == "POST":
                self.logger.debug(f"POST url={url} params={params} json={payload} "
                                  f"data={data} files.keys={files.keys()} headers={headers} (id={request_id})")
                resp = self.session.post(url, params=params, json=payload, data=data, files=files, headers=headers,
                                         timeout=timeout_pair)
            else:
                raise FeishuError(ERRORS.UNSUPPORTED_METHOD,
                                  f"不支持的请求method: {method}, 调用上下文: "
                                  f"api={api}, params={params}, payload={payload}")
        except requests.exceptions.RequestException as e:
            raise FeishuError(
                ERRORS.FAILED_TO_ESTABLISH_CONNECTION, f"建立和服务器的请求失败: {e}")

        try:
            result = resp.json()
        except ValueError:
            raise FeishuError(ERRORS.UNABLE_TO_PARSE_SERVER_RESPONSE,
                              f"服务器返回格式有问题，无法解析成JSON: {resp.text}")

        if result.get("code") != 0:
            raise FeishuError(result.get("code") or ERRORS.UNKNOWN_SERVER_ERROR,
                              result.get("msg") or f"无有效出错信息，返回JSON数据为: {result}")

        self.logger.debug(f"response={result} (id={request_id})")
        return result

    def fetch(self, method: str, url: str, params: str, data: dict, json: dict, headers: dict,
              timeout: Union[float, tuple]) \
            -> Union[bytes, Future]:
        """简易sync/asyncHTTP请求Adapter

        Usage::

        >>> def api_sync(self, url):
        ...     resp = self.fetch(url)

        >>> async def api_async(self, url):
        ...     resp = await self.fetch(url) # 注意, self.run_async必须为True

        或者更好一点，同时支持sync/async

        >>> @allow_async_call
        ... def api_both(self, url):
        ...     resp = self.fetch(url)
        """
        if self.closed:
            raise FeishuError(ERRORS.CLIENT_CLOSED, "client对象已被关闭")

        if self.run_async:
            if not self.session_async:
                self.session_async = aiohttp.ClientSession()
            if not self.event_loop or self.event_loop.is_closed():
                self.event_loop = _get_or_create_event_loop()

            async def async_fetch():
                resp = await self.session_async.request(method=method, url=url, params=params, data=data, json=json,
                                                        headers=headers, timeout=timeout)
                return await resp.read()

            return asyncio.ensure_future(
                async_fetch(),
                loop=self.event_loop
            )
        else:
            resp = self.session.request(method=method, url=url, params=params, data=data, json=json,
                                        headers=headers, timeout=timeout)
            return resp.content

    async def close(self):
        """不关闭一下aiohttp会发warning有点烦, 强迫症适用"""
        if not self.closed and self.session_async:
            self.session_async.close()
            self.closed = True

    def request_app_access_token(self) -> str:
        if not "app_access_token" in self.token_store.keys():
            body = self.request(method="GET", api_url=FEISHU_APP_ACCESS_TOKEN_URL, params={
                "app_id": self.app_id, "app_secret": self.app_secret})
            self.token_store["app_access_token"] = body["app_access_token"]
            return body["app_access_token"]
        else:
            return self.token_store["app_access_token"]

    def request_tenant_access_token(self) -> str:
        if not "tenant_access_token" in self.token_store.keys():
            body = self.request(method="GET", api_url=FEISHU_TENANT_ACCESS_TOKEN_URL, params={
                "app_id": self.app_id, "app_secret": self.app_secret})
            self.token_store["tenant_access_token"] = body["tenant_access_token"]
            return body["tenant_access_token"]
        else:
            return self.token_store["tenant_access_token"]

    def request_user_access_token(self, code: str = None) -> str:
        if not "access_token" in self.token_store.keys():
            print("get new acc")
            body = self.request(method="POST", api_url=FEISHU_USER_IDENTITY_URL, payload={
                "app_access_token": self.request_app_access_token(), "code": code, "grant_type": "authorization_code"})
            self.token_store["access_token"] = body["data"]["access_token"]
            self.token_store["refresh_token"] = body["data"]["refresh_token"]
            return body["data"]["access_token"]
        else:
            print("get old acc")
            return self.token_store["access_token"]

    def request_refreshed_user_access_token(self) -> dict:
        print("Refreshing user token")
        if not "access_token" in self.token_store.keys():
            body = self.request(method="POST", api_url=FEISHU_USER_REFRESH_URL, payload={
                "refresh_token": self.token_store["refresh_token"], "app_access_token": self.request_app_access_token(), "grant_type": "refresh_token"})
            self.token_store["access_token"] = body["data"]["access_token"]
            self.token_store["refresh_token"] = body["data"]["refresh_token"]
            return body["data"]["access_token"]
        else:
            return self.token_store["access_token"]

    def request_user_info(self) -> dict:
        if self.user_info_store == {}:
            body = self.request(method="GET", api_url=FEISHU_USER_INFO_URL, headers={
                "Content-Type": "application/json", "Authorization": "Bearer " + self.request_user_access_token()
            }, params={"user_access_token": self.request_user_access_token()})
            for k, v in body['data'].items():
                self.user_info_store[k] = v
            return body
        else:
            return self.user_info_store
            
class FeishuSelfRenewClient(FeishuClient):
    def request_user_access_token(self, code: str = None) -> str:
        if not "access_token" in self.token_store.keys():
            body = self.request(method="POST", api_url=FEISHU_USER_IDENTITY_URL, payload={
                "app_access_token": self.request_app_access_token(), "code": code, "grant_type": "authorization_code"})
            self.token_store["access_token"] = body["data"]["access_token"]
            self.token_store["refresh_token"] = body["data"]["refresh_token"]
            self._create_user_access_token_timer()
            return body["data"]["access_token"]
        else:
            return self.token_store["access_token"]

    def _request_refreshed_user_access_token(self) -> dict:
        print("[" + time.ctime() + "] Refreshing user token using refresh token: " +
              self.token_store["refresh_token"])
        try:
            body = self.request(method="POST", api_url=FEISHU_USER_REFRESH_URL, payload={
                "refresh_token": self.token_store["refresh_token"], "app_access_token": self.request_app_access_token(), "grant_type": "refresh_token"})
        except FeishuError:
            print(
                "[" + time.ctime() + "] Refreshing user token failed. Try again after 60s")
            time.sleep(60)
            self._request_refreshed_user_access_token()
        self.token_store["access_token"] = body["data"]["access_token"]
        self.token_store["refresh_token"] = body["data"]["refresh_token"]
        self._create_user_access_token_timer()

    def request_app_access_token(self) -> str:
        if not "app_access_token" in self.token_store.keys():
            body = self.request(method="GET", api_url=FEISHU_APP_ACCESS_TOKEN_URL, params={
                "app_id": self.app_id, "app_secret": self.app_secret})
            self.token_store["app_access_token"] = body["app_access_token"]
            if not self.app_access_token_flag:
                self.app_access_token_flag = True
                self._create_app_access_token_timer()
            return body["app_access_token"]
        else:
            return self.token_store["app_access_token"]

    def _request_app_access_token(self) -> str:
        try:    
            body = self.request(method="GET", api_url=FEISHU_APP_ACCESS_TOKEN_URL, params={"app_id": self.app_id, "app_secret": self.app_secret})
        except FeishuError:
            print(
                "[" + time.ctime() + "] Refreshing app token failed. Try again after 60s")
            time.sleep(60)
            self._request_app_access_token()
        self.token_store["app_access_token"] = body["app_access_token"]
        self._create_app_access_token_timer()

    def request_tenant_access_token(self) -> str:
        if not "tenant_access_token" in self.token_store.keys():
            body = self.request(method="GET", api_url=FEISHU_TENANT_ACCESS_TOKEN_URL, params={
                "app_id": self.app_id, "app_secret": self.app_secret})
            self.token_store["tenant_access_token"] = body["tenant_access_token"]
            if not self.tenant_access_token_flag:
                self.tenant_access_token_flag = True
                self._create_tenant_access_token_timer()
            return body["tenant_access_token"]
        else:
            return self.token_store["tenant_access_token"]

    def _request_tenant_access_token(self) -> str:
        try:
            body = self.request(method="GET", api_url=FEISHU_TENANT_ACCESS_TOKEN_URL, params={"app_id": self.app_id, "app_secret": self.app_secret})
        except FeishuError:
            print(
                "[" + time.ctime() + "] Refreshing app token failed. Try again after 60s")
            time.sleep(60)
            self._request_tenant_access_token()
        self.token_store["tenant_access_token"] = body["tenant_access_token"]
        self._create_tenant_access_token_timer()


    def _create_user_access_token_timer(self):
        t = threading.Timer(FEISHU_TOKEN_EXPIRE_TIME - FEISHU_TOKEN_UPDATE_TIME, self._request_refreshed_user_access_token)
        t.start()

    def _create_app_access_token_timer(self):
        t = threading.Timer(FEISHU_TOKEN_EXPIRE_TIME - FEISHU_TOKEN_UPDATE_TIME, self._request_app_access_token)
        t.start()

    def _create_tenant_access_token_timer(self):
        t = threading.Timer(FEISHU_TOKEN_EXPIRE_TIME - FEISHU_TOKEN_UPDATE_TIME, self._request_tenant_access_token)
        t.start()

class FeishuApprovalClient(FeishuClient):
    def request_approval_info(self, approval_code: str) -> dict:
        body = self.request(method="POST", api_url=FEISHU_APPROVAL_DEFINITION_URL, headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self.request_tenant_access_token()
        }, payload={"approval_code": approval_code,
                    "locale": "en-US"}
        )
        return body

    def request_approval_instance_list(self, approval_code: str, start: int, end: int) -> dict:
        body = self.request(method="POST", api_url=FEISHU_APPROVAL_INSTANCE_LIST_URL, headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self.request_tenant_access_token()
        }, payload={
            "approval_code": approval_code,
            "start_time": start,
            "end_time": end,
            "offset": 0,
            "limit": 100
        }
        )
        return body

    def subscribe_approval(self, approval_code) -> dict:
        body = self.request(method="POST", api_url=FEISHU_APPROVAL_SUBSCRIBE_URL, headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self.request_tenant_access_token()
        }, payload={
            "approval_code": approval_code
        }
        )
        return body

    def submit_approval(self, submit_form, approval_code, data):
        form = submit_form % data
        body = self.request(method="POST", api_url=FEISHU_APPROVAL_CREATE_URL, headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self.request_tenant_access_token()}, payload={
            "approval_code": approval_code,
            "user_id": self.user_info_store['user_id'],
            "form": form

        })
        return body

    def request_approval_instance_info(self, instance_code):
        body = self.request(method="POST", api_url=FEISHU_APPROVAL_GET_URL, headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self.request_tenant_access_token()
        }, payload={"instance_code": instance_code,
                    "locale": "en-US"}
        )
        return body

    def spread_sheet_meta_info(self, spread_sheet_token):
        body = self.request(method="GET", api_url=FEISHU_SHEET_META_DATA_URL % spread_sheet_token, headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self.request_user_access_token()})
        return body

    def prepend_sheet(self, spread_sheet_token, sheet_token, prepend_range, data):
        body = self.request(method="POST", api_url=FEISHU_SHEET_PREPEND_URL % spread_sheet_token, headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self.request_user_access_token()}, payload={
                "spreadSheetToken": sheet_token,
                "Authorization": self.request_user_access_token(),
                "valueRange": {
                    "range": sheet_token + prepend_range,
                    "values": [
                        data
                    ]
                }
        }
        )
        return body

class SelfRenewApprovalClient(SelfRenewClient,FeishuApprovalClient):
    pass

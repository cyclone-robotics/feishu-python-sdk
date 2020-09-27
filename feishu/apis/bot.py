#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""机器人管理相关API

包括:
- 群管理
- 机器人管理
"""
from typing import List, Optional

from .base import BaseAPI, allow_async_call
from ..consts import FEISHU_BATCH_SEND_SIZE
from ..models import BotInfo, CreateChatRequest, CreateChatResponse, ChatPagination, ChatInfo, ChatUpdateRequest, \
    AddChatterResponse, RemoveChatterResponse


class BotAPI(BaseAPI):
    @allow_async_call
    def get_bot_info(self) -> BotInfo:
        """获取自建应用的token

        https://open.feishu.cn/document/ukTMukTMukTM/uAjMxEjLwITMx4CMyETM
        返回示例:
            {
                "activate_status": 2,
                "app_name": "name",
                "avatar_url": "https://sf1-ttcdn-tos.pstatp.com/obj/lark.avatar/da5xxxx14b16113",
                "ip_white_list": [],
                "open_id": "ou_xxx"
            }
        """
        api = "/bot/v3/info/"
        result = self.client.request("GET", api=api)
        return BotInfo(**result.get("bot", {}))

    @allow_async_call
    def add_bot(self, chat_id: str):
        """拉机器人进群

        Args:
            chat_id: 群ID

        失败会raise FeishuError, (code和msg对应飞书平台的code/msg)
        """
        api = "/bot/v4/add"
        payload = {"chat_id": chat_id}
        self.client.request("POST", api=api, payload=payload)

    @allow_async_call
    def remove_bot(self, chat_id: str):
        """将机器人移出群

        Args:
            chat_id: 群ID

        失败会raise FeishuError, (code和msg对应飞书平台的code/msg)
        """
        api = "/bot/v4/remove"
        payload = {"chat_id": chat_id}
        self.client.request("POST", api=api, payload=payload)

    @allow_async_call
    def create_chat(self, name: str = '', description: str = '',
                    open_ids: List[str] = [], user_ids: List[str] = [], i18n_names: dict = {},
                    only_owner_add: bool = False, share_allowed: bool = True,
                    only_owner_at_all: bool = False, only_owner_edit: bool = False) -> CreateChatResponse:
        """创建群

        Args:
            name: 群名称, 可不填
            description: 群描述, 可不填
            open_ids: 最多200个, 自建应用使用
            user_ids: 最多200个, 第三方应用使用
            i18n_names: 举例 {”zh_cn": "中文", "en_us": "english"}
            only_owner_add: 是否仅群主可以添加人
            share_allowed: 是否允许分享群
            only_owner_at_all: 是否仅群主@all
            only_owner_edit: 是否仅群主可编辑群信息，群信息包括头像、名称、描述、公告

        Returns:
            CreateChatResponse:
                chat_id
                invalid_open_ids
                invalid_user_ids
        """
        api = "/chat/v4/create/"
        req = CreateChatRequest(name=name, description=description, open_ids=open_ids, user_ids=user_ids,
                                i18n_names=i18n_names, only_owner_add=only_owner_add, share_allowed=share_allowed,
                                only_owner_at_all=only_owner_at_all, only_owner_edit=only_owner_edit)
        payload = req.dict(exclude_defaults=True)
        result = self.client.request("POST", api=api, payload=payload)
        return CreateChatResponse(**result.get("data"))

    @allow_async_call
    def list_chat(self, page_size: int = 100, page_token: str = '') -> ChatPagination:
        """获取群列表

        Args:
            page_size: 最大为200
            page_token: 分页标记，第一次请求不填，表示从头开始遍历
                分页查询还有更多群时会同时返回新的 page_token, 下次遍历可采用该 page_token 获取更多群
        Returns:
            ChatPagination
                has_more: bool
                page_token: str
                groups: List[ChatInfo]
            示例
            {
                "groups": [
                    {
                        "avatar": "http://p3.pstatp.com/origin/78c0000676df676a7f6e",
                        "chat_id": "oc_9e9619b938c9571c1c3165681cdaead5",
                        "description": "description1",
                        "name": "test1",
                        "owner_open_id": "ou_194911f90c43ec42d1ba0e93f22b8fb1",
                        "owner_user_id": "ca51d83b"
                    },
                    {
                        "avatar": "http://p4.pstatp.com/origin/dae10015cfb346541010",
                        "chat_id": "oc_5ce6d572455d361153b7cb51da133945",
                        "description": "description2",
                        "name": "test2",
                        "owner_open_id": "ou_194911f90c43ec42d1ba0e93f22b8fb1",
                        "owner_user_id": "ca51d83b"
                    }
                ],
                "has_more": false,
                "page_token": "0"
            }
        """
        api = "/chat/v4/list"
        payload = {
            "page_size": str(page_size),
        }
        if page_token:
            payload["page_token"] = page_token
        result = self.client.request("POST", api=api, payload=payload)
        return ChatPagination(**result)

    @allow_async_call
    def list_chat_all(self) -> List[ChatInfo]:
        """获取所有群列表"""
        all_chats = []
        pag = self.list_chat(page_size=FEISHU_BATCH_SEND_SIZE)
        all_chats.extend(pag.groups)
        while pag.has_more:
            pag = self.list_chat(page_size=FEISHU_BATCH_SEND_SIZE, page_token=pag.page_token)
            all_chats.extend(pag.groups)
        return all_chats

    @allow_async_call
    def get_chat_info(self, chat_id: str) -> ChatInfo:
        """获取群信息"""
        api = "/chat/v4"
        params = {"chat_id": chat_id}
        result = self.client.request("GET", api=api, params=params)
        return ChatInfo(**result.get("data", {}))

    @allow_async_call
    def update_chat_info(self, chat_id: str,
                         owner_user_id: Optional[str] = None,
                         owner_open_id: Optional[str] = None,
                         name: Optional[str] = None,
                         i18n_names: Optional[dict] = None,
                         only_owner_add: Optional[bool] = None,
                         share_allowed: Optional[bool] = None,
                         only_owner_at_all: Optional[bool] = None,
                         only_owner_edit: Optional[bool] = None
                         ) -> str:
        """更新群信息"""
        api = "/chat/v4/update/"
        req = ChatUpdateRequest(chat_id=chat_id)
        for key in ["owner_user_id", "owner_open_id", "name", "i18n_names",
                    "only_owner_add", "share_allowed", "only_owner_at_all", "only_owner_edit"]:
            value = locals()[key]
            if value is not None:
                setattr(req, key, value)
        payload = req.dict(exclude_unset=True)
        result = self.client.request("POST", api=api, payload=payload)
        return result.get("data", {}).get("chat_id", "")

    @allow_async_call
    def add_chatter(self, chat_id: str, user_ids: List[str] = [], open_ids: List[str] = []) -> AddChatterResponse:
        """拉用户进群

        Args:
            chat_id: 群ID
            open_ids: 自建应用提供用户ID, 数量限制200
            user_ids: 第三方应用提供用户ID, 数量限制200

        Returns:
            AddChatterResponse:
                invalid_user_ids
                invalid_open_ids
        """
        api = "/chat/v4/chatter/add/"
        payload = {
            "chat_id": chat_id
        }
        if user_ids:
            payload["user_ids"] = user_ids
        if open_ids:
            payload["open_ids"] = open_ids
        result = self.client.request("POST", api=api, payload=payload)
        response = AddChatterResponse(result.get("data", {}))
        response.chat_id = chat_id
        return response

    @allow_async_call
    def add_chatter_all(self, chat_id: str, user_ids: List[str] = [], open_ids: List[str] = [],
                        slice_size: int = FEISHU_BATCH_SEND_SIZE) -> AddChatterResponse:
        """拉全部用户进群, 不考虑200限制"""
        response = AddChatterResponse()
        while user_ids or open_ids:
            resp = self.add_chatter(chat_id, user_ids[:slice_size], open_ids[:slice_size])
            response.invalid_user_ids.extend(resp.invalid_user_ids)
            response.invalid_open_ids.extend(resp.invalid_open_ids)
            user_ids, open_ids = user_ids[slice_size:], open_ids[slice_size:]
        response.chat_id = chat_id
        return response

    @allow_async_call
    def remove_chatter(self, chat_id: str, user_ids: List[str] = [], open_ids: List[str] = []) -> RemoveChatterResponse:
        """移除用户出群

        Args:
            chat_id: 群ID
            open_ids: 自建应用提供用户ID, 数量限制200
            user_ids: 第三方应用提供用户ID, 数量限制200

        Returns:
            RemoveChatterResponse:
                invalid_user_ids
                invalid_open_ids
        """
        api = "/chat/v4/chatter/delete/"
        payload = {
            "chat_id": chat_id
        }
        if user_ids:
            payload["user_ids"] = user_ids
        if open_ids:
            payload["open_ids"] = open_ids
        result = self.client.request("POST", api=api, payload=payload)
        response = RemoveChatterResponse(result.get("data", {}))
        response.chat_id = chat_id
        return response

    @allow_async_call
    def remove_chatter_all(self, chat_id: str, user_ids: List[str] = [], open_ids: List[str] = [],
                           slice_size: int = FEISHU_BATCH_SEND_SIZE) -> RemoveChatterResponse:
        """移除全部用户出群, 不考虑200限制"""
        response = RemoveChatterResponse()
        while user_ids or open_ids:
            resp = self.remove_chatter(chat_id, user_ids[:slice_size], open_ids[:slice_size])
            response.invalid_user_ids.extend(resp.invalid_user_ids)
            response.invalid_open_ids.extend(resp.invalid_open_ids)
            user_ids, open_ids = user_ids[slice_size:], open_ids[slice_size:]
        response.chat_id = chat_id
        return response

    @allow_async_call
    def disband_chat(self, chat_id: str):
        """解散群

        如果解散失败会raise FeishuError, code/msg为飞书返回的失败原因
        """
        api = "/chat/v4/disband"
        payload = {"chat_id": chat_id}
        self.client.request("POST", api=api, payload=payload)

    @allow_async_call
    def create_chat_all(self, name: str = '', description: str = '',
                        open_ids: List[str] = [], user_ids: List[str] = [], i18n_names: dict = {},
                        only_owner_add: bool = False, share_allowed: bool = True,
                        only_owner_at_all: bool = False, only_owner_edit: bool = False,
                        slice_size: int = FEISHU_BATCH_SEND_SIZE) -> CreateChatResponse:
        """创建群

        和create_chat的区别是, create_chat的列表有200个的限制，这个没有
        先create_chat, 如果还没搞定就add_chatter_all
        """
        first_batch_open_ids, left_open_ids = open_ids[:slice_size], open_ids[slice_size:]
        first_batch_user_ids, left_user_ids = user_ids[:slice_size], user_ids[slice_size:]
        response = self.create_chat(name=name, description=description, i18n_names=i18n_names,
                                    open_ids=first_batch_open_ids, user_ids=first_batch_user_ids,
                                    only_owner_add=only_owner_add, share_allowed=share_allowed,
                                    only_owner_at_all=only_owner_at_all, only_owner_edit=only_owner_edit)
        if left_open_ids or left_user_ids:
            add_resp = self.add_chatter_all(chat_id=response.chat_id,
                                            user_ids=left_user_ids, open_ids=left_open_ids)
            response.invalid_open_ids.extend(add_resp.invalid_open_ids)
            response.invalid_user_ids.extend(add_resp.invalid_user_ids)
        return response

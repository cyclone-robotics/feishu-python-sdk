#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""消息管理相关API

包括:
- 发送文本、图片、富文本、名片消息
- 发送互动卡片消息
- 图片文本上传
- 发送通知消息

注意，被动消息接收在event.py中
"""
from enum import Enum
from typing import Optional, Union, Type, List

from .base import BaseAPI, allow_async_call
from ..consts import FEISHU_BATCH_SEND_SIZE
from ..errors import ERRORS, FeishuError
from ..models import (Message, TextMessage, TextContent, SendMsgType, Content, ImageMessage, PostMessage,
                      ShareChatMessage, ImageContent, I18nPost, PostContent, ShareChatContent, BatchSendResponse,
                      BatchMessage)

fileobj = Type
Image = Type


class ImageType(str, Enum):
    MESSAGE = "message"
    AVATAR = "avatar"

    def __str__(self):
        return self.value


def create_message(msg_type: SendMsgType, content: Content,
                   chat_id: str, open_id: str, user_id: str, email: str, root_id: str) -> Message:
    message_cls = {
        SendMsgType.TEXT: TextMessage,
        SendMsgType.IMAGE: ImageMessage,
        SendMsgType.POST: PostMessage,
        SendMsgType.SHARE_CHAT: ShareChatMessage,
    }[msg_type]
    msg = message_cls(
        msg_type=msg_type,
        content=content
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

    return msg


class MessageAPI(BaseAPI):
    """消息管理相关API

    https://open.feishu.cn/document/ukTMukTMukTM/uUjNz4SN2MjL1YzM
    """

    @allow_async_call
    def send(self, message: Union[Message, dict]) -> Optional[str]:
        """发送/v4/send请求, 返回message_id

        Args:
            message: Message类型或者一个简单的dict

        Returns:
            str: message_id

        Usages::

        >>> # from feishu import Message, SendMsgType, TextContent
        >>> # from feishu import FeishuClient
        >>> msg = Message(open_id='xxx', msg_type=SendMsgType.Text, content=TextContent(text="abc"))
        >>> # or
        >>> # msg = {"open_id": "xxx", "msg_type": "text", "content": {"text": "abc"}}
        >>>
        >>> client = FeishuClient(...)
        >>> client.send(msg)
        """
        api = "/message/v4/send/"
        if isinstance(message, Message):
            payload = message.dict(exclude_none=True)
        else:
            payload = message
        result = self.client.request("POST", api=api, payload=payload)
        return result.get("data", {}).get("message_id")

    @allow_async_call
    def send_text(self, text: str, open_id: str = '', user_id: str = '', email: str = '',
                  chat_id: str = '', root_id: str = '') -> Optional[str]:
        """发送文本消息

        Args:
            text: 待发送的文本信息
            open_id: 用户的飞信ID(自建应用)
            user_id: 用户的应用ID(三方应用)
            email: 用户的邮箱
            chat_id: 群ID, 以上4种ID必须提供一种, 优先级为chat_id>open_id>user_id>email
            root_id: 回复消息所对应的呃消息id, 可选
        """
        msg = create_message(SendMsgType.TEXT, content=TextContent(text=text),
                             root_id=root_id, chat_id=chat_id, open_id=open_id, user_id=user_id, email=email)

        if text.strip():
            return self.send(msg)
        else:
            self.logger.warning(f"text为空, 文本消息未发送: msg={msg}")

    @allow_async_call
    def send_image(self, image: Union[bytes, "fileobj", "Image"] = '',
                   image_file: str = '', image_url: str = '', image_key: str = '',
                   open_id: str = '', user_id: str = '', email: str = '',
                   chat_id: str = '', root_id: str = '') -> Optional[str]:
        """发送文本消息

        Args:
            image: 待发送的图片，可以是PIL.Image, bytes, fileobj
            image_file: 待发送图片文件路径
            image_url: 待发送图片的url
            image_key: 待发送图片的key, 飞书专用，以上4个必须提供一种，优先级为: image_key>image>image_file>image_url
            open_id: 用户的飞信ID(自建应用)
            user_id: 用户的应用ID(三方应用)
            email: 用户的邮箱
            chat_id: 群ID, 以上4种ID必须提供一种, 优先级为chat_id>open_id>user_id>email
            root_id: 回复消息所对应的呃消息id, 可选
        """
        if not image_key:
            image_key = self._get_image_key(image=image, image_file=image_file, image_url=image_url)

        print("image_key2", image_key)
        if image_key:
            msg = create_message(SendMsgType.IMAGE, content=ImageContent(image_key=image_key),
                                 root_id=root_id, chat_id=chat_id, open_id=open_id, user_id=user_id, email=email)
            print("msg=", msg.dict(exclude_none=True))
            return self.send(msg)
        else:
            self.logger.warning(f"没有提供image_key, image_url, image_file, 或image，图片未发送: msg={msg}")

    @allow_async_call
    def send_post(self, post: Union[dict, I18nPost],
                  open_id: str = '', user_id: str = '', email: str = '',
                  chat_id: str = '', root_id: str = '') -> Optional[str]:
        """发送富文本消息

        Args:
            post: dict或者I18nPost类型
            open_id: 用户的飞信ID(自建应用)
            user_id: 用户的应用ID(三方应用)
            email: 用户的邮箱
            chat_id: 群ID, 以上4种ID必须提供一种, 优先级为chat_id>open_id>user_id>email
            root_id: 回复消息所对应的呃消息id, 可选

        post参数示例
        {
            "zh_cn": {
                "title": "我是一个标题",
                "content": [
                    [
                        {
                            "tag": "text",
                            "un_escape": true,
                            "text": "第一行&nbsp;:"
                        },
                        {
                            "tag": "a",
                            "text": "超链接",
                            "href": "http://www.feishu.cn"
                        },
                        {
                            "tag": "at",
                            "user_id": "ou_18eac85d35a26f989317ad4f02e8bbbb"
                        }
                    ],
                ]
            }
        }
        """
        msg = create_message(msg_type=SendMsgType.POST, content=PostContent(post=post),
                             root_id=root_id, chat_id=chat_id, open_id=open_id, user_id=user_id, email=email)
        if not post.get('zh_cn') and not post.get('en_us'):
            self.logger.warning(f"没有提供zh_cn/en_us内容, 富文本未发送: msg={msg}")
        else:
            return self.send(msg)

    @allow_async_call
    def send_share_chat(self, share_chat_id: str,
                        open_id: str = '', user_id: str = '', email: str = '',
                        chat_id: str = '', root_id: str = '') -> Optional[str]:
        """发送群名片

         Args:
            share_chat_id: 群名片ID
            open_id: 用户的飞信ID(自建应用)
            user_id: 用户的应用ID(三方应用)
            email: 用户的邮箱
            chat_id: 群ID, 以上4种ID必须提供一种, 优先级为chat_id>open_id>user_id>email
            root_id: 回复消息所对应的呃消息id, 可选
        """
        msg = create_message(msg_type=SendMsgType.SHARE_CHAT, content=ShareChatContent(share_chat_id=share_chat_id),
                             root_id=root_id, chat_id=chat_id, open_id=open_id, user_id=user_id, email=email)
        if not share_chat_id.strip():
            return self.send(msg)
        else:
            self.logger.warning(f"share_chat_id为空, 群名片未分享: msg={msg}")

    @allow_async_call
    def batch_send_all(self, message: Union[Message, dict], department_ids: List[str], open_ids: List[str],
                       user_ids: List[str]) -> BatchSendResponse:
        """批量发送消息

        Args:
            message: 消息可以是文本/图片/富文本/群名片/卡片
            department_ids: API有200个的限制，这里取消了200个的限制，改为多次发送，并合并结果
            open_ids: API有200个的限制，这里取消了200个的限制，改为多次发送，并合并结果
            user_ids: API有200个的限制，这里取消了200个的限制，改为多次发送，并合并结果
        """
        slice_size = FEISHU_BATCH_SEND_SIZE
        response = BatchSendResponse()
        while department_ids or open_ids or user_ids:
            resp = self.batch_send(message, department_ids=department_ids, open_ids=open_ids, user_ids=user_ids)
            response.message_id = resp.message_id
            response.message_ids.append(resp.message_id)
            response.invalid_department_ids.extend(resp.invalid_department_ids)
            response.invalid_open_ids.extend(resp.invalid_open_ids)
            response.invalid_user_ids.extend(resp.invalid_user_ids)

            department_ids = department_ids[slice_size:]
            open_ids = open_ids[slice_size:]
            user_ids = user_ids[slice_size:]

        return response

    @allow_async_call
    def batch_send(self, message: Union[Message, dict], department_ids: List[str], open_ids: List[str],
                   user_ids: List[str]) -> BatchSendResponse:
        """和batch_send_all的区别是id有200个的限制"""
        api = "/message/v4/batch_send/"
        batch_msg = BatchMessage(
            department_ids=department_ids,
            open_ids=open_ids,
            user_ids=user_ids,
            msg_type=message.msg_type,
            content=message.content,
        )
        result = self.client.request(method="POST", api=api, payload=batch_msg.dict())
        return BatchSendResponse(**(result.get("data") or {}))

    @allow_async_call
    def upload_image(self, image: Union[bytes, "fileobj"], image_type: ImageType = "message") -> Optional[str]:
        """上传图片

        Args:
            image: 可以是bytes或fileobj
            image_type: 图片类型, 可以是message/avatar

        Returns:
            str: image_key
        """
        api = "/image/v4/put/"
        data = {"image_type": image_type}
        files = {"image": image}
        result = self.client.request(method="POST", api=api, data=data, files=files)
        return result.get("data", {}).get("image_key")

    @allow_async_call
    def get_image(self, image_key: str) -> bytes:
        """获取图片数据"""
        api = "/image/v4/get"
        params = {"image_key": image_key}
        # TODO: 这个API要搞清楚是不是直接返回，是的话需要修改通用的request类
        return self.client.request(method="GET", api=api, params=params)

    @allow_async_call
    def _get_image_key(self, image: Union[bytes, "fileobj", "Image"] = '',
                       image_file: str = '', image_url: str = '') -> str:
        """获取image_key

        Args:
            image: 图片本身
            image_file: 图片文件的路径
            image_url: 图片链接

        Returns:
            image_key, 如果失败则raise FeishuError
        """
        image_key = ''
        if image:
            try:
                if hasattr(image, "tobytes"):
                    image = image.tobytes()

                image_key = self.upload_image(image)
                assert image_key
            except Exception as e:
                raise FeishuError(ERRORS.INVALID_IMAGE_FILE_OR_CONTENT,
                                  f"上传图片失败: {str(e)} image={image[:20]}...")
        elif image_file:
            try:
                image_key = self.upload_image(open(image_file, "rb"))
            except Exception as e:
                raise FeishuError(ERRORS.INVALID_IMAGE_FILE_OR_CONTENT,
                                  f"上传图片失败: {str(e)} image_file={image_file}")
        elif image_url:
            try:
                content = self.client.fetch(method="GET", url=image_url)
            except Exception as e:
                raise FeishuError(ERRORS.INVALID_IMAGE_FILE_OR_CONTENT,
                                  f"下载图片失败: {str(e)} image_url={image_url}")
            try:
                image_key = self.upload_image(content)
                print("image_key", image_key)
            except Exception as e:
                raise FeishuError(ERRORS.INVALID_IMAGE_FILE_OR_CONTENT,
                                  f"上传图片失败: {str(e)} content={content[:20]}...")

        return image_key

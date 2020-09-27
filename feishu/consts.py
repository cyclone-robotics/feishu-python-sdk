#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum

FEISHU_TOKEN_EXPIRE_TIME = 7200  # token时效, https://open.feishu.cn/document/ukTMukTMukTM/uIjNz4iM2MjLyYzM
FEISHU_TOKEN_UPDATE_TIME = 600  # token提前更新的时间
FEISHU_BATCH_SEND_SIZE = 200  # 批量发送消息列表的大小限制

# 环境变量名
FEISHU_APP_ID = "FEISHU_APP_ID"
FEISHU_APP_SECRET = "FEISHU_APP_SECRET"
FEISHU_VERIFY_TOKEN = "FEISHU_VERIFY_TOKEN"
FEISHU_ENCRYPT_KEY = "FEISHU_ENCRYPT_KEY"


class AppType(str, Enum):
    TENANT = "tenant"  # 企业自建应用
    USER = "user"  # 第三方应用

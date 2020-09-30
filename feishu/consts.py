#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum

# token时效, https://open.feishu.cn/document/ukTMukTMukTM/uIjNz4iM2MjLyYzM
FEISHU_TOKEN_EXPIRE_TIME = 7200
FEISHU_TOKEN_UPDATE_TIME = 600  # token提前更新的时间
FEISHU_BATCH_SEND_SIZE = 200  # 批量发送消息列表的大小限制

# 环境变量名
FEISHU_APP_ID = "APP_ID"
FEISHU_APP_SECRET = "APP_SECRET"
FEISHU_VERIFY_TOKEN = "FEISHU_VERIFY_TOKEN"
FEISHU_ENCRYPT_KEY = "FEISHU_ENCRYPT_KEY"

FEISHU_PRIMER_APPROVAL_TOKEN = None
FEISHU_PRIMER_APPROVAL_SHEET_TOKEN = None
FEISHU_PRIMER_APPROVAL_SHEET_SHEET1_TOKEN = None

FEISHU_APPROVAL_SUBMIT_FORM = None

class AppType(str, Enum):
    TENANT = "tenant"  # 企业自建应用
    USER = "user"  # 第三方应用


# 请求地址及参数
# 用户登录验证
# Ref: https://open.feishu.cn/document/ukTMukTMukTM/uETOwYjLxkDM24SM5AjN
def FEISHU_LOGIN_REDIRECT_URL(state: int):
    return "https://open.feishu.cn/open-apis/authen/v1/index?redirect_uri=https://labw.org/lab/primer&app_id=" + FEISHU_APP_ID + "&state=" + str(state)


FEISHU_APP_ACCESS_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/"
FEISHU_TENANT_ACCESS_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
FEISHU_USER_IDENTITY_URL = "https://open.feishu.cn/open-apis/authen/v1/access_token"
FEISHU_USER_INFO_URL = "https://open.feishu.cn/open-apis/authen/v1/user_info"
FEISHU_USER_REFRESH_URL = "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token"

## 审核
## Ref: https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/ucDOyUjL3gjM14yN4ITN


FEISHU_APPROVAL_CREATE_URL = "https://www.feishu.cn/approval/openapi/v2/instance/create"
FEISHU_APPROVAL_GET_URL = "https://www.feishu.cn/approval/openapi/v2/instance/get"
FEISHU_APPROVAL_DEFINITION_URL = "https://www.feishu.cn/approval/openapi/v2/approval/get"
FEISHU_APPROVAL_APPROVE_URL = "https://www.feishu.cn/approval/openapi/v2/instance/approve"
FEISHU_APPROVAL_INSTANCE_LIST_URL = "https://www.feishu.cn/approval/openapi/v2/instance/list"
FEISHU_APPROVAL_REJECT_URL = "https://www.feishu.cn/approval/openapi/v2/instance/reject"
FEISHU_APPROVAL_TRANSFER_URL = "https://www.feishu.cn/approval/openapi/v2/instance/transfer"
FEISHU_APPROVAL_CANCEL_URL = "https://www.feishu.cn/approval/openapi/v2/instance/cancel"

## Document
## Ref: https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/uETMzUjLxEzM14SMxMTN

FEISHU_SHEET_META_DATA_URL = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/%s/metainfo"
FEISHU_SHEET_UPDATE_TITLE_URL = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/%s/properties"
FEISHU_SHEET_APPEND_DATA_URL = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/%s/values_append"
FEISHU_SHEET_PREPEND_URL = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/%s/values_prepend"
FEISHU_SHEET_ADD_RC_URL = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/%s/dimension_range"
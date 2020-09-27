# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Tuple

from .base import BaseAPI, allow_async_call


class AuthAPI(BaseAPI):
    @allow_async_call
    def get_tenant_access_token(self) -> Tuple[str, int]:
        """获取自建应用的token

        https://open.feishu.cn/document/ukTMukTMukTM/uIjNz4iM2MjLyYzM

        Returns:
            Tuple[token, expire]
        """
        api = "/auth/v3/tenant_access_token/internal/"
        payload = dict(
            app_id=self.client.app_id,
            app_secret=self.client.app_secret,
        )
        result = self.client.request("POST", api=api, payload=payload, auth=False)
        # 返回 Body ：
        # {
        #     "code":0,
        #     "msg":"ok",
        #     "tenant_access_token":"xxxxx",
        #     "expire":7200  // 过期时间，单位为秒（两小时失效）
        # }
        return result["tenant_access_token"], result["expire"]

    def resend_app_ticket(self):
        """重新推送app_ticket

        https://open.feishu.cn/document/ukTMukTMukTM/uQjNz4CN2MjL0YzM
        """
        NotImplementedError

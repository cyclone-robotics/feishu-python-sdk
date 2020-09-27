from .auth import AuthAPI
from .base import allow_async_call
from .bot import BotAPI
from .card import CardAPI
from .message import MessageAPI


class FeishuAPI(AuthAPI, MessageAPI, CardAPI, BotAPI):
    """飞书API

    实现API的简单示例::

    >>> class DemoAPI(BaseAPI):
    ...     @allow_async_call
    ...     def demo_api(self, arg1, arg2) -> dict:
    ...         params, payload = do_something_with_arguments(arg1, arg2)
    ...         result = self.client.request(api, params, payload)
    ...         result = do_something_with_result(result)
    ...         return result

    这里client就是FeishuClient的示例，封装了统一调度的网络方法request
    api = /auth/v3/tenant_access_token/internal/
    params, payload为url参数和body参数，可为空不传

    注意:
        为了让allow_async_call的hack起作用，
        请一定要通过`result = self.client.request`或者`result = self.client.fetch_url`来发起通用请求，
        否则可能会造在异步代码中执行同步请求，卡住event_loop的问题
    """

    def __init__(self, feishu_client: "FeishuClient"):
        self.client = feishu_client
        # 执行allow_async_call里面的hack
        self.dummy()

    @allow_async_call
    def dummy(self):
        """这是一个用来初始化async函数的API"""
        pass

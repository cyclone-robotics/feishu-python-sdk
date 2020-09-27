import asyncio
from asyncio import Future
from typing import Union

from feishu.apis.base import allow_async_call


class TheClient:
    run_async = True
    event_loop = asyncio.get_event_loop()

    def request(self, arg: str) -> Union[str, Future]:
        if self.run_async:
            async def _async():
                return arg

            return asyncio.ensure_future(_async(), loop=self.event_loop)
        else:
            return arg


class TheAPI:
    client = TheClient()

    @allow_async_call
    def the_method(self, arg1: str) -> str:
        arg2 = arg1 + "2"
        result = self.client.request(arg2)
        return result


def test_sync_call():
    api = TheAPI()
    api.client.run_async = False
    assert "sync2" == api.the_method("sync")
    print("sync2")


def test_async_call():
    api = TheAPI()
    api.client.run_async = True
    future: asyncio.Future = api.the_method("async")
    api.client.event_loop.run_until_complete(future)
    assert "async2" == future.result()
    print("async2")


if __name__ == "__main__":
    test_async_call()
    test_sync_call()

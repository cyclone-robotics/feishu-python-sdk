import asyncio

from feishu import FeishuClient

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
cli = FeishuClient(run_async=False)
cli_async = FeishuClient(run_async=True)


def test_tenant_access_token():
    token, expire = cli.get_tenant_access_token()
    assert token and expire > 0, "其实一般到不了这一步，要出错之前就出错了"
    assert token and expire

    token, expire = loop.run_until_complete(cli_async.get_tenant_access_token())
    assert token and expire
    print(f"token={token}, expire={expire}")


def test_bot_info():
    bot_info = cli.get_bot_info()
    assert bot_info
    bot_info = loop.run_until_complete(cli_async.get_bot_info())
    assert bot_info
    print(f"bot_info={bot_info}")


if __name__ == "__main__":
    test_tenant_access_token()
    test_bot_info()

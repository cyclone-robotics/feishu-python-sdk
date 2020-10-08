# feishu-python-sdk

一个用于和飞书开放平台交互的python库 (feishu-python-sdk)

特性

- Python3.7+, Type Hints!
- Pydantic类型检查
- 使用了黑科技，API同时支持同步调用和异步调用
- 实现了订阅事件和卡片交互回调(其他开源库都没实现这个, 只能算feishu-client)
- 除了标准API外，还封装了一些语法糖调用方法, 比如绕过200元素限制等等

TODO

- [ ] 多写点测试, 目前coverage = 35%
- [ ] 多实现点接口, 目前实现了机器人和消息相关

## 使用说明

```
pip install feishu-python-sdk
```

运行测试用例

```shell
export FEISHU_APP_ID=飞书应用的APP_ID
export FEISHU_APP_SECRET=飞书应用的APP_SECRET
export FEISHU_VERIFY_TOKEN=飞书应用“事件订阅”的VERIFY_TOKEN参数
export FEISHU_ENCRYPT_KEY=飞书应用“事件订阅”的ENCRYPT_KEY参数
PYTHONPATH=. pytest --cov
```

### API调用示例

```python
from feishu import FeishuClient
client = FeishuClient(app_id=..., app_secret=...)
print(client.get_bot_info())
# activate_status=<BotActivateStatus.INITIALIZED: 0> app_name='Chatbot测试' 
# avatar_url='https://s3-fs.pstatp.com/static-resource/v1/0a04c4b7-4edd-4cb3-a277-a1f6c609af4g'
# ip_white_list=[] open_id='ou_b71f3874109c927c1c0a4f68ba512f69'
```

如果配置了环境变量，初始化的时候也可以省略参数

```python
client = FeishuClient()
```

更多API见`apis`目录

### 在异步框架中调用API

也可以异步调用，注意，异步调用需要在运行任意API之前先配置event_loop

```python
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from feishu import FeishuClient
client = FeishuClient(app_id=..., app_secret=..., run_async=True, event_loop=loop)

print(loop.run_until_complete(client.get_bot_info()))
```

有可能你会注意到同一个方法`get_bot_info`，它既能在同步下使用，又能在异步下使用。

这是因为再内部实现了一个名为`allow_async_call`的decorator, 用于半动态生成所有API的async版本, async版本会自动使用async版本的网络调用, 并把函数的返回通过`asyncio.ensure_future`调用修改成`asyncio.Future`

具体实现方式可以参考`feishu.apis.base.allow_async_call`, 以及`feishu.client.request`, `feishu.client.fetch`。

### 订阅事件和卡片交互回调

**订阅事件**需要在飞书后台开启订阅权限，然后配置回调地址，飞书会在更改配置以及应用、消息、群组等事件发生时向回调地址发送请求

参见飞书文档 <https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM>

所有飞书消息都定义在`feishu.events`中, 飞书发送的请求类似如下

```json
{ 
    "ts": "1502199207.7171419", // 事件发送的时间，一般近似于事件发生的时间。 
    "uuid": "bc447199585340d1f3728d26b1c0297a",  // 事件的唯一标识
    "token": "41a9425ea7df4536a7623e38fa321bae", // 即Verification Token 
    "type": "event_callback", // event_callback-事件推送，url_verification-url地址验证
    "event": { ... } // 不同事件此处数据不同 
}
```

对应sdk的类型为`events.Event`, 本sdk提供了flask和sanic的blueprint, 通常只需要实现`on_event`方法即可

以flask为例, 写一个flask的订阅事件并打印的服务只要这样即可

```python
from feishu import setup_event_blueprint, Event
from flask import Flask, Blueprint

app = Flask(__name__)

PATH_EVENT = '/feishu/event/callback'
VERIFY_TOKEN = ''  # 为空则不校验verify_token
ENCRYPT_KEY = ''  # 飞书应用没启用encrypt_key的话可以不填


def on_event(event: Event):
    print(event)


event_app = Blueprint(name="event_app", import_name=__name__)
setup_event_blueprint("flask", blueprint=event_app, path=PATH_EVENT,
                      on_event=on_event, verify_token=VERIFY_TOKEN, encrypt_key=ENCRYPT_KEY)
app.register_blueprint(event_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
```

然后运行，并在飞书后台配好可以访问此地址`http://HOST:9999/feishu/event/callback`的服务，配置好以后试着和应用对话即可

更简单的方法是，配置好环境变量后，直接运行以下代码

```
python -m feishu.server
```

这会启用event和action两种回调服务，方便后续做开发和调试

其中action为飞书交互卡片的交互事件回调，具体文档可见 https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN2ATN

强烈建议看一下`fesihu.server`中的实现

## 定制feishu-python-sdk

```
git clone https://github.com/cyclone-robotics/feishu-python-sdk
cd feishu-python-sdk
pip install -e .
```

然后对`feishu-python-sdk`目录的修改就都可以直接在调用中生效了

## API实现功能列表

- [ ] 授权
  - [x] 获取 app_access_token（企业自建应用）
  - [ ] 获取 app_access_token（应用商店应用）
  - [ ] 获取 tenant_access_token（企业自建应用）
  - [ ] 获取 tenant_access_token（应用商店应用）
  - [ ] 重新推送 app_ticket
- [ ] 身份验证
  - [ ] 请求身份验证
  - [ ] 获取登录用户身份
  - [ ] 刷新access_token
  - [ ] 获取用户信息
- [ ] 通讯录
  - [ ] 获取通讯录授权范围
  - [ ] 获取子部门列表
  - [ ] 获取子部门 ID 列表
  - [ ] 获取部门详情
  - [ ] 批量获取部门详情
  - [ ] 获取部门用户列表
  - [ ] 获取部门用户详情
  - [ ] 获取企业自定义用户属性配置
  - [ ] 批量获取用户信息
  - [ ] 新增用户
  - [ ] 更新用户信息
  - [ ] 删除用户
  - [ ] 新增部门
  - [ ] 更新部门信息
  - [ ] 删除部门
  - [ ] 批量新增用户
  - [ ] 批量新增部门
  - [ ] 查询批量任务执行状态
  - [ ] 获取应用管理员管理范围
  - [ ] 获取角色列表
  - [ ] 获取角色成员列表
- [ ] 用户信息
  - [ ] 使用手机号或邮箱获取用户 ID
- [ ] 应用信息
  - [ ] 获取应用管理权限
  - [ ] 获取应用在企业内的可用范围
  - [ ] 获取用户可用的应用
  - [ ] 获取企业安装的应用
  - [ ] 更新应用可用范围
  - [ ] 设置用户可用应用
- [ ] 应用商店计费信息
  - [ ] 查询用户是否在应用开通范围
  - [ ] 查询租户购买的付费方案
  - [ ] 查询订单详情
- [ ] 群组
  - [ ] 获取用户所在的群列表
  - [ ] 获取群成员列表
  - [ ] 搜索用户所在的群列表
- [ ] 机器人
  - [x] 批量发送消息
  - [x] 发送文本消息
  - [x] 发送图片消息
  - [x] 发送富文本消息
  - [x] 发送群名片
  - [ ] 消息撤回
  - [x] 发送卡片通知
  - [x] 群信息和群管理
    - [x] 创建群
    - [x] 获取群列表
    - [x] 获取群信息
    - [x] 更新群信息
    - [x] 拉用户进群
    - [x] 移除用户出群
    - [x] 解散群
  - [x] 机器人信息与管理
    - [x] 拉机器人进群
- [ ] 日历
  - [ ] 获取日历
  - [ ] 获取日历列表
  - [ ] 创建日历
  - [ ] 删除日历
  - [ ] 更新日历
  - [ ] 获取日程
  - [ ] 创建日程
  - [ ] 获取日程列表
  - [ ] 删除日程
  - [ ] 更新日程
  - [ ] 邀请/移除日程参与者
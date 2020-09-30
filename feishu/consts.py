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

FEISHU_APPROVAL_SUBMIT_FORM = NONE

class AppType(str, Enum):
    TENANT = "tenant"  # 企业自建应用
    USER = "user"  # 第三方应用


# 请求地址及参数
# 用户登录验证
# Ref: https://open.feishu.cn/document/ukTMukTMukTM/uETOwYjLxkDM24SM5AjN
def FEISHU_LOGIN_REDIRECT_URL(state: int):
    return "https://open.feishu.cn/open-apis/authen/v1/index?redirect_uri=https://labw.org/lab/primer&app_id=" + FEISHU_APP_ID + "&state=" + str(state)


FEISHU_APP_ACCESS_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/"
'''
method = POST
请求参数说明
请求 Header ：

参数	类型	必填/选填	说明	默认值	实例
Content-Type	string	必填	Content-Type		application/json
请求参数 ：

参数	类型	必填/选填	说明	默认值	实例
app_id	string	必填	应用唯一标识，创建应用后获得		cli_slkdjalasdkjasd
app_secret	string	必填	应用秘钥，创建应用后获得		dskLLdkasdjlasdKK

返回参数说明 :

参数	类型	说明
code	int	错误码，非 0 表示失败
msg	string	错误描述
app_access_token	string	访问 token
expire	int	app_access_token 过期时间
tenant_access_token	string	已废弃
'''

FEISHU_TENANT_ACCESS_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
'''
method = POST
请求参数说明
请求 Header ：

参数	类型	必填/选填	说明	默认值	实例
Content-Type	string	必填	Content-Type		application/json
请求参数 ：

返回参数说明 :

参数	类型	说明
code	int	错误码，非 0 表示失败
msg	string	错误描述
tenant_access_token	string	访问 token
expire	int	tenant_access_token 过期时间
'''

FEISHU_USER_IDENTITY_URL = "https://open.feishu.cn/open-apis/authen/v1/access_token"
'''
method = POST
请求参数说明 :

参数	类型	必须	说明
app_access_token	string	是	应用的 app_access_token，必须与请求身份验证中的应用保持一致
grant_type	string	是	在本流程中，此值为 authorization_code
code	string	是	来自请求身份验证(新)流程，用户扫码登录后会自动302到redirect_uri并带上此参数


返回参数说明 :

参数	说明
code	返回码，0表示请求成功，其他表示请求失败
msg	返回信息
data	返回业务数据
 ∟access_token	user_access_token，用于获取用户资源
 ∟avatar_url	用户头像
 ∟avatar_thumb	用户头像 72x72
 ∟avatar_middle	用户头像 240x240
 ∟avatar_big	用户头像 640x640
 ∟expires_in	access_token 的有效期，单位: 秒
 ∟name	用户姓名
 ∟en_name	用户英文名称
 ∟open_id	用户在应用内的唯一标识
 ∟tenant_key	当前企业标识
 ∟refresh_expires_in	refresh_token 的有效期，单位: 秒
 ∟refresh_token	刷新用户 access_token 时使用的 token
 ∟token_type	此处为 Bearer
'''

FEISHU_USER_INFO_URL = "https://open.feishu.cn/open-apis/authen/v1/user_info"
'''
method = GET
请求参数说明 :

参数	类型	必须	说明
app_access_token	string	是	应用的 app_access_token，必须与请求身份验证中的应用保持一致
grant_type	string	是	在本流程中，此值为 authorization_code
code	string	是	来自请求身份验证(新)流程，用户扫码登录后会自动302到redirect_uri并带上此参数

返回参数说明 :

参数	说明
code	返回码，0表示请求成功，其他表示请求失败
msg	返回信息
data	返回业务数据
	 ∟access_token	user_access_token，用于获取用户资源
	 ∟avatar_url	用户头像
	 ∟avatar_thumb	用户头像 72x72
	 ∟avatar_middle	用户头像 240x240
	 ∟avatar_big	用户头像 640x640
	 ∟expires_in	access_token 的有效期，单位: 秒
	 ∟name	用户姓名
	 ∟en_name	用户英文名称
	 ∟open_id	用户在应用内的唯一标识
	 ∟tenant_key	当前企业标识
	 ∟refresh_expires_in	refresh_token 的有效期，单位: 秒
	 ∟refresh_token	刷新用户 access_token 时使用的 token
	 ∟token_type	此处为 Bearer

'''

FEISHU_USER_REFRESH_URL = "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token"

'''
method = POST
参数	类型	必须	说明
app_access_token	string	是	应用的 app_access_token，必须与请求身份验证中的应用保持一致
grant_type	string	是	本流程中，此值为 refresh_token
refresh_token	string	是	来自获取登录用户身份(新) 或 本接口返回值

返回参数说明 :

参数	说明
code	返回码，0表示请求成功，其他表示请求失败
msg	返回信息
data	返回业务数据
 ∟access_token	user_access_token，用于获取用户资源
 ∟avatar_url	用户头像
 ∟avatar_thumb	用户头像 72x72
 ∟avatar_middle	用户头像 240x240
 ∟avatar_big	用户头像 640x640
 ∟expires_in	access_token 的有效期，单位: 秒
 ∟name	用户姓名
 ∟en_name	用户英文名称
 ∟open_id	用户在应用内的唯一标识
 ∟tenant_key	当前企业标识
 ∟refresh_expires_in	refresh_token 的有效期，单位: 秒
 ∟refresh_token	刷新用户 access_token 时使用的 token
 ∟token_type	此处为 Bearer
'''


## 审核
## Ref: https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/ucDOyUjL3gjM14yN4ITN


FEISHU_APPROVAL_CREATE_URL = "https://www.feishu.cn/approval/openapi/v2/instance/create"
'''
method = POST
请求 Header ：

key	value
Authorization	Bearer tenant_access_token
Content-Type	application/json

请求参数说明：
参数	类型	必须	说明
approval_code	String	是	审批定义 code
user_id	String	是	发起审批用户
open_id	String	否	发起审批用户 open id, 如果传了 user_id 则优先使用 user_id
department_id	String	否	发起审批用户部门，如果用户只属于一个部门，可以不填，如果属于多个部门，必须填其中一个部门
form	String	是	json 数组，控件值
	∟id	String	是	控件 ID，也可以使用自定义 ID custom_id 的值
	∟type	String	是	控件类型
	∟value	String	是	控件值，不同类型的值格式不一样
node_approver_user_id_list	map	否	如果有发起人自选节点，则需要填写对应节点的审批人
key: node id 或 custom node id , 通过 查看审批定义 获取
value: 审批人列表
node_approver_open_id_list	map	否	发起人自选 open id
uuid	String	否	审批实例 uuid，用于幂等操作，同一个 uuid 只能用于创建一个审批实例，如果冲突，返回错误码 60012 ，格式必须为 XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX，不区分大小写

返回参数说明：
返回参数说明 :

参数	类型	必须	说明
code	int	是	错误码，非0表示失败
msg	String	是	返回码的描述
data	map	是	返回业务信息
 ∟instance_code	String	是	审批实例 Code
'''

FEISHU_APPROVAL_GET_URL = "https://www.feishu.cn/approval/openapi/v2/instance/get"
'''
请求参数说明 :

参数	类型	必须	说明
instance_code	String	是	审批实例 Code
locale	String	否	zh-CN - 中文
en-US - 英文

see https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/uEDNyUjLxQjM14SM0ITN
'''

FEISHU_APPROVAL_DEFINITION_URL = "https://www.feishu.cn/approval/openapi/v2/approval/get"
'''
method = POST
请求Header
key	value
Authorization	Bearer tenant_access_token
Content-Type	application/json

请求参数说明 :

参数	类型	必须	说明
approval_code	String	是	审批定义 Code
locale	String	否	zh-CN - 中文
en-US - 英文

返回参数说明 :

参数	类型	必须	说明
code	int	是	错误码，非 0 表示失败
msg	String	是	返回码的描述
data	map	是	返回业务信息
 ∟approval_name	String	是	审批名称
 ∟form	String	是	json 数组，控件信息
  ∟id	String	是	控件 ID
  ∟custom_id	String	否	控件自定义 ID
  ∟name	String	是	控件名称
  ∟type	String	是	控件类型
 ∟node_list	list	是	节点信息
  ∟name	String	是	节点名称
  ∟need_approver	bool	是	是否发起人自选节点
true - 发起审批时需要提交审批人
  ∟node_id	String	是	节点 ID
  ∟custom_node_id	String	否	节点自定义 ID，如果没有设置则不返回
  ∟node_type	String	是	审批方式
AND -会签
OR - 或签
'''

FEISHU_APPROVAL_APPROVE_URL = "https://www.feishu.cn/approval/openapi/v2/instance/approve"
'''
请求参数说明 :

参数	类型	必须	说明
Authorization	String	是	tenant_access_token 为具体的租户访问 token
approval_code	String	是	审批定义 Code
instance_code	String	是	审批实例 Code
user_id	String	是	操作用户
task_id	String	是	任务 ID
comment	String	否	意见
返回参数说明 :

参数	类型	必须	说明
code	int	是	错误码，非0表示失败
msg	String	是	返回码的描述
'''
FEISHU_APPROVAL_INSTANCE_LIST_URL = "https://www.feishu.cn/approval/openapi/v2/instance/list"
FEISHU_APPROVAL_REJECT_URL = "https://www.feishu.cn/approval/openapi/v2/instance/reject"
'''
请求参数说明 :

参数	类型	必须	说明
Authorization	String	是	tenant_access_token 为具体的租户访问 token
approval_code	String	是	审批定义 Code
instance_code	String	是	审批实例 Code
user_id	String	是	操作用户
task_id	String	是	任务 ID
comment	String	否	意见
返回参数说明 :

参数	类型	必须	说明
code	int	是	错误码，非0表示失败
msg	String	是	返回码的描述
'''

FEISHU_APPROVAL_TRANSFER_URL = "https://www.feishu.cn/approval/openapi/v2/instance/transfer"
'''
请求参数说明 :

参数	类型	必须	说明
Authorization	String	是	tenant_access_token 为具体的租户访问 token
approval_code	String	是	审批定义 Code
instance_code	String	是	审批实例 Code
user_id	String	是	操作用户
task_id	String	是	任务 ID
comment	String	否	意见
transfer_user_id	String	是	被转交人唯一 ID
返回参数说明 :

参数	类型	必须	说明
code	int	是	错误码，非0表示失败
msg	String	是	返回码的描述

'''

FEISHU_APPROVAL_CANCEL_URL = "https://www.feishu.cn/approval/openapi/v2/instance/cancel"
'''
请求参数说明 :

参数	类型	必须	说明
Authorization	String	是	tenant_access_token 为具体的租户访问 token
approval_code	String	是	审批定义Code
instance_code	String	是	审批实例Code
user_id	String	是	操作用户

返回参数说明 :

参数	类型	必须	说明
code	int	是	错误码，非0表示失败
msg	String	是	返回码的描述

'''

## Documents
## Ref: https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/uETMzUjLxEzM14SMxMTN

FEISHU_SHEET_META_DATA_URL = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/%s/metainfo"
'''
method = GET
请求Header:

key	value
Authorization	Bearer user_access_token
Content-Type	application/json

请求参数说明 :

参数	类型	必须	说明     	来源
Authorization	string	是	user_access_token 通过接口 获取登录用户身份 或者 code2session 获得 ；注意内容不要漏了 "Bearer "	请求 Header
spreadsheetToken	string	是	sheet 的 token，获取方式见 对接前说明的第 4 项	URL PATH

返回参数说明:

参数	说明
spreadsheetToken	sheet的token
properties	sheet 的属性
 ∟title	sheet 的标题
 ∟ownerUser	所有者的 id
 ∟sheetCount	spreadsheet 下的 sheet 数
 ∟revision	该 sheet 的版本
sheets	spreadsheet 下的sheet列表
 ∟sheetId	sheet 的 id
 ∟title	sheet 的标题
 ∟index	该 sheet 的位置
 ∟rowCount	该 sheet 的最大行数
 ∟columnCount	该 sheet 的最大列数
 ∟merges	该 sheet 中合并单元格的范围
  ∟startRowIndex	合并单元格范围的开始行下标，index 从 0 开始
  ∟startColumnIndex	合并单元格范围的开始列下标，index 从 0 开始
  ∟rowCount	合并单元格范围的行数量
  ∟columnCount	合并单元格范围的列数量
'''

FEISHU_SHEET_UPDATE_TITLE_URL = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/%s/properties"
'''
method = PUT
请求参数说明 :

参数	类型	必须	说明         	来源
Authorization	string	是	user_access_token 通过接口 获取登录用户身份 或者 code2session 获得；注意内容不要漏了 "Bearer "	请求 Header
spreadsheetToken	string	是	spreadsheet 的 token，获取方式见 对接前说明 的第 4 项	URL PATH
properties		是	spreadsheet 的属性	请求 body
 ∟title	string	是	spreadsheet 的标题，最大长度100个字符	请求 body

返回参数说明:

参数	说明
updateSpreadsheet	返回更新表格属性后该 spreadsheet 的属性
 ∟spreadsheetToken	spreadsheet 的 token
 ∟title	spreadsheet 的标题
'''

FEISHU_SHEET_APPEND_DATA_URL = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/%s/values_append"
'''
method = POST
Body:

{
"valueRange":{
    "range": "string",
    "values": [
       [
          "string", 1 , "http://www.xx.com"
       ]
  ]
}
}

请求参数说明 :
参数	类型	必须	说明	来源
Authorization	string	是	user_access_token 通过接口 获取登录用户身份 或者 code2session 获得。注意内容不要漏了 "Bearer "	请求 Header
spreadsheetToken	string	是	spreadsheet 的 token，获取方式见 对接前说明 的第 4 项	URL PATH
insertDataOption	string	否	遇到空行追加，默认 OVERWRITE， 若空行的数量小于追加数据的行数 则覆盖数据 append；可选 INSERT_ROWS ，会在插入足够数量的行后再 append	URL Param
valueRange		是	值与范围	请求body
 ∟range	string	是	查询范围 range=<sheetId>!<开始格子>:<结束格子> 如：xxxx!A1:D5，详见 对接前说明 的第 5 项	请求 body
 ∟values	array<interface>	是	需要写入的值，如要写入超链接、emial、@人等，可详看附录sheet 支持写入数据类型	请求 body

返回参数说明:

参数	说明
spreadsheetToken	sheet 的 token
tableRange	写入的范围
updates	插入数据的范围、行列数等
 ∟spreadsheetToken	sheet 的 token
 ∟updatedRange	写入的范围
 ∟updatedRows	写入的行数
 ∟updatedColumns	写入的列数
 ∟updatedCells	写入的单元格总数
 ∟revision	sheet 的版本号
revision	sheet 的版本号
'''

FEISHU_SHEET_PREPEND_URL = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/%s/values_prepend"
'''
method = POST
{
"valueRange":{
  "range": "string",
  "values": [
    [
      "string",1 ,"http://www.xx.com"
    ]
  ]
  }
}
请求参数说明 :

参数	类型	必须	说明	来源
Authorization	string	是	user_access_token 通过接口 获取登录用户身份 或者 code2session 获得；注意内容不要漏了 "Bearer "	请求 Header
spreadsheetToken	string	是	sheet的token，获取方式见 对接前说明 的第 4 项	URL PATH
valueRange		是	值与范围	请求body
 ∟range	string	是	查询范围 range=<子sheetId>!<开始格子>:<结束格子> 如：xxxx!A1:D5，详见 对接前说明 的第 5 项	请求 body
 ∟values	array<interface>	是	需要写入的值，如要写入超链接、email、@人等，可详看附录sheet 支持写入数据类型	请求 body

返回参数说明:

参数	说明
spreadsheetToken	sheet 的 token
tableRange	写入的范围
updates	插入数据的范围、行列数等
 ∟spreadsheetToken	sheet 的 token
 ∟updatedRange	写入的范围
 ∟updatedRows	写入的行数
 ∟updatedColumns	写入的列数
 ∟updatedCells	写入的单元格总数
 ∟revision	sheet 的版本号
revision	sheet 的版本号
'''


FEISHU_SHEET_ADD_RC_URL = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/%s/dimension_range"
'''
method = POST
Body:
{
  "dimension":{
       "sheetId": "string",
        "majorDimension": "ROWS",
        "length": 1
     }
}

请求参数说明 :

参数	类型	必须	说明	来源
Authorization	string	是	user_access_token 通过接口 获取登录用户身份 或者 code2session 获得；注意内容不要漏了 "Bearer "	请求 Header
spreadsheetToken	string	是	spreadsheet 的 token，详见 对接前说明 的第 5 项	URL PATH
dimension		是	需要增加行列的维度信息	请求 body
 ∟sheetId	string	是	sheetId	请求 body
 ∟majorDimension	string	否	默认 ROWS ，可选 ROWS、COLUMNS	请求 body
 ∟length	int	是	要增加的行/列数,0<length<5000	请求 body

返回参数说明:

参数	说明
addCount	增加的行/列数
majorDimension	插入维度
'''

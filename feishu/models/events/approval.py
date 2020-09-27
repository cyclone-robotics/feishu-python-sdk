#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""飞书审批事件

https://open.feishu.cn/document/ukTMukTMukTM/uQTNxYjL0UTM24CN1EjN
"""
from enum import Enum
from typing import List

from .base import BaseModel, EventType, EventContent


class TimeUnit(str, Enum):
    DAY = "DAY"
    HALF_DAY = "HALF_DAY"
    HOUR = "HOUR"


class LeaveApprovalEvent(EventContent):
    """请假审批

    {
         "app_id": "cli_xxx",
         "tenant_key":"xxx",
         "type": "leave_approval",
         "instance_code": "xxx", // 审批实例Code
         "employee_id": "xxx",  // 用户id
         "start_time": 1502199207, // 审批发起时间
         "end_time": 1502199307,   // 审批结束时间
         "leave_type": "xxx",      // 请假类型
         "leave_unit": 1,          // 请假最小时长：1：一天，2：半天
         "leave_start_time": "2018-12-01 12:00:00", // 请假开始时间
         "leave_end_time": "2018-12-02 12:00:00",   // 请假结束时间
         "leave_interval": 7200,          // 请假时长，单位（秒）
         "leave_reason": "xxx"     // 请假事由
    }
    """
    app_id: str
    tenant_key: str
    type: EventType = EventType.LEAVE_APPROVAL
    instance_code: str
    employee_id: str
    start_time: int
    end_time: int
    leave_type: str
    leave_unit: int
    leave_start_time: str
    leave_end_time: str
    leave_interval: int
    leave_reason: str


class I18nResource(BaseModel):
    """
    {
        "locale":"en_us",
        "is_default":true,
        "texts":{
            "@i18n@123456":"Holiday"
        }
    }
    """
    locale: str
    is_default: bool
    texts: dict


class LeaveApprovalV2Event(EventContent):
    """新版请假消息

    {
         "app_id": "cli_xxx",
         "tenant_key":"xxx",
         "type": "leave_approvalV2",
         "instance_code": "xxx", // 审批实例Code
         "user_id": "xxx",  // 用户id
         "start_time": 1564590532,  // 审批发起时间
         "end_time": 1564590532, // 审批结束时间
         "leave_name": "@i18n@123456",  // 假期名称
         "leave_unit": "DAY",  // 请假最小时长
         "leave_start_time": "2019-10-01 00:00:00",// 请假开始时间
         "leave_end_time":"2019-10-02 00:00:00",// 请假结束时间
         "leave_detail": [
            ["2019-10-01 00:00:00","2019-10-02 00:00:00"]
         ], // 具体请假明细
        "leave_interval": 86400,  // 请假时长，单位（秒）
        "leave_reason": "abc", // 请假事由
        "i18n_resources":[ {
                "locale":"en_us",
                "is_default":true,
                "texts":{
                    "@i18n@123456":"Holiday"
                }
        }  ] // 国际化文案
    }
    """
    app_id: str
    tenant_key: str
    type: EventType = EventType.LEAVE_APPROVAL_V2
    instance_code: str
    user_id: str
    start_time: int
    end_time: int
    leave_name: str
    leave_unit: TimeUnit
    leave_start_time: str
    leave_end_time: str
    leave_detail: List[List[str]]
    leave_interval: int
    leave_reason: str
    i18n_resources: List[I18nResource]


class WorkApprovalEvent(EventContent):
    """加班审批

    {
         "app_id": "cli_xxx",
         "tenant_key":"xxx",
         "type":"work_approval",
         "instance_code": "xxx", // 审批实例Code
         "employee_id": "xxx",  // 用户id
         "start_time": 1502199207, // 审批发起时间
         "end_time": 1502199307,   // 审批结束时间
         "work_type": "xxx",      // 加班类型
         "work_start_time": "2018-12-01 12:00:00", // 加班开始时间
         "work_end_time": "2018-12-02 12:00:00",   // 加班结束时间
         "work_interval": 7200,          // 加班时长，单位（秒）
         "work_reason": "xxx"     // 加班事由
    }
    """
    app_id: str
    tenant_key: str
    type: EventType = EventType.WORK_APPROVAL
    instance_code: str
    employee_id: str
    start_time: int
    end_time: int
    work_type: str
    work_start_time: str
    work_end_time: str
    work_interval: int
    work_reason: str


class ShiftApprovalEvent(EventContent):
    """换班审批

    {
         "app_id": "cli_xxx",
         "tenant_key":"xxx",
         "type":"shift_approval",
         "instance_code": "xxx", // 审批实例Code
         "employee_id": "xxx",  // 用户id
         "start_time": 1502199207, // 审批发起时间
         "end_time": 1502199307,   // 审批结束时间
         "shift_time": "2018-12-01 12:00:00",    // 换班时间
         "return_time": "2018-12-02 12:00:00",   // 还班时间
         "shift_reason": "xxx"     // 换班事由
    }
    """
    app_id: str
    tenant_key: str
    type: EventType = EventType.REMEDY_APPROVAL
    instance_code = str
    employee_id: str
    start_time: int
    end_time: int
    shift_time: str
    return_time: str
    shift_reason: str


class RemedyApprovalEvent(EventContent):
    """补卡审批

    {
         "app_id": "cli_xxx",
         "tenant_key":"xxx",
         "type":"remedy_approval",
         "instance_code": "xxx", // 审批实例Code
         "employee_id": "xxx",  // 用户id
         "start_time": 1502199207, // 审批发起时间
         "end_time": 1502199307,   // 审批结束时间
         "remedy_time": "2018-12-01 12:00:00",   // 补卡时间
         "remedy_reason": "xxx"    // 补卡原因
    }
    """
    app_id: str
    tenant_key: str
    type: EventType = EventType.REMEDY_APPROVAL
    instance_code = str
    employee_id: str
    start_time: int
    end_time: int
    remedy_time: str
    remedy_reason: str


class Schedule(BaseModel):
    """
    {         // Schedule 结构数组
        "trip_start_time": "2018-12-01 12:00:00", // 行程开始时间
        "trip_end_time":  "2018-12-01 12:00:00", // 行程结束时间
        "trip_interval":  3600, // 行程时长（秒）
        "departure":  "xxx",       // 出发地
        "destination":  "xxx",       // 目的地
        "transportation":  "xxx",       // 目的地
        "trip_type": "单程", // 单程/往返
        "remark": "备注"    // 备注
    }
    """
    trip_start_time: str
    trip_end_time: str
    trip_interval: int
    departure: str
    destination: str
    transportation: str
    trip_type: str
    remark: str


class TripApprovalEvent(EventContent):
    """出差审批

    {
         "app_id": "cli_xxx",
         "tenant_key":"xxx",
         "type":"trip_approval",
         "instance_code": "xxx", // 审批实例Code
         "employee_id": "xxx",  // 用户id
         "start_time": 1502199207, // 审批发起时间
         "end_time": 1502199307,   // 审批结束时间
         "schedules": [{         // Schedule 结构数组
                "trip_start_time": "2018-12-01 12:00:00", // 行程开始时间
                "trip_end_time":  "2018-12-01 12:00:00", // 行程结束时间
                "trip_interval":  3600, // 行程时长（秒）
                "departure":  "xxx",       // 出发地
                "destination":  "xxx",       // 目的地
                "transportation":  "xxx",       // 目的地
                "trip_type": "单程", // 单程/往返
                "remark": "备注"    // 备注
                },
         ]
         "trip_interval": 3600,    // 行程总时长（秒）
         "trip_reason": "xxx"     // 出差事由
         "trip_peers": ["xxx", "yyy"],   // 同行人
    }
    """
    app_id: str
    tenant_key: str
    type: str
    instance_code: str
    employee_id: str
    start_time: int
    end_time: int
    schedules: List[Schedule]
    trip_interval: int
    trip_reason: str
    trip_peers: List[str]


class OutApprovalEvent(EventContent):
    """外出审批事件

    {
        'app_id': 'cli_9e28cb7ba56a100e',
        'i18n_resources': [{
          'is_default': True,
          'locale': 'zh_cn',
          'texts': {
            '@i18n@someKey': '中文文案' // key对应的文案
          }
        }],
        'instance_code': '59558CEE-CEF4-45C9-A2C3-DCBF8BEC7341', // 此审批的唯一标识
        'out_image': '',
        'out_interval': 10800, // 外出时长，单位秒
        'out_name': '@i18n@someKey', // 通过i18n_resources里的信息换取相应语言的文案
        'out_reason': '外出事由',
        'out_start_time': '2020-05-15 15:00:00',
        'out_end_time': '2020-05-15 18:00:00',
        'out_unit': 'HOUR', // 外出时长的单位，HOUR 小时，DAY 天，HALF_DAY 半天
        'start_time': 1589527346, // 审批开始时间
        'end_time': 1589527354, // 审批结束时间
        'tenant_key': '2d520d3b434f175e', // 企业唯一标识
        'type': 'out_approval', // 事件类型
        'user_id': 'g6964gd3' // 申请发起人
    }
    """
    app_id: str
    i18n_resources: List[I18nResource]
    instance_code: str
    out_image: str
    out_interval: int
    out_name: str
    out_reason: str
    out_start_time: str
    out_end_time: str
    out_unit: TimeUnit
    start_time: int
    end_time: int
    tenant_key: str
    type: str
    user_id: str

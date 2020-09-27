#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""飞书应用事件

https://open.feishu.cn/document/ukTMukTMukTM/uQTNxYjL0UTM24CN1EjN
"""
from typing import List

from .base import BaseModel, EventType, AppStatus, PricePlanType, BuyType, EventContent


class Applicant(BaseModel):
    open_id: str
    user_id: str = ''


class Installer(BaseModel):
    open_id: str
    user_id: str = ''


class AppOpenEvent(EventContent):
    """首次开通应用

    {
        "app_id": "cli_xxx",  // 开通的应用ID
        "tenant_key":"xxx",   // 开通应用的企业唯一标识
        "type":"app_open",     // 事件类型
        "applicants": [ // 应用的申请者，可能有多个
            {
              "open_id":"xxx" ,  // 员工对此应用的唯一标识，同一员工对不同应用的open_id不同
              "user_id": "b78cfg77"//安装者的user_id （仅企业自建应用返回 ）
            }
        ],
        "installer": {	// 应用的安装者。如果是自动安装，则没有此字段。
        "open_id":"xxx" ,  // 员工对此应用的唯一标识，同一员工对不同应用的open_id不同
        "user_id": "b78cfg77"//安装者的user_id （仅企业自建应用返回 ）
    }
    """

    app_id: str
    tenant_key: str
    type: EventType = EventType.APP_OPEN
    applicants: List[Applicant]
    installer: Installer


class AppStatusChangeEvent(EventContent):
    """应用停启用

    {
        "app_id": "cli_xxx",  // 应用ID
        "tenant_key":"xxx",   // 企业唯一标识
        "type": "app_status_change",  // 事件类型
        "status": "start_by_tenant" //应用状态 start_by_tenant: 租户启用; stop_by_tenant: 租户停用; stop_by_platform: 平台停用
    }
    """
    app_id: str
    tenant_key: str
    type: EventType = EventType.APP_STATUS_CHANGE
    status: AppStatus


class OrderPaidEvent(EventContent):
    """应用商店应用购买

    {
        "type":"order_paid",     // 事件类型
        "app_id": "cli_9daeceab98721136", //应用ID
        "order_id": "6704894492631105539", // 用户购买付费方案时对订单ID 可作为唯一标识
        "price_plan_id": "price_9d86fa1333b8110c",  //付费方案ID
        "price_plan_type": "per_seat_per_month", // 用户购买方案类型
        "seats": 20, // 表示购买了多少人份
        "buy_count":1, //套餐购买数量 目前都为1
        "create_time": "1502199207",
        "pay_time": "1502199209",
        "buy_type": "buy", // 购买类型 buy普通购买 upgrade为升级购买 renew为续费购买
        "src_order_id": "6704894492631105539", // 当前为升级购买时(buy_type 为upgrade)，该字段表示原订单ID，升级后原订单失效，状态变为已升级(业务方需要处理)
        "order_pay_price":10000//订单支付价格 单位分，
        "tenant_key": "2f98c01bc23f6847"//购买应用的企业标示
    }
    """
    type: EventType = EventType.ORDER_PAID
    app_id: str
    order_id: str
    price_plan_id: str
    price_plan_type: str = PricePlanType.PER_SEAT_PER_MONTH
    seats: int
    buy_count: int
    create_time: str
    pay_time: str
    buy_type: BuyType
    src_order_id: str
    order_pay_price: int
    tenant_key: str


class AppTicketEvent(EventContent):
    """app_ticket事件

    对于应用商店应用，开放平台会每隔1小时推送一次 app_ticket ，应用通过该 app_ticket 获取 app_access_token。
    {
         "app_id": "cli_xxx",
         "app_ticket":"xxx",
         "type":"app_ticket"
    }
    """
    app_id: str
    app_ticket: str
    type: EventType = EventType.APP_TICKET


class AppUninstalledEvent(EventContent):
    """
    {
        "app_id": "cli_xxx", // 被卸载的应用ID
        "tenant_key": "xxx",  // 卸载应用的企业ID
        "type": "app_uninstalled"  // 事件类型
     }
    """
    app_id: str
    tenant_key: str
    type: EventType = EventType.APP_UNINSTALLED

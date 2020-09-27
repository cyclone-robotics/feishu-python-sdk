#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""飞书通讯录事件

https://open.feishu.cn/document/ukTMukTMukTM/uITNxYjLyUTM24iM1EjN
"""
from .base import BaseModel, EventType, EventContent


class UserAddEvent(EventContent):
    """员工变更

    {
         "type": "user_add",    // 事件类型，包括user_add, user_update, user_leave
         "app_id": "cli_xxx",   // 应用ID
         "tenant_key": "xxx",   // 企业标识
         "open_id":"xxx" ,  // 员工对此应用的唯一标识，同一员工对不同应用的open_id不同
         "employee_id":"xxx",    // 即“用户ID”，仅企业自建应用会返回
         "union_id": "xxx" // 用户在ISV下的唯一标识，申请了"获取用户统一ID"权限后返回
    }
    """
    type: EventType = EventType.USER_ADD
    app_id: str
    tenant_key: str
    open_id: str
    employee_id: str = ''
    union_id: str = ''


class DeptAddEvent(EventContent):
    """部门变更

    {
         "type": "dept_add",  // 事件类型，包括 dept_add, dept_update, dept_delete
         "app_id": "cli_xxx",  // 应用ID
         "tenant_key": "xxx",           // 企业标识
         "open_department_id":"od-xxx"  // 部门的Id
     }
    """
    type: EventType = EventType.DEPT_ADD
    app_id: str
    tenant_key: str
    open_department_id: str


class UserStatus(BaseModel):
    is_active: bool
    is_frozen: bool
    is_resigned: bool


class UserStatusChangeEvent(EventContent):
    """用户状态变更

    {
        "type": "user_status_change",    // 事件类型
        "app_id": "cli_xxx",   // 应用ID
        "tenant_key": "xxx",   // 企业标识
        "open_id":"xxx" ,  // 员工对此应用的唯一标识，同一员工对不同应用的open_id不同
        "employee_id":"xxx",    // 即“用户ID”，仅企业自建应用会返回
        "union_id": "xxx",  //用户统一ID，申请了"获取用户统一ID"权限后返回
        "before_status": { // 变化前的状态
            "is_active": false,        // 账号是否已激活
            "is_frozen": false,       // 账号是否冻结
            "is_resigned": false    // 是否离职
        },
        "change_time": "2020-02-21 16:28:48", // 状态更新的时间
        "current_status": { // 变化后的状态
            "is_active": true,
            "is_frozen": false,
            "is_resigned": false
        }
    }
    """
    type: EventType = EventType.USER_STATUS_CHANGE
    app_id: str
    tenant_key: str = ''
    open_id: str = ''
    employee_id: str = ''
    union_id: str = ''
    before_status: UserStatus = {}
    change_time: str = ''
    current_status: UserStatus = {}


class ContactScopeChangeEvent(EventContent):
    """授权范围变更

    {
         "type": "contact_scope_change", // 事件类型
         "app_id": "cli_xxx",   // 应用ID
         "tenant_key": "xxx", //企业标识
     }
    """
    type: EventType = EventType.CONTACT_SCOPE_CHANGE
    app_id: str
    tenant_key: str

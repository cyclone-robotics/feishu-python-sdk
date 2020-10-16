#!/usr/bin/env python
# coding: utf-8 -*-
from enum import Enum


class FeishuError(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.code},{self.msg}>"

    __unicode__ = __repr__


class ERRORS(int, Enum):
    FAILED_TO_ESTABLISH_CONNECTION = -1
    UNABLE_TO_PARSE_SERVER_RESPONSE = -2
    UNKNOWN_SERVER_ERROR = -3
    UNSUPPORTED_METHOD = -4
    INVALID_IMAGE_FILE_OR_CONTENT = -5
    VALIDATION_ERROR = -6
    MISSING_ENCRYPT_KEY = -7


class APPROVALERRORS(int, Enum):
    WRONG_REQUEST_PARAM = 60001
    APPROVAL_CODE_NOT_FOUND = 60002
    INSTANCE_CODE_NOT_FOUND = 60003
    USER_NOT_FOUND = 60004
    DEPARTMENT_VERIFICATION_FAILED = 60005
    FORM_VERIFICATION_FAILED = 60006
    SUBSCRIBE_ALREADY_EXIST = 60007
    SUBSCRIBE_NOT_EXIST = 60008
    NO_PERMISSION = 60009
    TASK_ID_NOT_FOUND = 60010
    NOT_AVAILABLE_FOR_FREE_USER = 60011
    UUID_CONFLICT_FOR_INSTANCE = 60012
    UNSUPPORTED_APPROVAL_DEFINITION = 60013

# class DOCUMENTERRORS(int, Enum):

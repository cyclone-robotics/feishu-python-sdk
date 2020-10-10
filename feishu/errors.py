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

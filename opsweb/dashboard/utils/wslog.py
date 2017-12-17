#!/usr/bin/env python

import logging
import os

def wslog_error():
    return logging.getLogger("error_logger")
def wslog_info():
    return logging.getLogger("info_logger")


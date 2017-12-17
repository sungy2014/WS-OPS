#!/usr/bin/env python

import sys
import os
import os,django

def mycrontab():
    sys.path += [os.path.dirname(os.getcwd()),os.getcwd()]
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    sys.path.append(rootPath)
    sys.path.append("/ops-data/zp/haha/mysite-11/opsweb")
    sys.path = list(set(sys.path))
    print(sys.path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opsweb.settings") # project_name 项目名称
    django.setup()

    from resources.server import ServerAliyunAutoAdd
    ServerAliyunAutoAdd()

    return "success"

if __name__ == "__main__":
    mycrontab()

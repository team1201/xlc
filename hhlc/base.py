# parseBase.py
# Author zm
# Creation 2014-09-29

import os
from enum import Enum


class ToError(Exception):
    pass


class Tobase():
    _plan, _head, _data, _rowIndex = None, None, None, None

    def __init__(self):
        self._initFuns()
        pass

    def chkDirPath(self, filePath):
        if not os.path.exists(filePath):
            upDir = os.path.dirname(filePath)
            if not os.path.isdir(upDir):
                os.makedirs(upDir)

    def _getValue(self, conf, *args):
        val = ''
        if "index" in conf:
            val = self.getDataForIndex(self._rowIndex, conf["index"])
        elif "head" in conf:
            val = self.getDataForKey(self._rowIndex, conf["head"])
        else:
            if ("format" not in conf) or \
                    (conf["format"] not in ['fmt_class', 'fmt_class2array', 'fmt_class2class']):
                val = self.getDataForKey(self._rowIndex, conf["key"])

        if "format" in conf:
            return self._callFun(conf["format"], val, conf, *args)
        else:
            return self.default(val)

    def _callFun(self, format, val, conf, *args):
        if format.find("fmt_") != 0:
            raise ToError("format key is error:" + format)
        if isinstance(format, list):
            for key in format:
                val = self.funs[Totype(key)](val, conf, *args)
        else:
            val = self.funs[Totype(format)](val, conf, *args)

        return val

    def _initFuns(self):
        __funs = {}
        __funs[Totype.fmt_str] = self.defaultStr
        __funs[Totype.fmt_int] = self.defaultInt

        self.funs = __funs
        pass

    def defaultStr(self, *args):
        return '"%s"' % str(args[0])

    def defaultInt(self, *args):
        if args[0] != 0 and not args[0]:
            return ''
        return int(args[0])

    def default(self, *args):
        val = str(args[0])          # '10.0'
        try:
            tmp = float(val)        # 10.0
            if tmp == int(tmp):     # 10.0 == 10
                return str(int(tmp))
            return val
        except ValueError:
            return self.defaultStr(val)

        # if val.isdigit():
        #     return val
        # else:
        #     return self.defaultStr(val)

    def parse(self, plan, head, data):
        self._plan = plan
        self._head = head
        self._data = data
        pass

    def getDataForIndex(self, row, cell):
        return self._data[row][cell]

    def getDataForKey(self, row, key):
        return self._data[row][self._head.index(key)]

    def getPlanKey(self, key, default=""):
        return self._plan.get(key) if (key in self._plan) else default


class Totype(Enum):
    # 共同的
    fmt_str = "fmt_str"
    fmt_int = "fmt_int"
    fmt_array = "fmt_array"
    fmt_class = "fmt_class"
    fmt_class2array = "fmt_class2array"

    # 用于csv
    fmt_class2class = "fmt_class2class"

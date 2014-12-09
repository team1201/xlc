# parseLua.py
# Author zm
# Creation 2014-09-29

import os
from zrong.base import writeByTempl
from hhlc.base import Tobase, Totype
import hhlc.dirconf as dirconf


class Tolua(Tobase):

    def __init__(self):
        super(Tolua, self).__init__()

    def _initFuns(self):
        super(Tolua, self)._initFuns()
        self.funs[Totype.fmt_class] = self.fmt_class
        self.funs[Totype.fmt_class2array] = self.fmt_class2array
        self.funs[Totype.fmt_class2array_none] = self.fmt_class2array_none

    # 导出 lua
    def parse(self, plan, head, data):
        super(Tolua, self).parse(plan, head, data)
        start, end = self._getTemplate(self.getPlanKey("template", "default"))

        tmpStr = ''
        for i in range(len(data)):
            addRow = True
            self._rowIndex = i
            __rowStr = start % self.getData(i, plan.get("major_index"))

            for conf in plan.get("columns"):
                val = self._getValue(conf)
                if str(val).strip(' "') != "":
                    __rowStr += self._tab() + \
                        conf['key'] + "=" + str(val) + ",\n"
                else:
                    if "ignore_head" in plan:
                        __head = ''
                        if "index" in conf:
                            __head = head[conf['index']]
                        elif "head" in conf:
                            __head = conf['head']
                        if __head and __head in plan.get("ignore_head"):
                            addRow = False
                            break

            __rowStr += end
            if addRow: tmpStr += __rowStr

        self._createFile(tmpStr, plan.get("true_name"))

    def fmt_class(self, val, conf, *args):
        tab = args[0] + 1 if (len(args) > 0) else 1
        # 所有值为空时是否显示该类 [2] = {...}
        showNone = conf["showNone"] if "showNone" in conf else True

        tmpStr, isNone = self._getClass(conf["data"], tab)

        if showNone or not isNone:
            return tmpStr
        else:
            return ""

    def fmt_class2array(self, val, conf, *args):
        return self._getClassArray(val, conf, *args)[0]

    def fmt_class2array_none(self, val, conf, *args):
        tmpStr, allNone = self._getClassArray(val, conf, *args)

        if not allNone:
            return tmpStr
        else:
            return ""

    def _getClassArray(self, val, conf, *args):
        tab = args[0] + 1 if (len(args) > 0) else 1
        data = conf["data"]
        # 所有值为空时是否显示该类 [2] = {...}
        showNone = conf["showNone"] if "showNone" in conf else True
        tmpStr = '{\n'

        allNone = True
        for i in range(len(data)):
            classStr, isNone = self._getClass(data[i], tab+1)
            if showNone or not isNone:
                tmpStr += self._tab(tab+1) + '[%s]=' % (i + 1)
                tmpStr += classStr + ',\n'
                allNone = False
        tmpStr += self._tab(tab) + '}'

        return tmpStr, allNone

    def _getClass(self, data, tab):
        tmpStr = '{\n'
        isNone = True
        for d in data:
            val = self._getValue(d, tab)
            if str(val).strip(' "') != "":
                tmpStr += self._tab(tab + 1) + \
                    d['key'] + "=" + str(val) + ",\n"
                isNone = False
        tmpStr += self._tab(tab) + '}'
        return tmpStr, isNone

    def _tab(self, tab=1):
        return " " * (tab * 4)

    def _getTemplate(self, template):
        if template == "default":
            return 'data[%s]={\n', '}\n\n'
        elif template == "array":
            return '[%s]={\n', '},\n\n'
        pass

    def getData(self, row, cell):
        val = self.getDataForIndex(row, cell)
        return self._parseValueForLua(val)

    def _parseValueForLua(self, val):
        if val == 0:
            val = int(val)
        if isinstance(val, str):
            val = val.replace(u'，', u',').replace(
                u'：', u':').replace(u'；', u';')
        else:
            val = round(val, 3)
            val = val - int(val) != 0 and val or int(val)
        return val

    def _createFile(self, str, true_name):
        lua_dict = {"XLSDATA": str}
        filePath = os.path.join(
            dirconf.lua_path, true_name + '.lua')

        self.chkDirPath(filePath)

        writeByTempl(
            os.path.join(dirconf.temp_path, "%s.lua" %
                         self.getPlanKey("template", "default")),
            filePath,
            lua_dict
        )

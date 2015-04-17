# parser.py
# Author zm
# Creation 2014-09-26

import os
import xlrd
from zrong.base import (read_file)
from xlc.tocsv import Tocsv
from xlc.tolua import Tolua
import xlc.dirconf as dirconf


class ParseError(Exception):
    pass


class Parser():

    def __init__(self, ptype):
        self.csv = Tocsv()
        self.lua = Tolua()
        self.ptype = ptype
        pass

    def sheetCheck(self, sheet):
        if "sheets" not in sheet:
            raise ParseError("not sheets key")
        if "xls" not in sheet:
            raise ParseError("not xls key")
        return sheet

    # 解析模块, 并执行计划
    def parseModules(self, files):
        for path in files:
            print("parse file: " + os.path.basename(path))

            self.module = self.sheetCheck(eval(read_file(path)))

            for sheet in self.module.get("sheets"):
                self.parseSheet(sheet)

        print("parse complete")

    def parseSheet(self, sheet):
        plans = sheet.get("plan")
        for plan in plans:
            if plan not in self.module:
                raise ParseError("not " + plan + " key")
            self.parsePlan(sheet, self.module.get(plan))

    def parsePlan(self, sheet, plan):
        __original = self.readXls(sheet)
        # print(__original)

        if "headLine" in sheet:
            __headLine = int(sheet.get("headLine"))
        else:
            __headLine = 0

        if "dataLine" in sheet:
            __dataLine = int(sheet.get("dataLine"))
        else:
            __dataLine = 1

        __head = __original[__headLine]
        __data = [__original[i] for i in range(__dataLine, len(__original))]

        # print(__head)
        # print()
        # print(__data)

        if self.canParse(plan.get("export"), "csv"):
            self.csv.parse(plan, __head, __data)
        elif self.canParse(plan.get("export"), "lua"):
            self.lua.parse(plan, __head, __data)

    def canParse(self, export, ptype):
        if (self.ptype == "all" and export == ptype) or (self.ptype == export == ptype):
            return True
        return False

    def readXls(self, sheet):
        __path = os.path.join(dirconf.xls_path, self.module.get("xls"))
        if not os.path.exists(__path):
            raise ParseError(__path + " not find")

        __original = xlrd.open_workbook(__path)
        if sheet.get("sheet_index"):
            # 通过索引顺序获取
            __table = __original.sheet_by_index(int(sheet.get("sheet_index")))
        elif sheet.get("sheet_name"):
            # 通过表名获取
            __table = __original.sheet_by_name(sheet.get("sheet_name"))
        else:
            # 默认取第一张表
            __table = __original.sheet_by_index(0)

        nrows = __table.nrows
        # ncols = __table.ncols

        __data = [__table.row_values(i) for i in range(nrows)]

        return __data

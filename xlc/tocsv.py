# parseCsv.py
# Author zm
# Creation 2014-09-29

import os
import csv
from hhlc.base import Tobase, Totype
import hhlc.dirconf as dirconf


class Tocsv(Tobase):

    def __init__(self):
        super(Tocsv, self).__init__()

    def _initFuns(self):
        super(Tocsv, self)._initFuns()
        self.funs[Totype.fmt_class] = self.fmt_class
        self.funs[Totype.fmt_class2array] = self.fmt_class2array
        self.funs[Totype.fmt_class2class] = self.fmt_class2class

    # 导出 csv
    def parse(self, plan, head, data):
        super(Tocsv, self).parse(plan, head, data)
        filePath = os.path.join(
            dirconf.csv_path, plan.get("true_name") + '.csv')

        self.chkDirPath(filePath)

        csvfile = open(filePath, 'w', newline='')
        writer = csv.writer(csvfile)

        # head
        writer.writerow([conf['key'] for conf in plan.get("columns")])

        # body
        for i in range(len(data)):
            addRow = True
            self._rowIndex = i
            __row = []

            for conf in plan.get("columns"):
                val = self._getValue(conf)
                __row.append(val)
                if str(val).strip(' "') == "":
                    if "ignore_head" in plan:
                        __head = ''
                        if "index" in conf:
                            __head = head[conf['index']]
                        elif "head" in conf:
                            __head = conf['head']
                        if __head and __head in plan.get("ignore_head"):
                            addRow = False
                            break

            if addRow: writer.writerow(__row)

        csvfile.close()

    def fmt_class(self, val, conf):
        return self._getClass(conf["data"], ":")

    def fmt_class2array(self, val, conf):
        data = conf["data"]
        tmpStr = ''

        for i in range(len(data)):
            tmpStr += self._getClass(data[i], ":") + "|"

        return tmpStr[:-1]

    def fmt_class2class(self, val, conf):
        return self._getClass(conf["data"], "|")

    def _getClass(self, data, split):
        tmpStr = ''
        for d in data:
            val = self._getValue(d)
            tmpStr += str(val) + split

        return tmpStr[:-1]

    def defaultStr(self, *args):
        return args[0]

    # def getData(self, row, cell):
    #     val = super(Tocsv, self).getDataForIndex(row, cell)
    #     return self._parseValueForCsv(val)

    def _parseValueForCsv(self, val):
        if val == 0:
            val = int(val)
        if isinstance(val, str):
            val = val.replace(',', u'，')
            # .replace(':', u'：').replace(';', u'；').replace("'", u'’')
        else:
            val = val - int(val) != 0 and val or int(val)
        return val

# parser.py
# Author zm
# Creation 2014-09-26

import os
from zrong.base import getFiles
from hhlc.conf import Parser, ParseError
import hhlc.dirconf as dirconf


# 排除非模块文件
def excludeFiles(path):
    __fname = os.path.basename(path)
    for exclude in ["__init__.py"]:
        if exclude == __fname:
            return False
    return True


# 获取指定文件
def get_theModule(files, fnames):
    def is_theFile(path):
        __fname = os.path.basename(path).replace('.py','')
        if __fname in fnames:
            return True
        return False

    return filter(is_theFile, files)


def call(xls, export, tmpl, command=[], ptype="all"):
    if not os.path.exists(xls):
        raise ParseError("xls directory is not exists:" + xls)
    if not os.path.exists(export):
        raise ParseError("export directory is not exists:" + export)
    if not os.path.exists(tmpl):
        raise ParseError("tmpl directory is not exists:" + tmpl)

    dirconf.updateXlsPath(xls)
    dirconf.updateTempPath(tmpl)

    if ptype == "all":
        dirconf.updateExportPath(export)
    elif ptype == "lua":
        dirconf.updateLuaPath(export)
    elif ptype == "csv":
        dirconf.updateCsvPath(export)
        
    files = filter(excludeFiles, getFiles(dirconf.xls_path, ["py"]))

    if isinstance(command, list) and len(command) != 0:
        files = get_theModule(files, command) # + ".py"

    parser = Parser(ptype)
    parser.parseModules(files)


def callDt(xls, export, tmpl, command, ptype):
    call(xls, export, tmpl, command, ptype)

def callEtc(heroPath, sszPath, exportPath):
    import hhlc.etc as etc
    # import etc
    etc.call(heroPath, sszPath, exportPath)

if __name__ == '__main__':
    callDt(
        "D:\\works\\hhl\\projects\\config\\xls", 
        "D:\\works\\hhl\\projects\\client\\src\\conf", 
        "D:\\works\\hhl\\projects\\config\\templates",
        ["skill"],
        "lua")

    # callEtc(
    #     "D:\\works\\hhl\\projects\\resource\\art",
    #     "D:\\works\\hhl\\projects\\resource\\art\\ssz",
    #     "D:\\works\\hhl\\projects\\resource\\skill"
    # )


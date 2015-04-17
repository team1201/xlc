# parser.py
# Author zm
# Creation 2014-09-26

import os


file_dir = os.path.split(os.path.abspath(__file__))[0]
work_dir = os.path.dirname(file_dir)

xls_path = os.path.join(work_dir, "xls")
temp_path = os.path.join(work_dir, "templates")
export_path = os.path.join(work_dir, "export")
csv_path = os.path.join(export_path, "csv")
lua_path = os.path.join(export_path, "lua")


def updateXlsPath(path):
    global xls_path
    xls_path = path

def updateTempPath(path):
    global temp_path
    temp_path = path

def updateExportPath(path):
    global csv_path, lua_path
    export_path = path
    csv_path = os.path.join(export_path, "csv")
    lua_path = os.path.join(export_path, "lua")


def updateCsvPath(path):
    global csv_path
    csv_path = path


def updateLuaPath(path):
    global lua_path
    lua_path = path

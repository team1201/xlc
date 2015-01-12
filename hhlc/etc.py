# -*- coding: utf-8 -*-
# etc.py
# etc = effect tool convertor
# Author zm
# Creation 2014-09-26
# Modification zrong 2015-01-09

import re
import os
import json
from zrong.base import (write_file, read_file, get_files, slog)


class Parser():

    def __init__(self, export):
        self.export = export
        self.file_dir = os.getcwd()

    def parseConf(self, obj, fileName):
        start = '["%s"]={\n'
        end = '}\n\n'
        tmpStr = ''

        for key in obj.keys():
            # print(key)
            tmpStr += start % key
            tmpStr += str(obj[key]).replace("[", "{").replace("]", "}")
            tmpStr += end

        self.saveFile(tmpStr, fileName)

    def parseHero(self, files):
        tmpStr = ''

        for path in files:
            heroId = os.path.basename(path).split('.')[0]
            obj = json.loads(read_file(path))
            tmpStr += self._parseHero(obj, heroId)

        self.saveFile(tmpStr, "etc")

    def _parseHero(self, obj, heroId):
        start = '[%s]={\n'
        end = '}\n\n'
        tmpStr = ''

        for key in obj["skill"].keys():
            id = self._parseSkillKey(key, heroId)
            tmpStr += self._tab(1) + start % id
            if type(obj["skill"][key]) != str:
                tmpStr += self.parseHeroClass(id, obj["skill"][key])
            else:
                tmpStr += self.getSkill(2, id, *obj["skill"][key].split(','))
            tmpStr += self._tab(1) + end

        return tmpStr

    def _parseSkillKey(self, key, heroId):
        if key == "skill1":
            return heroId + "11"
        elif key == "skill2":
            return heroId + "12"
        elif key == "skill3":
            return heroId + "13"
        elif key == "skill4":
            return heroId + "21"

        return "null"

    def parseHeroClass(self, key, obj):
        return self.getSkill(2, key, obj["effects_b_ready"], obj["effects_b"], obj["effects_f_ready"], obj["effects_f"], obj["t_sex"], obj["t_syb"], obj["t_sb"], obj["ce_b_ready"], obj["ce_b_no"], obj["ce_f_ready"], obj["ce_f_no"], obj["t_syx"], obj["t_sd"], obj["zoom"], obj["zoom_no"], obj["shake"], obj["shake_no"], obj["shine1"], obj["shine1_no"], obj["shine2"], obj["shine2_no"])

    def getSkill(self, tab, id, *args):
        _tab = self._tab(tab)
        # print(len(args))
        return _tab + 'id=' + id + ',\n' + \
            _tab + 'effects_b_ready=' + self.getValue(args[0]) + ',\n' + \
            _tab + 'effects_b=' + self.getValue(args[1]) + ',\n' + \
            _tab + 'effects_f_ready=' + self.getValue(args[2]) + ',\n' + \
            _tab + 'effects_f=' + self.getValue(args[3]) + ',\n' + \
            _tab + 't_sex=' + self.getValue(args[4]) + ',\n' + \
            _tab + 't_syb=' + self.getValue(args[5]) + ',\n' + \
            _tab + 't_sb=' + self.getValue(args[6]) + ',\n' + \
            _tab + 'ce_b_ready=' + self.getValue(args[7]) + ',\n' + \
            _tab + 'ce_b_no=' + self.getValue(args[8]) + ',\n' + \
            _tab + 'e_f_ready=' + self.getValue(args[9]) + ',\n' + \
            _tab + 'ce_f_no=' + self.getValue(args[10]) + ',\n' + \
            _tab + 't_syx=' + self.getValue(args[11]) + ',\n' + \
            _tab + 't_sd=' + self.getValue(args[12]) + ',\n' + \
            _tab + 'zoom=' + self.getValue(args[13]) + ',\n' + \
            _tab + 'zoom_no=' + self.getValue(args[14]) + ',\n' + \
            _tab + 'shake=' + self.getValue(args[15]) + ',\n' + \
            _tab + 'shake_no=' + self.getValue(args[16]) + ',\n' + \
            _tab + 'shine1=' + self.getValue(args[17]) + ',\n' + \
            _tab + 'shine1_no=' + self.getValue(args[18]) + ',\n' + \
            _tab + 'shine2=' + self.getValue(args[19]) + ',\n' + \
            _tab + 'shine2_no=' + self.getValue(args[20]) + '\n'

    def getValue(self, val):
        val = str(val)          # '10.0'
        try:
            tmp = float(val)        # 10.0
            if tmp == int(tmp):     # 10.0 == 10
                return str(int(tmp))
            return val
        except ValueError:
            return '"%s"' % str(val)

    def _tab(self, tab=1):
        return " " * (tab * 4)

    def saveFile(self, data, fileName):
        # save path
        filePath = os.path.join(
            self.export, fileName + '.lua')

        # check path
        self.chkDirPath(filePath)

        write_file(filePath, 'local data={\n' + data + '\n}\nreturn data')

    def chkDirPath(self, filePath):
        if not os.path.exists(filePath):
            upDir = os.path.dirname(filePath)
            if not os.path.isdir(upDir):
                os.makedirs(upDir)


# 排除非1010类文件
def herosFiles(path):
    __fname = os.path.basename(path).split('.')[0]
    try:
        tmp = int(__fname)
        return True
    except ValueError:
        return False


# 排除1010类文件
def confFiles(path):
    __fname = os.path.basename(path)
    try:
        tmp = int(__fname.split('.')[0])
        return False
    except ValueError:
        for exclude in ["play.json", "conf.json"]:
            if exclude == __fname:
                return False
        return True


# 获取play.json
def playFiles(path):
    __fname = os.path.basename(path)
    for exclude in ["play.json"]:
        if exclude == __fname:
            return True
    return False


def call(heroPath, sszPath, exportPath):
    parser = Parser(exportPath)

    # parse heros
    files = filter(herosFiles, get_files(heroPath, ["json"]))
    slog.info("parse: etc.json")
    parser.parseHero(files)

    # parse ssz
    files = filter(confFiles, get_files(sszPath, ["json"]))
    for path in files:
        slog.info("parse: %s", os.path.basename(path))
        jsontxt = read_file(path)
        jsontxt = re.sub(r'^\/\/.*$', '', jsontxt, flags=re.M)
        obj = json.loads(jsontxt)
        parser.parseConf(obj, os.path.basename(path).split('.')[0])

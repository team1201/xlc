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
        start = '["%s"]=\n'
        end = '\n\n'
        tmpStr = ''

        for key in obj.keys():
            # print(key)
            tmpStr += start % key
            tmpStr += str(obj[key]).replace("[", "{").replace("]", "}") + ","
            tmpStr += end

        self.saveFile(tmpStr, fileName)

    def parseHero(self, files):
        tmpStr = ''

        for path in files:
            heroId = os.path.basename(path).split('.')[0]
            print("parse ect:", heroId)
            jsontxt = read_file(path)
            # replace //
            jsontxt = re.sub(r'\/\/.*$', '', jsontxt, flags=re.M)
            # replace /**/
            jsontxt = re.sub(r'\/\*[\w\W]*?\*\/', '', jsontxt, flags=re.M)
            # print(jsontxt)
            obj = json.loads(jsontxt)
            tmpStr += self._parseHero(obj, heroId)

        self.saveFile(tmpStr, "etc")

    def _parseHero(self, obj, heroId):
        self._jsonData = obj
        start = '[%s]={\n'
        end = '},\n\n'
        tmpStr = ''

        hasEnemy = "enemy_action" in obj

        if "hero_action" in obj:
            for key in obj["hero_action"].keys():
                if key in ["attack", "skill1","skill2","skill3","skill4"]:
                    id = self._parseSkillKey(key, heroId)
                    tmpStr += self._tab(1) + start % id
                    tmpStr += self.getSkill(2, id, obj["hero_action"][key])
                    if hasEnemy and key in obj["enemy_action"]:
                        tmpStr += self._parseEnemy_action(2, obj["enemy_action"][key])
                    else:
                        tmpStr += '\n'
                    tmpStr += self._tab(1) + end

        return tmpStr

    def _parseSkillKey(self, key, heroId):
        if key == "attack":
            return heroId + "00"
        if key == "skill1":
            return heroId + "11"
        elif key == "skill2":
            return heroId + "12"
        elif key == "skill3":
            return heroId + "13"
        elif key == "skill4":
            return heroId + "21"

        return "null"

    def getSkill(self, tab, id, obj):
        _tab = self._tab(tab)
        # print(len(args))
        return _tab + 'id=' + id + ',\n' + \
            _tab + 'effects_b=' + self.getValue(obj["effects_b"]) + ',\n' + \
            _tab + 'effects_b_no=' + self.getTable(obj["effects_b_no"]) + ',\n' + \
            _tab + 'effects_f=' + self.getValue(obj["effects_f"]) + ',\n' + \
            _tab + 'effects_f_no=' + self.getTable(obj["effects_f_no"]) + ',\n' + \
            _tab + 't_sex=' + self.getValue(obj["t_sex"]) + ',\n' + \
            _tab + 't_syb=' + self.getValue(obj["t_syb"]) + ',\n' + \
            _tab + 't_sb=' + self.getValue(obj["t_sb"]) + ',\n' + \
            _tab + 'ce_b=' + self.getValue(obj["ce_b"]) + ',\n' + \
            _tab + 'ce_b_no=' + self.getValue(obj["ce_b_no"]) + ',\n' + \
            _tab + 'ce_f=' + self.getValue(obj["ce_f"]) + ',\n' + \
            _tab + 'ce_f_no=' + self.getValue(obj["ce_f_no"]) + ',\n' + \
            _tab + 't_syx=' + self.getValue(obj["t_syx"]) + ',\n' + \
            _tab + 't_sd=' + self.getValue(obj["t_sd"]) + ',\n' + \
            _tab + 'zoom=' + self.getValue(obj["zoom"]) + ',\n' + \
            _tab + 'zoom_no=' + self.getValue(obj["zoom_no"]) + ',\n' + \
            _tab + 'shake=' + self.getValue(obj["shake"]) + ',\n' + \
            _tab + 'shake_no=' + self.getValue(obj["shake_no"]) + ',\n' + \
            _tab + 'shine1=' + self.getValue(obj["shine1"]) + ',\n' + \
            _tab + 'shine1_no=' + self.getValue(obj["shine1_no"]) + ',\n' + \
            _tab + 'shine2=' + self.getValue(obj["shine2"]) + ',\n' + \
            _tab + 'shine2_no=' + self.getValue(obj["shine2_no"])

    def _parseEnemy_action(self, tab, obj):
        _tab = self._tab(tab)
        return  ',\n' + \
            _tab + 'e_effects_no=' + self.getValue(obj["e_effects_no"]) + ',\n' + \
            _tab + 'e_shine1=' + self.getValue(obj["e_shine1"]) + ',\n' + \
            _tab + 'e_shine1_no=' + self.getValue(obj["e_shine1_no"]) + ',\n' + \
            _tab + 'e_shine2=' + self.getValue(obj["e_shine2"]) + ',\n' + \
            _tab + 'e_shine2_no=' + self.getValue(obj["e_shine2_no"]) + ',\n' + \
            _tab + 'e_desc=' + self.getValue(obj["e_desc"]) + ',\n' + \
            _tab + 'e_desc_no=' + self.getValue(obj["e_desc_no"]) + ',\n' + \
            _tab + 'e_icon=' + self.getValue(obj["e_icon"]) + ',\n' + \
            _tab + 'e_icon_no=' + self.getValue(obj["e_icon_no"]) + ',\n' + \
            _tab + 'e_effects_b=' + self.getValue(obj["e_effects_b"]) + ',\n' + \
            _tab + 'e_effects_b_no=' + self.getValue(obj["e_effects_b_no"]) + ',\n' + \
            _tab + 'e_effects_f=' + self.getValue(obj["e_effects_f"]) + ',\n' + \
            _tab + 'e_effects_f_no=' + self.getValue(obj["e_effects_f_no"]) + ',\n' + \
            _tab + 'e_arm=' + self.getValue(obj["e_arm"]) + ',\n' + \
            _tab + 'e_arm_no=' + self.getValue(obj["e_arm_no"]) + ',\n' + \
            _tab + 'e_label=' + self.getValue(obj["e_label"]) + '\n'

    def getValue(self, val):
        val = str(val)          # '10.0'
        try:
            tmp = float(val)        # 10.0
            if tmp == int(tmp):     # 10.0 == 10
                return str(int(tmp))
            return val
        except ValueError:
            return '"%s"' % str(val)

    def getTable(self, val):
        val = str(val)
        return val.replace("[", "{").replace("]", "}")

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
        if tmp != 0:
            return True
        return False
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
        jsontxt = re.sub(r'\/\/.*$', '', jsontxt, flags=re.M)
        obj = json.loads(jsontxt)
        parser.parseConf(obj, os.path.basename(path).split('.')[0])

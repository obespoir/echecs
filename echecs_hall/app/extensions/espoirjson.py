# coding=utf-8

import json
import re

"""
新品配置解析器, 可以解析带注释的 json 文件
"""


class TrimNote(object):
    """
    创建一个TrimNote类，用于处理从文件中读出的字符串
    """
    def __init__(self, instr):
        self.instr = instr

    # 删除“//”标志后的注释
    def rmCmt(self):
        qtCnt = cmtPos = slashPos = 0
        rearLine = self.instr
        # rearline: 前一个“//”之后的字符串，
        # 双引号里的“//”不是注释标志，所以遇到这种情况，仍需继续查找后续的“//”
        while rearLine.find('//') >= 0: # 查找“//”
            slashPos = rearLine.find('//')
            cmtPos += slashPos
            # print 'slashPos: ' + str(slashPos)
            headLine = rearLine[:slashPos]
            while headLine.find('"') >= 0: # 查找“//”前的双引号
                qtPos = headLine.find('"')
                if not self.isEscapeOpr(headLine[:qtPos]): # 如果双引号没有被转义
                    qtCnt += 1 # 双引号的数量加1
                headLine = headLine[qtPos+1:]
                # print qtCnt
            if qtCnt % 2 == 0: # 如果双引号的数量为偶数，则说明“//”是注释标志
                # print self.instr[:cmtPos]
                return self.instr[:cmtPos]
            rearLine = rearLine[slashPos+2:]
            # print rearLine
            cmtPos += 2
        # print self.instr
        return self.instr

    # 判断是否为转义字符
    def isEscapeOpr(self, instr):
        if len(instr) <= 0:
            return False
        cnt = 0
        while instr[-1] == '\\':
            cnt += 1
            instr = instr[:-1]
        if cnt % 2 == 1:
            return True
        else:
            return False


class EspoirJson(object):
    """
    解析带有//注释的json文件
    """
    @classmethod
    def loads(cls, json_path):
        try:
            srcJson = open(json_path, 'r')
        except Exception:
            print('cannot open ' + json_path)
            quit()

        dstJsonStr = ''
        for line in srcJson.readlines():
            if not re.match(r'\s*//', line) and not re.match(r'\s*\n', line):
                xline = TrimNote(line)
                dstJsonStr += xline.rmCmt()

        dstJson = {}
        try:
            dstJson = json.loads(dstJsonStr)
            return dstJson
        except:
            print(json_path + ' is not a valid json file')
            quit()


if __name__ == "__main__":
    print(EspoirJson.loads("config2.json"))
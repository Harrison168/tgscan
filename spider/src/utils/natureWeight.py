#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Nature权重，保持与Java中的一致
NATURE_WEIGHT_PKU = {
    "a": 0.8, "ad": 0.7, "ag": 0.6, "al": 0.7, "an": 0.8, "b": 0.6, "bg": 0.5, "bl": 0.6,
    "c": 0.3, "cc": 0.4, "d": 0.5, "dg": 0.4, "dl": 0.4, "e": 0.4, "f": 0.6, "g": 0.8,
    "gb": 0.9, "gbc": 0.9, "gc": 0.9, "gm": 0.9, "gp": 0.9, "h": 0.3, "i": 0.7, "j": 1.0,
    "k": 0.3, "l": 0.7, "m": 0.8, "mg": 0.8, "mq": 0.8, "n": 1.0, "nb": 0.9, "nba": 0.9,
    "nbc": 0.9, "nbp": 0.9, "nf": 0.8, "ng": 0.6, "nh": 0.9, "nhd": 0.9, "nhm": 0.9,
    "ni": 0.7, "nic": 0.8, "nis": 0.7, "nit": 0.8, "nl": 0.7, "nm": 0.8, "nmc": 0.9,
    "nn": 0.8, "nnd": 0.8, "nnt": 0.8, "ns": 1.0, "nsf": 1.0, "nt": 1.0, "nth": 1.0,
    "ntcb": 1.0, "ntcf": 1.0, "ntch": 1.0, "ntc": 1.0, "nx": 1.0, "nz": 0.8, "o": 0.4,
    "p": 0.3, "q": 0.6, "r": 0.4, "rr": 0.4, "rz": 0.4, "s": 0.5, "t": 0.6, "tg": 0.6,
    "u": 0.2, "ud": 0.2, "ug": 0.2, "uj": 0.2, "ul": 0.2, "uv": 0.2, "uz": 0.2,
    "v": 0.7, "vd": 0.6, "vg": 0.6, "vi": 0.6, "vn": 0.7, "vq": 0.7, "w": 0.0, "x": 0.1,
    "y": 0.4, "z": 0.3,
}

# 定义 PTB 词性权重字典
NATURE_WEIGHT_PTB = {
    # CC 并列连接词
    "CC": 0.4,
    # CD 基数
    "CD": 0.8,
    # DT 限定词
    "DT": 0.5,
    # EX 存在型 there
    "EX": 0.5,
    # FW 外文单词
    "FW": 0.8,
    # IN 介词/从属连接词
    "IN": 0.4,
    # JJ 形容词
    "JJ": 0.8,
    # JJR 形容词，比较级
    "JJR": 0.9,
    # JJS 形容词，最高级
    "JJS": 1.0,
    # LS 列表项标记
    "LS": 0.3,
    # MD 情态动词
    "MD": 0.5,
    # NN 名词，可数或不可数
    "NN": 1.0,
    # NNS 名词，复数
    "NNS": 1.0,
    # NNP 专有名词，单数
    "NNP": 1.0,
    # NNPS 专有名词，复数
    "NNPS": 1.0,
    # PDT 前位限定词
    "PDT": 0.6,
    # POS 所有格结束词
    "POS": 0.5,
    # PRP 人称代名词
    "PRP": 0.5,
    # PRP$ 物主代词，所有格代名词
    "PRP$": 0.6,
    # RB 副词
    "RB": 0.5,
    # RBR 副词，比较级
    "RBR": 0.6,
    # RBS 副词，最高级
    "RBS": 0.7,
    # RP 小品词
    "RP": 0.4,
    # SYM 符号（数学或科学）
    "SYM": 0.4,
    # TO "to"
    "TO": 0.3,
    # UH 感叹词
    "UH": 0.4,
    # VB 动词，基本形态
    "VB": 0.8,
    # VBD 动词，过去式
    "VBD": 0.8,
    # VBG 动词，动名词/现在分词
    "VBG": 0.8,
    # VBN 动词，过去分词
    "VBN": 0.8,
    # VBP 动词，非第三人称单数现在式
    "VBP": 0.8,
    # VBZ 动词，第三人称单数现在式
    "VBZ": 0.8,
    # WDT wh-限定词
    "WDT": 0.6,
    # WP wh-代词
    "WP": 0.6,
    # WP$ 所有格 wh-代词
    "WP$": 0.7,
    # WRB wh-副词
    "WRB": 0.6,
    # PU 标点符号
    "PU": 0.1,
}
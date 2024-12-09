#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import re
import fasttext
import hanlp
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict


from spider.src.utils import natureWeight
from spider.src.utils.common import root_dir


class HanlpUtil:



    def __init__(self):
        # 加载分词和词性标注模型
        self.segmenter = hanlp.load(hanlp.pretrained.tok.UD_TOK_MMINILMV2L12)  # 分词模型
        self.segmenter_zh = hanlp.load(hanlp.pretrained.tok.CTB9_TOK_ELECTRA_BASE)  # 分词模型
        self.pos_tagger = hanlp.load(hanlp.pretrained.pos.PTB_POS_RNN_FASTTEXT_EN)  # 词性标注模型
        self.pos_tagger_zh = hanlp.load(hanlp.pretrained.pos.PKU_POS_ELECTRA_SMALL)  # 词性标注模型


    # 分词并计算权重
    def extract_keywords_with_pos(self, text, language_code="en", top_k=10):
        # 分词和词性标注结果
        if language_code == "zh":
            words = self.segmenter_zh(text)  # 分词结果
            tokens_with_pos = self.pos_tagger_zh(words)  # 词性标注结果
            nature_weight = natureWeight.NATURE_WEIGHT_PKU
        else:
            words = self.segmenter(text)  # 分词结果
            tokens_with_pos = self.pos_tagger(words)  # 词性标注结果
            nature_weight = natureWeight.NATURE_WEIGHT_PTB

        # words = self.segmenter_zh(text)  # 分词结果
        # tokens_with_pos = self.pos_tagger_zh(words)  # 词性标注结果
        # nature_weight = natureWeight.NATURE_WEIGHT_PKU

        # print("分词结果:", words)
        # print("词性标注结果:", tokens_with_pos)

        # 去除标点符号和空格
        words_filtered = [word for word in words if re.match(r'\w+', word)]  # 只保留字母、数字和汉字
        tokens_with_pos_filtered = [nature for word, nature in zip(words, tokens_with_pos) if re.match(r'\w+', word)]

        # 去除重复词
        seen_words = set()
        filtered_words = []
        filtered_tokens_with_pos = []
        for word, nature in zip(words_filtered, tokens_with_pos_filtered):
            if word not in seen_words:
                seen_words.add(word)
                filtered_words.append(word)
                filtered_tokens_with_pos.append(nature)

        # 计算词权重
        word_weights = []
        for word, nature in zip(filtered_words, filtered_tokens_with_pos):
            weight = nature_weight.get(nature, 0.1)  # 默认权重为 0.1
            word_weights.append((word, weight))

        # 根据权重排序并提取关键词
        sorted_keywords = sorted(word_weights, key=lambda x: x[1], reverse=True)
        keywords = [kw for kw, _ in sorted_keywords[:top_k]]

        return keywords, list(zip(filtered_words, filtered_tokens_with_pos))

    # def dataDir():
    #     data_dir = root_dir / f"data"
    #     if not os.path.exists(data_dir):
    #         os.mkdir(data_dir)
    #     return data_dir


if __name__ == '__main__':
    hanlpUtil = HanlpUtil()

    text = f"Telegram 中文社群, Telegram 中文/汉化/知识/教程, 科技, 机场, 科学上网...... 自由是有规则的，没规则的自由是混乱。 禁言是机器人干的，退群重新加入即可。 群规: * 禁止传播谣言/盗版 * 禁止撕逼/谩骂/人身攻击/血腥/暴力 * 禁止讨论免流/黄赌毒/宗教/政治/键政 * 禁止广告/推广/黑产/灰产/暗网/刷屏/色情/开车/NSFW * 仅限聊中文话题 👥Telegram 二十万人 @tgcnx 👥Telegram 中文二群 @tgzhcn 📢Telegram 中文频道 @tgcnz"
    text_en = f"Coinlist ( 香港-硬币清单） - 𝙾𝚃𝙲 𝙼𝙰𝚁𝙺𝙴𝚃 , 𝚄𝙿𝙷𝙾𝙻𝙳 , 𝙱𝙸𝙽𝙰𝙽𝙲𝙴 , 𝙷𝚄𝙾𝙱𝙸 , 𝙰𝙽𝙳 𝙾𝚃𝙷𝙴𝚁𝚂💲🔥"
    text_en2 = f"SHARE FREE AIRDROP - ARBITRUM BSC LOW TAX - SHILL HIDDEN GEM"
    # tokens = tokenizer(text)
    # print(tokens)

    # 手动实现 TF-IDF 提取关键词（需要自己构建词频和逆文档频率矩阵）
    # vectorizer = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
    # tfidf_matrix = vectorizer.fit_transform([tokens])
    # feature_names = vectorizer.get_feature_names_out()
    # scores = tfidf_matrix.toarray()[0]
    # # 获取得分最高的词
    # top_keywords = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)[:10]
    # print("Top Keywords:", top_keywords)

    # 提取关键词
    keywords, pos_tags = hanlpUtil.extract_keywords_with_pos(text_en, language_code="en", top_k=10)
    print("关键词：", keywords)
    print("词性标注：", pos_tags)
    keywords, pos_tags = hanlpUtil.extract_keywords_with_pos(text_en2, language_code="en", top_k=10)
    print("关键词：", keywords)
    print("词性标注：", pos_tags)


    # 定义多功能分词器
    # pipeline = hanlp.pipeline() \
    #     .append(hanlp.utils.rules.split_sentence, output_key='sentences') \
    #     .append(segmenter, output_key='tokens') \
    #     .append(pos_tagger, output_key='part_of_speech_tags')
    # output = pipeline(text_en)
    # print(output)


    # model = fasttext.load_model('lid.176.bin')
    # prediction = model.predict(text)
    # language = prediction[0][0].split('__')[-1]
    # print(f"The detected language is: {language}")















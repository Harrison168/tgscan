package xyz.tgscan.utils;

import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.common.Term;
import lombok.extern.slf4j.Slf4j;

import java.util.List;

@Slf4j
public class HanLPUtil {

    public static List<String> generateTags(String content) {
        return HanLP.extractKeyword(content, 5); // 提取前 5 个关键词
    }

    /**
     * 获取词与词性
     * @param content
     */
    public static List<Term> recognizeEntities(String content) {
        List<Term> terms = HanLP.segment(content);
//        for (Term term : terms) {
//            System.out.println(term.word + " - " + term.nature); // 打印词与词性
//        }

        return terms;
    }

    public static void main(String[] args) {
//        String text = "这个频道是关于人工智能技术和编程的讨论。";
        String text = "Du Rove's Channel, Thoughts from the CEO of Telegram";
        List<String> tags = generateTags(text);
        System.out.println(tags);

//        String text1 = "这是一个关于Python编程语言的技术频道。";
        String text1 = "Du Rove's Channel, Thoughts from the CEO of Telegram";
        recognizeEntities(text1);
    }
}

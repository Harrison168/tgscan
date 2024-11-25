package xyz.tgscan.utils;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class UrlUtils {

    public static String getTGIdByUrl(String url) {
        String pattern = ".*/([^/?]+)$"; // 匹配最后一部分的字符串
        Pattern regex = Pattern.compile(pattern);
        Matcher matcher = regex.matcher(url);

        if (matcher.find()) {
            return matcher.group(1); // 返回匹配的 ID 部分
        }
        return null;
    }

    public static void main(String[] args) {
        System.out.println(UrlUtils.getTGIdByUrl("https://t.me/+1hd33CRoEfBjNzE8"));
    }
}

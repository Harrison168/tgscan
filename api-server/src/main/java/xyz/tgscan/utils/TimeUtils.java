package xyz.tgscan.utils;

import java.time.*;
import java.time.format.DateTimeFormatter;

public class TimeUtils {

    public static final String FORMAT_YYYYMMDD = "yyyyMMdd";
    public static final String FORMAT_dd_MM_yyyy = "dd-MM-yyyy";


    public static Instant getMonthStartTime(){
        LocalDateTime now = LocalDateTime.now();
        Month month = now.getMonth();
        int year = now.getYear();
        LocalDateTime monthStartTime = LocalDateTime.of(year, month, 1, 0 , 0, 0);
        Instant monthStartIns = monthStartTime.toInstant(ZoneOffset.of("+0"));
        return monthStartIns;
    }

    /**
     * 获取日期的数字值
     * 20240305
     * @return
     */
    public static String getDateNum(Instant time){
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern(FORMAT_YYYYMMDD).withZone(ZoneId.systemDefault());
        String timeStr = formatter.format(time);
        return timeStr;
    }

    /**
     * 时间格式化
     */
    public static String getDateTime(Instant time, String format, ZoneId zoneId){
        if (zoneId==null){
            zoneId = ZoneId.systemDefault();
        }
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern(format).withZone(zoneId);
        String timeStr = formatter.format(time);
        return timeStr;
    }

    /**
     * 计算同月两个时间的日期差
     * @param time1
     * @param time2
     * @return
     */
    public static Integer timeMinusByDayOfMonth(Instant time1, Instant time2){
        LocalDateTime dateTime1 = LocalDateTime.ofInstant(time1, ZoneOffset.of("+0"));
        LocalDateTime dateTime2 = LocalDateTime.ofInstant(time2, ZoneOffset.of("+0"));
        int days = dateTime2.getDayOfMonth()-dateTime1.getDayOfMonth();
        return days;
    }

    public static String getTimeForZ8(Instant time){
        LocalDateTime dateTime = LocalDateTime.ofInstant(time, ZoneOffset.of("+8"));
        String dateStr = dateTime.format(DateTimeFormatter.ISO_DATE);
        return dateStr;
    }

    public static void main(String[] args) {

//        System.out.println(getMonthStartTime());

//        LocalDateTime now = LocalDateTime.now();
//        LocalDateTime oldTime = now.minusHours(4);
//        System.out.println(timeMinusByDayOfMonth(oldTime.toInstant(ZoneOffset.of("+0")), Instant.now()));

//        System.out.println(getTimeForZ8(Instant.now()));

        System.out.println(getDateNum(Instant.now()));

    }
}

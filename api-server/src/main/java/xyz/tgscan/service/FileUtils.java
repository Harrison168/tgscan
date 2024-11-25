package xyz.tgscan.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Base64;

@Slf4j
@Component
public class FileUtils {

    @Value("${files.dir.icon}")
    private String iconDir; // 图标存放路径


    public String downloadIcon(String url, String linkId) {
        String fileName = null;
        try {
            // 检查是否为 base64 数据 URI
            if (url.startsWith("data:image")) {
                fileName = downloadBase64Image(url, linkId);
            } else if (url.startsWith("https://")) {
                fileName = downloadHttpsImage(url, linkId);
            } else {
                log.error("不支持的URL格式：" + url);
            }
        } catch (Exception e) {
            log.error("downloadIcon error, url={}", url, e);
        }
        return fileName;
    }

    /**
     * 下载 HTTPS 图像并保存到文件
     */
    private String downloadHttpsImage(String url, String linkId) throws Exception {
        URL imageUrl = new URL(url);
        HttpURLConnection connection = (HttpURLConnection) imageUrl.openConnection();
        connection.setRequestMethod("GET");
        connection.setConnectTimeout(5000);
        connection.setReadTimeout(5000);

        if (connection.getResponseCode() == HttpURLConnection.HTTP_OK) {
            String contentType = connection.getContentType();
            String fileExtension = getFileExtensionFromContentType(contentType);

            if (fileExtension == null) {
                log.error("未知的内容类型：" + contentType);
                return null;
            }

            Path downloadDirPath = Paths.get(iconDir);
            if (Files.notExists(downloadDirPath)) {
                Files.createDirectories(downloadDirPath);
            }

            String fileName = "icon_" + linkId + fileExtension;
            String iconPath = iconDir + "/" + fileName;
            Path path = Paths.get(iconPath);

            try (InputStream inputStream = connection.getInputStream()) {
                Files.copy(inputStream, path, StandardCopyOption.REPLACE_EXISTING);
            }

            return fileName;
        } else {
            log.error("下载失败，HTTP响应代码：" + connection.getResponseCode());
            return null;
        }
    }

    /**
     * 处理 base64 图像数据并保存到文件
     */
    private String downloadBase64Image(String base64Data, String linkId) throws Exception {
        String[] parts = base64Data.split(",");
        if (parts.length != 2 || !parts[0].startsWith("data:image")) {
            log.error("无效的 Base64 图像数据");
            return null;
        }

        // 解码 URL 编码的 Base64 数据
        String base64Content = URLDecoder.decode(parts[1], StandardCharsets.UTF_8);

        String mimeType = parts[0].split(";")[0].split(":")[1];
        String fileExtension = getFileExtensionFromContentType(mimeType);

        if (fileExtension == null) {
            log.error("未知的 MIME 类型：" + mimeType);
            return null;
        }


        // 进行解码并保存图像文件
        byte[] imageBytes = Base64.getDecoder().decode(base64Content);

        Path downloadDirPath = Paths.get(iconDir);
        if (Files.notExists(downloadDirPath)) {
            Files.createDirectories(downloadDirPath);
        }

        String fileName = "icon_" + linkId + fileExtension;
        String iconPath = iconDir + "/" + fileName;
        Path path = Paths.get(iconPath);

        try (OutputStream outputStream = Files.newOutputStream(path)) {
            outputStream.write(imageBytes);
        }

        return fileName;
    }

    /**
     * 根据 MIME 类型返回文件扩展名
     */
    private String getFileExtensionFromContentType(String contentType) {
        if (contentType == null) return null;
        switch (contentType) {
            case "image/png":
                return ".png";
            case "image/jpeg":
                return ".jpg";
            case "image/gif":
                return ".gif";
            case "image/svg+xml":
                return ".svg";
            case "image/webp":
                return ".webp";
            case "image/bmp":
                return ".bmp";
            default:
                return null; // 如果内容类型未知，返回 null
        }
    }
}

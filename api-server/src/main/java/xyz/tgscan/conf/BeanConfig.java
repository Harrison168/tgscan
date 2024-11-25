package xyz.tgscan.conf;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import xyz.tgscan.service.TelegramSearchBot;

@Slf4j
@Configuration
public class BeanConfig {

    @Value("${telegram.bot.token}")
    private String botToken;

    @Value("${telegram.bot.username}")
    private String botUsername;

    @Value("${telegram.bot.webhook.path}")
    private String botPath;

    @Value("${api.root}")
    private String apiRoot;

    @Bean
    public TelegramSearchBot telegramBot() {
        return new TelegramSearchBot(botToken, botUsername, apiRoot+botPath);
    }
}

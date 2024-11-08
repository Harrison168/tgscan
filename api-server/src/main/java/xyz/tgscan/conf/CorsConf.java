package xyz.tgscan.conf;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import xyz.tgscan.service.TelegramBot;

@Configuration
public class CorsConf {


  @Value("${telegram.bot.token}")
  private String botToken;

  @Value("${telegram.bot.username}")
  private String botUsername;

  @Value("${telegram.bot.webhook.path}")
  private String botPath;

  @Value("${api.root}")
  private String apiRoot;

  @Bean
  public WebMvcConfigurer corsConfigurer() {
    return new WebMvcConfigurer() {
      @Override
      public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**").allowedOriginPatterns("*").allowCredentials(true);
      }
    };
  }

  @Bean
  public TelegramBot telegramBot() {
    return new TelegramBot(botToken, botUsername, apiRoot+botPath);
  }
}

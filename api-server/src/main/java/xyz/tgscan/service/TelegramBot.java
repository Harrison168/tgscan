package xyz.tgscan.service;

import org.telegram.telegrambots.bots.TelegramWebhookBot;
import org.telegram.telegrambots.meta.api.methods.BotApiMethod;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;

public class TelegramBot extends TelegramWebhookBot {

    private final String botToken;
    private final String botUsername;
    private final String botPath;

    public TelegramBot(String botToken, String botUsername, String botPath) {
        this.botToken = botToken;
        this.botUsername = botUsername;
        this.botPath = botPath;
    }

    @Override
    public String getBotToken() {
        return botToken;
    }

    @Override
    public String getBotUsername() {
        return botUsername;
    }

    @Override
    public String getBotPath() {
        return botPath;
    }

    @Override
    public BotApiMethod<?> onWebhookUpdateReceived(Update update) {
        if (update.hasMessage()) {
            Message message = update.getMessage();
            String chatId = message.getChatId().toString();
            SendMessage response = new SendMessage();
            response.setChatId(chatId);
            response.setText("Hello! You sent: " + message.getText());
            return response;
        }
        return null;
    }
}

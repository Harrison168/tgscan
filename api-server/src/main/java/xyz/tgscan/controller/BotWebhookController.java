package xyz.tgscan.controller;

import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.telegram.telegrambots.meta.api.methods.BotApiMethod;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;
import xyz.tgscan.enums.TgRoomTypeParamEnum;
import xyz.tgscan.service.SearchService;
import xyz.tgscan.service.TelegramBot;
import xyz.tgscan.utils.NetUtil;
import xyz.tgscan.utils.SearchLogUtil;

@RestController
@Slf4j
@RequestMapping("/api/bot")
public class BotWebhookController {

    @Autowired
    private TelegramBot telegramBot;

    @Autowired
    private SearchService searchService;
    @Autowired
    private SearchLogUtil searchLogUtil;
    @Autowired
    private HttpServletRequest request;


    @PostMapping(value = "/webhook")
    public BotApiMethod<?> onUpdateReceived(@RequestBody Update update) {
        if (update.hasMessage()) {
            Message message = update.getMessage();
            String chatId = message.getChatId().toString();
            String kw = message.getText();

            searchLogUtil.log(kw, TgRoomTypeParamEnum.ALL.name(), 1, NetUtil.getClientIp(request));
            searchService.recall(kw, 1, TgRoomTypeParamEnum.ALL);

            // --todo --
            SendMessage response = new SendMessage();
            response.setChatId(chatId);
            response.setText("Hello! You sent: " + message.getText());
            return response;
        }

        return telegramBot.onWebhookUpdateReceived(update);
    }

}

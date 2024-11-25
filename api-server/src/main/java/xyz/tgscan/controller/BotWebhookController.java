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
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import xyz.tgscan.dto.RoomDocDTO;
import xyz.tgscan.dto.SearchRespDTO;
import xyz.tgscan.enums.TgRoomTypeParamEnum;
import xyz.tgscan.service.SearchService;
import xyz.tgscan.service.TelegramSearchBot;
import xyz.tgscan.utils.NetUtil;
import xyz.tgscan.utils.SearchLogUtil;

@RestController
@Slf4j
@RequestMapping("/api/bot")
public class BotWebhookController {

    @Autowired
    private TelegramSearchBot telegramSearchBot;

//    @Autowired
//    private SearchService searchService;
//    @Autowired
//    private SearchLogUtil searchLogUtil;
//    @Autowired
//    private HttpServletRequest request;


    @PostMapping(value = "/search")
    public BotApiMethod<?> search(@RequestBody Update update) {
        return telegramSearchBot.onWebhookUpdateReceived(update);
    }




}

package xyz.tgscan.service;

import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.telegram.telegrambots.bots.TelegramWebhookBot;
import org.telegram.telegrambots.meta.api.methods.BotApiMethod;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import xyz.tgscan.dto.RoomDocDTO;
import xyz.tgscan.dto.SearchRespDTO;
import xyz.tgscan.enums.TgRoomTypeParamEnum;
import xyz.tgscan.utils.NetUtil;
import xyz.tgscan.utils.SearchLogUtil;

import java.util.ArrayList;
import java.util.List;

@Slf4j
public class TelegramSearchBot extends TelegramWebhookBot {

    private final String botToken;
    private final String botUsername;
    private final String botPath;

    @Autowired
    private SearchService searchService;
    @Autowired
    private SearchLogUtil searchLogUtil;
    @Autowired
    private HttpServletRequest request;

    public TelegramSearchBot(String botToken, String botUsername, String botPath) {
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
            String kw = message.getText();

            log.info("bot/search, Received message = {}", kw);
            searchLogUtil.log(kw, TgRoomTypeParamEnum.ALL.name(), 1, NetUtil.getClientIp(request));
            SearchRespDTO respDTO = searchService.recall(kw, 1, TgRoomTypeParamEnum.ALL);

            log.info("bot/search, Message sent successfully to chatId={}", chatId);
            return sendMessageWithHtml(chatId, respDTO);
        }

        return null;
    }

    private SendMessage sendMessageWithHtml(String chatId, SearchRespDTO respDTO) {
        StringBuilder messageBuilder = new StringBuilder("<b>Here are the links:</b>\n\n");

        for (Object entity : respDTO.getDoc()) {
            RoomDocDTO room = (RoomDocDTO) entity;
            messageBuilder.append(String.format("<a href=\"%s\">%s</a>\n", room.getLink(), room.getName()));
        }

//        log.info("bot/search, sendMessageWithHtml = {}", messageBuilder.toString());

        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(messageBuilder.toString());
        message.setParseMode("HTML"); // 使用 HTML 格式
        message.setDisableWebPagePreview(true); // 禁用 URL 预览

        createInlineKeyboardMessage(message);

        return message;
    }

    private void createInlineKeyboardMessage(SendMessage message){
        // 创建按钮
        InlineKeyboardButton button1 = new InlineKeyboardButton();
        button1.setText("🔥 热门频道");
        button1.setCallbackData("hot_channels");

        InlineKeyboardButton button2 = new InlineKeyboardButton();
        button2.setText("🔥 热搜词");
        button2.setCallbackData("hot_keywords");

        InlineKeyboardButton button3 = new InlineKeyboardButton();
        button3.setText("🔥 热门分类");
        button3.setCallbackData("hot_categories");

        // 将按钮添加到一行
        List<InlineKeyboardButton> row1 = new ArrayList<>();
        row1.add(button1);
        row1.add(button2);
        row1.add(button3);

        // 另一行按钮
        InlineKeyboardButton button4 = new InlineKeyboardButton();
        button4.setText("📋 帮助");
        button4.setCallbackData("help");

        InlineKeyboardButton button5 = new InlineKeyboardButton();
        button5.setText("➕ 添加群组赚钱");
        button5.setCallbackData("add_group");

        List<InlineKeyboardButton> row2 = new ArrayList<>();
        row2.add(button4);
        row2.add(button5);

        // 创建键盘
        InlineKeyboardMarkup inlineKeyboard = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> keyboard = new ArrayList<>();
        keyboard.add(row1);
        keyboard.add(row2);
        inlineKeyboard.setKeyboard(keyboard);

        // 设置键盘
        message.setReplyMarkup(inlineKeyboard);
    }
}

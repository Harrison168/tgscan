package xyz.tgscan.controller;

import com.alibaba.fastjson2.JSON;
import jakarta.servlet.http.HttpServletRequest;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.*;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import nonapi.io.github.classgraph.utils.URLPathEncoder;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;
import xyz.tgscan.domain.Offsets;
import xyz.tgscan.dto.*;
import xyz.tgscan.dto.requests.RecommendRequest;
import xyz.tgscan.enums.IdxConstant;
import xyz.tgscan.enums.TgRoomTypeParamEnum;
import xyz.tgscan.service.SearchService;
import xyz.tgscan.utils.NetUtil;
import xyz.tgscan.utils.RoomLinksUtil;
import xyz.tgscan.utils.SearchLogUtil;
import xyz.tgscan.utils.StringUtil;

import static xyz.tgscan.enums.IdxConstant.HOME_RECOM_PAGE_SIZE;

@RestController
@Slf4j
@RequestMapping("/api/search")
public class SearchController {

  @Autowired
  private SearchLogUtil searchLogUtil;
  @Autowired
  private HttpServletRequest request;
  @Autowired
  private RoomLinksUtil roomLinksUtil;
  private HttpClient client = HttpClients.createDefault();
  @Autowired
  private SearchService searchService;



  @GetMapping("query")
  public SearchRespDTO query(
      @RequestParam("kw") String kw,
      @RequestParam(value = "p", required = false, defaultValue = "1") Integer page,
      @RequestParam(value = "t", required = false, defaultValue = "ALL") TgRoomTypeParamEnum type) {

    searchLogUtil.log(kw, type.name(), page, NetUtil.getClientIp(request));
    return searchService.recall(kw, page, type);
  }

  @GetMapping("getById")
  public SearchRespDTO getById(
          @RequestParam("id") String id,
          @RequestParam(value = "t", required = false, defaultValue = "ALL") TgRoomTypeParamEnum type) {

    searchLogUtil.log(id, type.name(), null, NetUtil.getClientIp(request));
    return searchService.getById(id, type);
  }

  @SneakyThrows
  @GetMapping("autocomplete")
  public List<String> autocomplete(@RequestParam("kw") String kw) {
    var resp = client.execute(
        new HttpGet(
            "http://api.bing.com/qsonhs.aspx?q=" + URLPathEncoder.encodePath(kw)));
    var entity = resp.getEntity();
    var string = EntityUtils.toString(entity);
    var json = JSON.parseObject(string, AutoCompleteDTO.class);
    if (Objects.isNull(json.aS.results)) {
      return Collections.emptyList();
    }
    return json.aS.results.stream()
        .map(x -> x.suggests)
        .flatMap(Collection::stream)
        .map(x -> x.txt)
        .toList();
  }

  @GetMapping(value = "/image/{imageName}", produces = MediaType.IMAGE_JPEG_VALUE)
  public byte[] getImage(@PathVariable String imageName) throws IOException {
    File file = new File("icon/" + imageName + ".jpg");
    if (!file.exists()) {
      file = new File("icon/tg.jpg");
    }
    FileInputStream inputStream = new FileInputStream(file);
    byte[] bytes = new byte[(int) file.length()];
    inputStream.read(bytes);
    inputStream.close();
    return bytes;
  }

  @GetMapping("roomLinks")
  public List<Offsets> roomLinks() {
    return roomLinksUtil.roomLinks();
  }


  @PostMapping("recommend")
  public SearchRespDTO getRecommendedRooms(@RequestBody RecommendRequest request) {
    if (request.getPage() == null){
      request.setPage(1);
    }
    if (StringUtils.hasLength(request.getLang())){
      request.setLang(IdxConstant.DEFAULT_LANG);
    }

    return searchService.getRecommendedRooms(HOME_RECOM_PAGE_SIZE, request.getPage(), request.getUserTags(), request.getLang());
  }
}

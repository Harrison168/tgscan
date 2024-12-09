package xyz.tgscan.dto;

import jakarta.persistence.Id;
import lombok.Data;
import lombok.experimental.Accessors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.elasticsearch.annotations.Document;
import xyz.tgscan.enums.IdxConstant;
import xyz.tgscan.utils.TimeUtils;

import java.time.Instant;
import java.util.Map;

@Slf4j
@Data
@Accessors(chain = true)
@Document(indexName = IdxConstant.ROOM_IDX, createIndex = false)
public class RoomDocDTO {

  @Id private String id;

  private String link;

  private Integer memberCnt;

  private String type;

  private String status;

  private String icon;

  private String name;

  private String jhiDesc;

  private String sendDate;

  private String lang;

  private String tags;

  public static RoomDocDTO fromTgRoomDoc(Map tgRoomDoc, String icon_url_path) {
    RoomDocDTO roomDocDTO = new RoomDocDTO();
    roomDocDTO.setId(tgRoomDoc.get("id").toString());
    roomDocDTO.setLink((String) tgRoomDoc.get("link"));
    roomDocDTO.setMemberCnt((Integer) tgRoomDoc.get("memberCnt"));
    roomDocDTO.setType((String) tgRoomDoc.get("type"));
    roomDocDTO.setStatus((String) tgRoomDoc.get("status"));
    roomDocDTO.setIcon((String) icon_url_path + "/" + tgRoomDoc.get("icon"));
    roomDocDTO.setName((String) tgRoomDoc.get("name"));
    roomDocDTO.setJhiDesc((String) tgRoomDoc.get("jhiDesc"));

    roomDocDTO.setSendDate(TimeUtils.getDateTime(Instant.ofEpochMilli( Long.parseLong(tgRoomDoc.get("sendTime")+"")), TimeUtils.FORMAT_dd_MM_yyyy, null));

    roomDocDTO.setLang((String) tgRoomDoc.get("lang"));
    roomDocDTO.setTags((String) tgRoomDoc.get("tags"));

    return roomDocDTO;
  }
}

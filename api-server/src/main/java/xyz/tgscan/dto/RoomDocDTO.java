package xyz.tgscan.dto;

import jakarta.persistence.Id;

import java.time.Instant;
import java.util.Map;
import lombok.Data;
import lombok.experimental.Accessors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.util.StringUtils;
import xyz.tgscan.enums.IdxConstant;
import xyz.tgscan.utils.StringUtil;
import xyz.tgscan.utils.TimeUtils;

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

  public static RoomDocDTO fromTgRoomDoc(Map tgRoomDoc) {
    RoomDocDTO roomDocDTO = new RoomDocDTO();
    roomDocDTO.setId(tgRoomDoc.get("id").toString());
    roomDocDTO.setLink((String) tgRoomDoc.get("link"));
    roomDocDTO.setMemberCnt((Integer) tgRoomDoc.get("memberCnt"));
    roomDocDTO.setType((String) tgRoomDoc.get("type"));
    roomDocDTO.setStatus((String) tgRoomDoc.get("status"));
    roomDocDTO.setIcon((String) tgRoomDoc.get("icon"));
    roomDocDTO.setName((String) tgRoomDoc.get("name"));
    roomDocDTO.setJhiDesc((String) tgRoomDoc.get("jhiDesc"));

    roomDocDTO.setSendDate(TimeUtils.getDateTime(Instant.ofEpochSecond((Integer) tgRoomDoc.get("sendTime")), TimeUtils.FORMAT_dd_MM_yyyy, null));

    return roomDocDTO;
  }
}

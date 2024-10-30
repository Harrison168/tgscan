package xyz.tgscan.domain;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.Id;
import java.util.Date;
import lombok.Data;
import lombok.experimental.Accessors;
import org.springframework.data.elasticsearch.annotations.Document;
import xyz.tgscan.enums.IdxConstant;

@Data
@Accessors(chain = true)
@Document(indexName = IdxConstant.ROOM_IDX, createIndex = false)
public class RoomDoc {
  @JsonIgnore private String _class;
  @Id private String id;

  private String link;
  private String userName;
  private String name;
  private String phraseName;
  private String standardName;

  private String jhiDesc;
  private String standardJhiDesc;
  private String phraseJhiDesc;

  private Integer memberCnt;

  private String type;

  private String status;

  private String icon;

  private Date sendTime;

  public static RoomDoc fromEntity(Room room) {
    RoomDoc roomDoc = new RoomDoc();
    roomDoc.setId(room.getLink());
    roomDoc.setPhraseName(room.getName());
    roomDoc.setStandardName(room.getName());
    var split = room.getLink().split("/");
    roomDoc.setUserName(split[split.length - 1]);
    roomDoc.setPhraseJhiDesc(room.getJhiDesc());
    roomDoc.setStandardJhiDesc(room.getJhiDesc());
    roomDoc.setLink(room.getLink());
    roomDoc.setName(room.getName());
    roomDoc.setJhiDesc(room.getJhiDesc());
    roomDoc.setMemberCnt(room.getMemberCnt());
    roomDoc.setType(room.getType());
    roomDoc.setStatus(room.getStatus());
    roomDoc.setSendTime(new Date(room.getCollectedAt().getTime()));
    roomDoc.setIcon(room.getIcon());
    return roomDoc;
  }
}

package xyz.tgscan.dto.requests;

import lombok.Data;

import java.util.List;

@Data
public class RecommendRequest {

    private Integer page;
    private List<String> userTags;
    private String lang;
}

package com.coinlytics.backend.dto;

import lombok.Data;

import java.util.List;
import java.util.Map;

@Data
public class AiAnalysisResponseDto {

    private Object type_2_category_statistics;

    private List<Map<String, Object>> type_3_anomalies;

    private Object type_5_health_score;
}
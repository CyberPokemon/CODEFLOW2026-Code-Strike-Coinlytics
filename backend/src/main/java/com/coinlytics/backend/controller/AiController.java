package com.coinlytics.backend.controller;

import com.coinlytics.backend.dto.AiAnalysisResponseDto;
import com.coinlytics.backend.service.AiService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
public class AiController {

    private final AiService aiService;

    @GetMapping("/analyze/{tableNo}")
    public ResponseEntity<AiAnalysisResponseDto> analyze(
            @PathVariable Long tableNo
    ) {

        return ResponseEntity.ok(
                aiService.analyze(tableNo)
        );
    }
}

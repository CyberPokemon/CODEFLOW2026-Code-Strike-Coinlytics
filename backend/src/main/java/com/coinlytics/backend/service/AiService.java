package com.coinlytics.backend.service;

import com.coinlytics.backend.dto.AiAnalysisResponseDto;
import com.coinlytics.backend.model.UploadedFile;
import com.coinlytics.backend.model.Users;
import com.coinlytics.backend.repository.UploadedFileRepository;
import com.coinlytics.backend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
@RequiredArgsConstructor
public class AiService {

    private final UserRepository userRepository;

    private final UploadedFileRepository uploadedFileRepository;

    private final RestTemplate restTemplate;

    @Value("${ml.api.url}")
    private String mlApiUrl;

    public AiAnalysisResponseDto analyze(Long tableNo) {

        // FETCH LOGGED IN USER EMAIL FROM JWT
        String email = SecurityContextHolder
                .getContext()
                .getAuthentication()
                .getName();

        Users user = userRepository.findByEmail(email)
                .orElseThrow(() ->
                        new RuntimeException("User not found"));

        // VALIDATE TABLE OWNERSHIP
        UploadedFile uploadedFile =
                uploadedFileRepository.findById(tableNo)
                        .orElseThrow(() ->
                                new RuntimeException("Table not found"));

        if(!uploadedFile.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("Unauthorized access");
        }

        // CALL ML API
        String url =
                mlApiUrl +
                        "/analyze/" +
                        user.getId() +
                        "/" +
                        tableNo;

        Map response =
                restTemplate.getForObject(url, Map.class);

        // FILTER REQUIRED DATA
        AiAnalysisResponseDto dto =
                new AiAnalysisResponseDto();

        dto.setType_2_category_statistics(
                response.get("type_2_category_statistics")
        );

        dto.setType_3_anomalies(
                (java.util.List<java.util.Map<String, Object>>)
                        response.get("type_3_anomalies")
        );

        dto.setType_5_health_score(
                response.get("type_5_health_score")
        );

        return dto;
    }
}
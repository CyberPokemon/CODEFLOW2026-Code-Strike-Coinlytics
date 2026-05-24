package com.coinlytics.backend.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@Builder
public class FileResponseDto {

    private Long fileNo;

    private String originalFilename;

    private LocalDateTime uploadedAt;

    private LocalDateTime encryptedExpiryAt;
}
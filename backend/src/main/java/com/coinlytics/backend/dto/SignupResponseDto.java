package com.coinlytics.backend.dto;

import lombok.Data;

@Data
public class SignupResponseDto {
    
    private String username;
    private String accessToken;
}
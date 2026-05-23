package com.coinlytics.backend.dto;

import lombok.Data;

@Data
public class LoginResponseDto {
    String jwt;
    Long userId;
}

package com.coinlytics.backend.dto;

import com.coinlytics.backend.model.Role;
import lombok.Data;

@Data
public class SignupRequest {
    private String name;
    private String email;
    private String password;
    private Role role;
}

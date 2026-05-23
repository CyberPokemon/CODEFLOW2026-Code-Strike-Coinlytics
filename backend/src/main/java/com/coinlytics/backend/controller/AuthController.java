package com.coinlytics.backend.controller;

import com.coinlytics.backend.dto.LoginRequest;
import com.coinlytics.backend.dto.LoginResponseDto;
import com.coinlytics.backend.dto.SignupRequest;
import com.coinlytics.backend.dto.SignupResponseDto;
import com.coinlytics.backend.service.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    @Autowired
    private final AuthService authService;

    @PostMapping("/signup")
    public ResponseEntity<SignupResponseDto> register(@RequestBody SignupRequest request) {
        return ResponseEntity.ok(authService.register(request));
    }

    @PostMapping("/login")
    public ResponseEntity<LoginResponseDto> login(@RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }
}

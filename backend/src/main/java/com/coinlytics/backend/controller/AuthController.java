package com.coinlytics.backend.controller;

import com.coinlytics.backend.dto.LoginRequest;
import com.coinlytics.backend.dto.SignupRequest;
import com.coinlytics.backend.service.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    @Autowired
    private final AuthService authService;

    @PostMapping("/signup")
    public String register(
            @RequestBody SignupRequest request
    ) {
        return authService.register(request);
    }

    @PostMapping("/login")
    public String login(@RequestBody LoginRequest request
    ) {
        return authService.login(request);
    }
}

package com.coinlytics.backend.service;

import com.coinlytics.backend.dto.LoginRequest;
import com.coinlytics.backend.dto.SignupRequest;
import com.coinlytics.backend.model.Users;
import com.coinlytics.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtService jwtService;

    public String register(SignupRequest request) {
        if(userRepository.findByEmail(request.getEmail()).isPresent())
        {
            return "User already exists. Please login.";
        }
        Users users=new Users();
        users.setName(request.getName());
        users.setEmail(request.getEmail());
        users.setRole(request.getRole());
        users.setPhoneNumber(request.getPhoneNumber());
        users.setPassword(passwordEncoder.encode(request.getPassword()));
        userRepository.save(users);
        return "Registration Done.";
    }

    public String login(LoginRequest request) {

        Users users=userRepository.findByEmail(request.getEmail())
                .orElse(null);

        if(users==null)
        {
            return "User not registered. Please signup first.";
        }

        authenticationManager.authenticate
                (new UsernamePasswordAuthenticationToken(
                        request.getEmail(),request.getPassword()));
        return jwtService.generateToken(request.getEmail());
    }
}

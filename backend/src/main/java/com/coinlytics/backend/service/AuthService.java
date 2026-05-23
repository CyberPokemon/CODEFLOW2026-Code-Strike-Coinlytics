package com.coinlytics.backend.service;

import com.coinlytics.backend.dto.LoginRequest;
import com.coinlytics.backend.dto.LoginResponseDto;
import com.coinlytics.backend.dto.SignupRequest;
import com.coinlytics.backend.dto.SignupResponseDto;
import com.coinlytics.backend.error.customException.UserAlreadyExistsException;
import com.coinlytics.backend.error.customException.UserNotExistsException;
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

    public SignupResponseDto register(SignupRequest request) {
        if(userRepository.findByEmail(request.getEmail()).isPresent())
        {
            throw new UserAlreadyExistsException("User already exists. Please login.");
        }
        Users users=new Users();
        users.setName(request.getName());
        users.setEmail(request.getEmail());
        users.setRole(request.getRole());
        users.setPhoneNumber(request.getPhoneNumber());
        users.setPassword(passwordEncoder.encode(request.getPassword()));
        userRepository.save(users);
        return new SignupResponseDto(request.getEmail(),jwtService.generateToken(request.getEmail()));
    }

    public LoginResponseDto login(LoginRequest request) {

        Users users=userRepository.findByEmail(request.getEmail())
                .orElse(null);

        if(users==null)
        {
            throw new UserNotExistsException("User not registered. Please signup first.");
        }

        authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(
                        request.getEmail(),request.getPassword()));
        return new LoginResponseDto(request.getEmail(),jwtService.generateToken(request.getEmail()));
    }
}

package com.coinlytics.backend.service;

import com.coinlytics.backend.model.UploadedFile;
import com.coinlytics.backend.model.Users;
import com.coinlytics.backend.repository.UploadedFileRepository;
import com.coinlytics.backend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.nio.file.Files;
import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class FileService {

    private final UploadedFileRepository uploadedFileRepository;
    private final UserRepository userRepository;

    private static final String UPLOAD_DIR =
            "encrypted_uploads/";

    public String uploadCsv(MultipartFile file)
            throws Exception {

        // Validate CSV
        if (!file.getOriginalFilename().endsWith(".csv")) {
            throw new RuntimeException(
                    "Only CSV files allowed."
            );
        }

        // Get authenticated user email
        String email =
                SecurityContextHolder.getContext()
                        .getAuthentication()
                        .getName();

        Users user = userRepository.findByEmail(email)
                .orElseThrow(() ->
                        new RuntimeException("User not found"));

        // Create folder
        File directory = new File(UPLOAD_DIR);

        if (!directory.exists()) {
            directory.mkdirs();
        }

        // Read bytes
        byte[] fileBytes = file.getBytes();

        // Encrypt bytes
        byte[] encryptedBytes =
                AESUtil.encrypt(fileBytes);

        // Create encrypted filename
        String encryptedFileName =
                System.currentTimeMillis()
                        + "_"
                        + file.getOriginalFilename()
                        + ".enc";

        String path =
                UPLOAD_DIR + encryptedFileName;

        // Save encrypted file
        Files.write(
                new File(path).toPath(),
                encryptedBytes
        );

        // Save metadata
        UploadedFile uploadedFile =
                UploadedFile.builder()
                        .fileName(file.getOriginalFilename())
                        .encryptedPath(path)
                        .uploadedAt(LocalDateTime.now())
                        .lastAccessedAt(LocalDateTime.now())
                        .user(user)
                        .build();

        uploadedFileRepository.save(uploadedFile);

        return "Encrypted file uploaded successfully.";
    }
}

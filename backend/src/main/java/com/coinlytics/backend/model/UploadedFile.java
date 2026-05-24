package com.coinlytics.backend.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "uploaded_files")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UploadedFile {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long fileNo;

    private String originalFilename;

    private String encryptedPath;

    private LocalDateTime uploadedAt;

    private LocalDateTime sqlExpiryAt;

    private LocalDateTime encryptedExpiryAt;

    private boolean sqlPresent;

    private boolean filePresent;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private Users user;
}
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

    private String fileName;

    private String encryptedPath;

    private LocalDateTime uploadedAt;

    private LocalDateTime lastAccessedAt;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private Users user;
}
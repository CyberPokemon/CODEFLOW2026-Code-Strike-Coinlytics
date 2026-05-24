package com.coinlytics.backend.repository;

import com.coinlytics.backend.model.UploadedFile;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface UploadedFileRepository extends JpaRepository<UploadedFile, Long> {
    List<UploadedFile> findByUserId(Long userId);
}

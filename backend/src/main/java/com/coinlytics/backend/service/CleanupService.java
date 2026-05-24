package com.coinlytics.backend.service;

import com.coinlytics.backend.model.UploadedFile;
import com.coinlytics.backend.repository.TransactionRepository;
import com.coinlytics.backend.repository.UploadedFileRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.File;
import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class CleanupService {

    private final UploadedFileRepository uploadedFileRepository;

    private final TransactionRepository transactionRepository;

    @Scheduled(fixedRate = 60000)
    public void cleanup() {

        List<UploadedFile> files =
                uploadedFileRepository.findAll();

        LocalDateTime now = LocalDateTime.now();

        for(UploadedFile file : files) {

            if(file.isSqlPresent() &&
                    now.isAfter(file.getSqlExpiryAt())) {

                transactionRepository.deleteByTableId(
                        file.getFileNo()
                );

                file.setSqlPresent(false);
            }

            if(file.isFilePresent() &&
                    now.isAfter(file.getEncryptedExpiryAt())) {

                new File(
                        file.getEncryptedPath()
                ).delete();

                file.setFilePresent(false);

                uploadedFileRepository.delete(file);
            }
        }
    }
}
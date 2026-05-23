package com.coinlytics.backend.controller;

import com.coinlytics.backend.service.FileService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/files")
@RequiredArgsConstructor
public class FileController {

    private final FileService fileService;

    @PostMapping("/upload")
    public ResponseEntity<String> uploadFile(
            @RequestParam("file")
            MultipartFile file
    ) {

        try {

            return ResponseEntity.ok(
                    fileService.uploadCsv(file)
            );

        } catch (Exception e) {

            return ResponseEntity.internalServerError()
                    .body(e.getMessage());
        }
    }
}

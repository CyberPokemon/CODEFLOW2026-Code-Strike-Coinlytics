package com.coinlytics.backend.controller;

import com.coinlytics.backend.service.FileService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/files")
@RequiredArgsConstructor
public class FileController {

    private final FileService fileService;

    @PostMapping("/upload")
    public ResponseEntity<?> upload(
            @RequestParam("file")
            MultipartFile file
    ) {

        try {

            return ResponseEntity.ok(
                    fileService.upload(file)
            );

        } catch (Exception e) {

            return ResponseEntity.badRequest()
                    .body(e.getMessage());
        }
    }

    @GetMapping("/{fileId}")
    public ResponseEntity<?> getFile(
            @PathVariable Long fileId
    ) {

        try {

            return ResponseEntity.ok(
                    fileService.getFileData(fileId)
            );

        } catch (Exception e) {

            return ResponseEntity.badRequest()
                    .body(e.getMessage());
        }
    }
}
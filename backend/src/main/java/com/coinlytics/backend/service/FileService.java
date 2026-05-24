package com.coinlytics.backend.service;

import com.coinlytics.backend.model.TransactionRecord;
import com.coinlytics.backend.model.UploadedFile;
import com.coinlytics.backend.model.Users;
import com.coinlytics.backend.repository.TransactionRepository;
import com.coinlytics.backend.repository.UploadedFileRepository;
import com.coinlytics.backend.repository.UserRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class FileService {

    private final UploadedFileRepository uploadedFileRepository;

    private final TransactionRepository transactionRepository;

    private final UserRepository userRepository;

    private final AESUtil aesUtil;

    private final CsvHeaderMapper csvHeaderMapper;

    private static final String DIRECTORY =
            "encrypted_files/";

    @Transactional
    public String upload(MultipartFile file)
            throws Exception {

        String email =
                SecurityContextHolder
                        .getContext()
                        .getAuthentication()
                        .getName();

        Users user =
                userRepository.findByEmail(email)
                        .orElseThrow();

        byte[] originalBytes = file.getBytes();

        validateAndSaveData(
                originalBytes,
                user
        );

        byte[] encrypted =
                aesUtil.encrypt(originalBytes);

        File dir = new File(DIRECTORY);

        if (!dir.exists()) {
            dir.mkdirs();
        }

        String path =
                DIRECTORY
                        + System.currentTimeMillis()
                        + ".enc";

        Files.write(Path.of(path), encrypted);

        UploadedFile uploadedFile =
                UploadedFile.builder()
                        .originalFilename(
                                file.getOriginalFilename()
                        )
                        .encryptedPath(path)
                        .uploadedAt(LocalDateTime.now())
                        .sqlExpiryAt(
                                LocalDateTime.now()
                                        .plusMinutes(30)
                        )
                        .encryptedExpiryAt(
                                LocalDateTime.now()
                                        .plusHours(1)
                        )
                        .sqlPresent(true)
                        .filePresent(true)
                        .user(user)
                        .build();

        uploadedFileRepository.save(uploadedFile);

        return "File Uploaded Successfully";
    }

    private void validateAndSaveData(
            byte[] bytes,
            Users user
    ) throws Exception {

        BufferedReader reader =
                new BufferedReader(
                        new InputStreamReader(
                                new ByteArrayInputStream(bytes)
                        )
                );

        CSVParser parser =
                CSVFormat.DEFAULT
                        .withFirstRecordAsHeader()
                        .parse(reader);

        Map<String, Integer> headers =
                parser.getHeaderMap();

        Map<String, String> normalized =
                new HashMap<>();

        for(String header : headers.keySet()) {

            String mapped =
                    csvHeaderMapper.normalize(header);

            if(mapped != null) {
                normalized.put(mapped, header);
            }
        }

        List<String> required =
                List.of(
                        "DATE",
                        "PARTICULARS",
                        "CREDIT",
                        "DEBIT",
                        "BALANCE"
                );

        if(!normalized.keySet().containsAll(required)) {
            throw new RuntimeException(
                    "Invalid bank statement format"
            );
        }

        long slNo = 1;

        for(CSVRecord record : parser) {

            TransactionRecord txn =
                    TransactionRecord.builder()
                            .slNo(slNo++)
                            .txnDate(
                                    LocalDate.parse(
                                            record.get(
                                                    normalized.get("DATE")
                                            )
                                    )
                            )
                            .particulars(
                                    record.get(
                                            normalized.get("PARTICULARS")
                                    )
                            )
                            .credit(
                                    parseDouble(
                                            record.get(
                                                    normalized.get("CREDIT")
                                            )
                                    )
                            )
                            .debit(
                                    parseDouble(
                                            record.get(
                                                    normalized.get("DEBIT")
                                            )
                                    )
                            )
                            .balance(
                                    parseDouble(
                                            record.get(
                                                    normalized.get("BALANCE")
                                            )
                                    )
                            )
                            .user(user)
                            .build();

            transactionRepository.save(txn);
        }
    }

    private Double parseDouble(String value) {

        if(value == null || value.isBlank()) {
            return 0.0;
        }

        return Double.parseDouble(
                value.replace(",", "")
        );
    }
}
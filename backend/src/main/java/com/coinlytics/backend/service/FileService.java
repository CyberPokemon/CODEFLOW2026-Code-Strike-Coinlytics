package com.coinlytics.backend.service;

import com.coinlytics.backend.dto.FileResponseDto;
import com.coinlytics.backend.dto.TransactionResponseDto;
import com.coinlytics.backend.model.TransactionRecord;
import com.coinlytics.backend.model.UploadedFile;
import com.coinlytics.backend.model.Users;
import com.coinlytics.backend.repository.TransactionRepository;
import com.coinlytics.backend.repository.UploadedFileRepository;
import com.coinlytics.backend.repository.UserRepository;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
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
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.nio.file.Path;

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

    @PersistenceContext
    private EntityManager entityManager;

    @Transactional
    public String upload(MultipartFile file) throws Exception {

        String email = SecurityContextHolder
                        .getContext()
                        .getAuthentication()
                        .getName();

        Users user = userRepository.findByEmail(email)
                        .orElseThrow();

        byte[] originalBytes = file.getBytes();

        byte[] encrypted = aesUtil.encrypt(originalBytes);

        File dir = new File(DIRECTORY);

        if (!dir.exists()) {
            dir.mkdirs();
        }

        String path = DIRECTORY
                        + System.currentTimeMillis()
                        + ".enc";

        Files.write(Path.of(path), encrypted);

        UploadedFile uploadedFile =
                UploadedFile.builder()
                        .originalFilename(file.getOriginalFilename())
                        .encryptedPath(path)
                        .uploadedAt(LocalDateTime.now())
                        .sqlExpiryAt(LocalDateTime.now().plusMinutes(30))
                        .encryptedExpiryAt(LocalDateTime.now().plusMinutes(60))
                        .sqlPresent(true)
                        .filePresent(true)
                        .user(user)
                        .build();

        UploadedFile savedFile = uploadedFileRepository.save(uploadedFile);

        validateAndSaveData(
                originalBytes,
                user,
                savedFile.getFileNo()
        );

        return "File Uploaded Successfully";
    }

    private void validateAndSaveData(
            byte[] bytes,
            Users user,
            Long tableId
    ) throws Exception {

        BufferedReader reader =
                new BufferedReader(
                        new InputStreamReader(
                                new ByteArrayInputStream(bytes)
                        )
                );

        CSVParser parser = CSVFormat.DEFAULT
                        .withFirstRecordAsHeader()
                        .parse(reader);

        Map<String, Integer> headers = parser.getHeaderMap();

        Map<String, String> normalized = new HashMap<>();

        for(String header : headers.keySet()) {

            String mapped = csvHeaderMapper.normalize(header);

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

        List<TransactionRecord> batch = new ArrayList<>();

        for(CSVRecord record : parser) {

            TransactionRecord txn =
                    TransactionRecord.builder()
                            .tableId(tableId)
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

            batch.add(txn);

            if(batch.size() == 1000) {
                transactionRepository.saveAll(batch);

                entityManager.flush();
                entityManager.clear();

                batch.clear();
            }
        }

        if(!batch.isEmpty()) {
            transactionRepository.saveAll(batch);
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

    @Transactional
    public List<TransactionResponseDto> getFileData(
            Long fileId
    ) throws Exception {

        String email = SecurityContextHolder
                        .getContext()
                        .getAuthentication()
                        .getName();

        Users user = userRepository.findByEmail(email).orElseThrow();

        UploadedFile uploadedFile = uploadedFileRepository.findById(fileId).orElseThrow(() ->new RuntimeException("File not found"));

        // OWNERSHIP VALIDATION
        if(!uploadedFile.getUser().getId().equals(user.getId())) {

            throw new RuntimeException("Unauthorized access");
        }

        // CASE 1 → SQL DATA EXISTS
        if(uploadedFile.isSqlPresent()) {

            List<TransactionRecord> records = transactionRepository.findByTableId(fileId);

            uploadedFile.setSqlExpiryAt(LocalDateTime.now().plusMinutes(30));

            uploadedFile.setEncryptedExpiryAt(LocalDateTime.now().plusHours(1));

            uploadedFileRepository.save(uploadedFile);

            return mapToDto(records);
        }

        // CASE 2 → SQL EXPIRED BUT FILE EXISTS
        if(uploadedFile.isFilePresent()) {

            byte[] encryptedBytes = Files.readAllBytes(Path.of(uploadedFile.getEncryptedPath()));

            byte[] decryptedBytes = aesUtil.decrypt(encryptedBytes);

            rebuildTransactions(decryptedBytes, uploadedFile, user);

            uploadedFile.setSqlPresent(true);

            uploadedFile.setSqlExpiryAt(LocalDateTime.now().plusMinutes(30));

            uploadedFile.setEncryptedExpiryAt(LocalDateTime.now().plusHours(1));

            uploadedFileRepository.save(uploadedFile);

            List<TransactionRecord> records = transactionRepository.findByTableId(fileId);

            return mapToDto(records);
        }

        throw new RuntimeException("Data expired permanently");
    }

    private void rebuildTransactions(byte[] bytes, UploadedFile uploadedFile, Users user) throws Exception {

        BufferedReader reader =new BufferedReader(new InputStreamReader(new ByteArrayInputStream(bytes)));

        CSVParser parser = CSVFormat.DEFAULT
                        .withFirstRecordAsHeader()
                        .parse(reader);

        Map<String, Integer> headers = parser.getHeaderMap();

        Map<String, String> normalized = new HashMap<>();

        for(String header : headers.keySet()) {

            String mapped = csvHeaderMapper.normalize(header);

            if(mapped != null) {
                normalized.put(mapped, header);
            }
        }

        long slNo = 1;

        for(CSVRecord record : parser) {

            TransactionRecord txn = TransactionRecord.builder()
                            .tableId(uploadedFile.getFileNo())
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

    private List<TransactionResponseDto> mapToDto(
            List<TransactionRecord> records
    ) {

        return records.stream()
                .map(record ->
                        TransactionResponseDto.builder()
                                .slNo(record.getSlNo())
                                .txnDate(record.getTxnDate())
                                .particulars(record.getParticulars())
                                .credit(record.getCredit())
                                .debit(record.getDebit())
                                .balance(record.getBalance())
                                .build()
                )
                .toList();
    }

    @Transactional
    public String deleteFile(Long fileId)
            throws Exception {

        String email = SecurityContextHolder
                        .getContext()
                        .getAuthentication()
                        .getName();

        Users user = userRepository.findByEmail(email)
                        .orElseThrow();

        UploadedFile uploadedFile =
                uploadedFileRepository.findById(fileId)
                        .orElseThrow(() ->
                                new RuntimeException(
                                        "File not found"
                                )
                        );

        // OWNERSHIP CHECK
        if(!uploadedFile.getUser().getId().equals(user.getId())) {

            throw new RuntimeException("Unauthorized");
        }

        // DELETE SQL DATA
        transactionRepository.deleteByTableId(fileId);

        // DELETE ENCRYPTED FILE
        File encryptedFile = new File(uploadedFile.getEncryptedPath());

        if(encryptedFile.exists()) {
            encryptedFile.delete();
        }

        // DELETE METADATA
        uploadedFileRepository.delete(uploadedFile);

        return "File deleted successfully";
    }


    public List<FileResponseDto> getFiles() {

        String email = SecurityContextHolder
                .getContext()
                .getAuthentication()
                .getName();

        Users user = userRepository.findByEmail(email)
                .orElseThrow();

        List<UploadedFile> files =
                uploadedFileRepository.findByUserId(user.getId());

        return files.stream()
                .map(file ->
                        FileResponseDto.builder()
                                .fileNo(file.getFileNo())
                                .originalFilename(file.getOriginalFilename())
                                .uploadedAt(file.getUploadedAt())
                                .encryptedExpiryAt(file.getEncryptedExpiryAt())
                                .build()
                )
                .toList();
    }
}
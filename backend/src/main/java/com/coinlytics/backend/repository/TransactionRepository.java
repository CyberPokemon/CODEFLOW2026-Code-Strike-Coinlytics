package com.coinlytics.backend.repository;

import com.coinlytics.backend.model.TransactionRecord;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TransactionRepository
        extends JpaRepository<TransactionRecord, Long> {

    List<TransactionRecord> findByTableId(Long tableId);

    @Modifying
    @Transactional
    void deleteByTableId(Long tableId);
}
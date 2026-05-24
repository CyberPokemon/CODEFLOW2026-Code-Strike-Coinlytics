package com.coinlytics.backend.repository;

import com.coinlytics.backend.model.TransactionRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TransactionRepository
        extends JpaRepository<TransactionRecord, Long> {

    List<TransactionRecord> findByTableId(Long tableId);

    void deleteByTableId(Long tableId);
}
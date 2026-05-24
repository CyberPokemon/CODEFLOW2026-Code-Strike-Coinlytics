package com.coinlytics.backend.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

@Entity
@Table(name = "transactions")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TransactionRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long tableId;

    private Long slNo;

    private LocalDate txnDate;

    private String particulars;

    private Double credit;

    private Double debit;

    private Double balance;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private Users user;
}
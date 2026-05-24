package com.coinlytics.backend.dto;

import lombok.*;

import java.time.LocalDate;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class TransactionResponseDto {

    private Long slNo;

    private LocalDate txnDate;

    private String particulars;

    private Double credit;

    private Double debit;

    private Double balance;
}
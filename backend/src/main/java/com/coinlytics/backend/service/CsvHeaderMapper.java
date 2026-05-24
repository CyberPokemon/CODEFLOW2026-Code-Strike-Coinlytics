package com.coinlytics.backend.service;

import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class CsvHeaderMapper {

    private static final Map<String, String> mappings =
            Map.ofEntries(

                    // DATE
                    Map.entry("date", "DATE"),
                    Map.entry("transaction date", "DATE"),
                    Map.entry("txn date", "DATE"),
                    Map.entry("value date", "DATE"),

                    // PARTICULARS
                    Map.entry("particulars", "PARTICULARS"),
                    Map.entry("particulrs", "PARTICULARS"),
                    Map.entry("description", "PARTICULARS"),
                    Map.entry("particulrs/description", "PARTICULARS"),
                    Map.entry("narration", "PARTICULARS"),
                    Map.entry("remarks", "PARTICULARS"),

                    // CREDIT
                    Map.entry("credit", "CREDIT"),
                    Map.entry("credits", "CREDIT"),
                    Map.entry("deposit", "CREDIT"),
                    Map.entry("deposits", "CREDIT"),
                    Map.entry("deposits/credit", "CREDIT"),
                    Map.entry("cr", "CREDIT"),

                    // DEBIT
                    Map.entry("debit", "DEBIT"),
                    Map.entry("debits", "DEBIT"),
                    Map.entry("withdrawal", "DEBIT"),
                    Map.entry("withdrawals", "DEBIT"),
                    Map.entry("withdrawls/debit", "DEBIT"),
                    Map.entry("dr", "DEBIT"),

                    // BALANCE
                    Map.entry("balance", "BALANCE"),
                    Map.entry("closing balance", "BALANCE"),
                    Map.entry("available balance", "BALANCE")
            );

    public String normalize(String column) {

        if(column == null) {
            return null;
        }

        return mappings.getOrDefault(
                column
                        .trim()
                        .toLowerCase(),
                null
        );
    }
}
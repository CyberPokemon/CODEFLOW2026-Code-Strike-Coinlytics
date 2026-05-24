package com.coinlytics.backend.service;

import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class CsvHeaderMapper {

    private static final Map<String, String> mappings =
            Map.ofEntries(

                    Map.entry("date", "DATE"),
                    Map.entry("transaction date", "DATE"),
                    Map.entry("value date", "DATE"),

                    Map.entry("particulars", "PARTICULARS"),
                    Map.entry("description", "PARTICULARS"),
                    Map.entry("narration", "PARTICULARS"),

                    Map.entry("credit", "CREDIT"),
                    Map.entry("deposit", "CREDIT"),
                    Map.entry("cr", "CREDIT"),

                    Map.entry("debit", "DEBIT"),
                    Map.entry("withdrawal", "DEBIT"),
                    Map.entry("dr", "DEBIT"),

                    Map.entry("balance", "BALANCE"),
                    Map.entry("closing balance", "BALANCE")
            );

    public String normalize(String column) {

        return mappings.getOrDefault(
                column.trim().toLowerCase(),
                null
        );
    }
}
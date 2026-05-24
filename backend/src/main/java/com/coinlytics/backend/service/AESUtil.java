package com.coinlytics.backend.service;

import org.springframework.stereotype.Component;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.ByteArrayOutputStream;
import java.security.SecureRandom;
import java.util.Arrays;

@Component
public class AESUtil {

    private static final String AES = "AES/GCM/NoPadding";

    private static final byte[] KEY = "12345678901234567890123456789012".getBytes();

    public byte[] encrypt(byte[] data) throws Exception {

        Cipher cipher = Cipher.getInstance(AES);

        SecretKeySpec keySpec = new SecretKeySpec(KEY, "AES");

        byte[] iv = new byte[12];

        SecureRandom random = new SecureRandom();

        random.nextBytes(iv);

        GCMParameterSpec spec = new GCMParameterSpec(128, iv);

        cipher.init(Cipher.ENCRYPT_MODE, keySpec, spec);

        byte[] encrypted = cipher.doFinal(data);

        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();

        outputStream.write(iv);

        outputStream.write(encrypted);

        return outputStream.toByteArray();
    }

    public byte[] decrypt(byte[] encryptedData) throws Exception {

        byte[] iv = Arrays.copyOfRange(encryptedData, 0, 12);

        byte[] actualData = Arrays.copyOfRange(
                encryptedData,
                12,
                encryptedData.length
        );

        Cipher cipher = Cipher.getInstance(AES);

        SecretKeySpec keySpec = new SecretKeySpec(KEY, "AES");

        GCMParameterSpec spec = new GCMParameterSpec(128, iv);

        cipher.init(Cipher.DECRYPT_MODE, keySpec, spec);

        return cipher.doFinal(actualData);
    }
}
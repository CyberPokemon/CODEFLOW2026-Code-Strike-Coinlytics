package com.coinlytics.backend.service;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class AESUtil {

    private static final String ALGORITHM = "AES";

    // 16 bytes = 128-bit AES key
    private static final String SECRET = "1234567890123456";

    private static final SecretKey secretKey = new SecretKeySpec(SECRET.getBytes(), ALGORITHM);

    public static byte[] encrypt(byte[] data)
            throws Exception {

        Cipher cipher = Cipher.getInstance(ALGORITHM);

        cipher.init(Cipher.ENCRYPT_MODE, secretKey);

        return cipher.doFinal(data);
    }

    public static byte[] decrypt(byte[] encryptedData)
            throws Exception {

        Cipher cipher = Cipher.getInstance(ALGORITHM);

        cipher.init(Cipher.DECRYPT_MODE, secretKey);

        return cipher.doFinal(encryptedData);
    }
}
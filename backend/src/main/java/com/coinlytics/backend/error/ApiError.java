package com.coinlytics.backend.error;

import java.time.LocalDateTime;

public class ApiError {

    private LocalDateTime timestamp;
    private String error;
    private int statusCode;
    private String message;
    private String path;

    public ApiError(LocalDateTime timestamp, String error, int statusCode, String message, String path) {
        this.timestamp = timestamp;
        this.error = error;
        this.statusCode = statusCode;
        this.message = message;
        this.path = path;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public int getStatusCode() {
        return statusCode;
    }

    public void setStatusCode(int statusCode) {
        this.statusCode = statusCode;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }
}
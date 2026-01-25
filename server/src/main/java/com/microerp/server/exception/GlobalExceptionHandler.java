package com.microerp.server.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * 역할: API 예외를 일관된 응답으로 변환한다.
 * 책임: 검증/DB/일반 예외 처리.
 * 외부 의존성: Spring Web, Spring Validation.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    /**
     * 목적: ApiException을 처리한다.
     * Args:
     *  - exception: ApiException
     * Returns:
     *  - ResponseEntity<ErrorResponse>: 오류 응답
     * Side Effects:
     *  - 로그를 기록한다.
     * Raises: 없음
     */
    @ExceptionHandler(ApiException.class)
    public ResponseEntity<ErrorResponse> handleApiException(ApiException exception) {
        logger.warn("API error: {}", exception.getMessage());
        return ResponseEntity
            .status(exception.getStatus())
            .body(new ErrorResponse(exception.getMessage(), exception.getStatus().name()));
    }

    /**
     * 목적: 입력 검증 오류를 처리한다.
     * Args:
     *  - exception: MethodArgumentNotValidException
     * Returns:
     *  - ResponseEntity<ErrorResponse>: 오류 응답
     * Side Effects:
     *  - 로그를 기록한다.
     * Raises: 없음
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException exception) {
        String message = "Validation failed";
        FieldError fieldError = exception.getBindingResult().getFieldError();
        if (fieldError != null) {
            message = fieldError.getField() + ": " + fieldError.getDefaultMessage();
        }
        logger.warn("Validation error: {}", message);
        return ResponseEntity
            .status(HttpStatus.BAD_REQUEST)
            .body(new ErrorResponse(message, "VALIDATION_ERROR"));
    }

    /**
     * 목적: DB 접근 오류를 처리한다.
     * Args:
     *  - exception: DataAccessException
     * Returns:
     *  - ResponseEntity<ErrorResponse>: 오류 응답
     * Side Effects:
     *  - 로그를 기록한다.
     * Raises: 없음
     */
    @ExceptionHandler(DataAccessException.class)
    public ResponseEntity<ErrorResponse> handleDataAccessException(DataAccessException exception) {
        logger.error("Database error", exception);
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ErrorResponse("Database error", "DB_ERROR"));
    }

    /**
     * 목적: 기타 예외를 처리한다.
     * Args:
     *  - exception: Exception
     * Returns:
     *  - ResponseEntity<ErrorResponse>: 오류 응답
     * Side Effects:
     *  - 로그를 기록한다.
     * Raises: 없음
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpectedException(Exception exception) {
        logger.error("Unexpected error", exception);
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ErrorResponse("Unexpected error", "UNEXPECTED"));
    }
}

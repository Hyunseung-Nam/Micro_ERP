package com.microerp.server;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 역할: 서버 부팅 엔트리포인트를 제공한다.
 * 책임: Spring Boot 컨텍스트 초기화 및 실행.
 * 외부 의존성: Spring Boot.
 */
@SpringBootApplication
public class MicroErpServerApplication {
    private static final Logger logger = LoggerFactory.getLogger(MicroErpServerApplication.class);

    /**
     * 목적: 애플리케이션을 시작한다.
     * Args:
     *  - args: 실행 인자
     * Returns: 없음
     * Side Effects:
     *  - 애플리케이션 컨텍스트를 초기화한다.
     * Raises: 없음
     */
    public static void main(String[] args) {
        logger.info("Starting Micro ERP server");
        SpringApplication.run(MicroErpServerApplication.class, args);
    }
}

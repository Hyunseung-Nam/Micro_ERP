package com.microerp.server.service;

import com.microerp.server.dto.UserResponse;
import com.microerp.server.exception.ApiException;
import com.microerp.server.repository.UserRepository;
import java.util.List;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

/**
 * 역할: 사용자 조회 로직을 제공한다.
 * 책임: 사용자 목록 제공.
 * 외부 의존성: Spring Data JPA.
 */
@Service
public class UserService {
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * 목적: 사용자 목록을 조회한다.
     * Args: 없음
     * Returns:
     *  - List<UserResponse>: 사용자 목록
     * Side Effects:
     *  - 조회 로그를 기록한다.
     * Raises:
     *  - ApiException: DB 오류 발생 시
     */
    public List<UserResponse> getUsers() {
        try {
            logger.info("Loading user list");
            return userRepository.findAll().stream()
                .map(user -> new UserResponse(user.getUsername(), user.getRole(), user.getCreatedAt()))
                .collect(Collectors.toList());
        } catch (DataAccessException ex) {
            logger.error("Database error while fetching users", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }
}

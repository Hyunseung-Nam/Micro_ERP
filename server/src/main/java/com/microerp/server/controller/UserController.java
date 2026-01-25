package com.microerp.server.controller;

import com.microerp.server.dto.UserResponse;
import com.microerp.server.service.UserService;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 역할: 사용자 조회 API를 제공한다.
 * 책임: 사용자 목록 반환.
 * 외부 의존성: Spring Web.
 */
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    /**
     * 목적: 사용자 목록을 조회한다.
     * Args: 없음
     * Returns:
     *  - ResponseEntity<List<UserResponse>>: 사용자 목록
     * Side Effects: 없음
     * Raises: 없음
     */
    @GetMapping
    public ResponseEntity<List<UserResponse>> getUsers() {
        return ResponseEntity.ok(userService.getUsers());
    }
}

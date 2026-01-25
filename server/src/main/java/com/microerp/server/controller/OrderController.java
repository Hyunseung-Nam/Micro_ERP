package com.microerp.server.controller;

import com.microerp.server.dto.OrderCreateRequest;
import com.microerp.server.dto.OrderResponse;
import com.microerp.server.service.OrderService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 역할: 발주 API를 제공한다.
 * 책임: 발주 조회, 생성, 종결 엔드포인트 제공.
 * 외부 의존성: Spring Web.
 */
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    /**
     * 목적: 발주 목록을 조회한다.
     * Args: 없음
     * Returns:
     *  - ResponseEntity<List<OrderResponse>>: 발주 목록
     * Side Effects: 없음
     * Raises: 없음
     */
    @GetMapping
    public ResponseEntity<List<OrderResponse>> getOrders() {
        return ResponseEntity.ok(orderService.getOrders());
    }

    /**
     * 목적: 발주를 생성한다.
     * Args:
     *  - request: 발주 생성 요청
     * Returns:
     *  - ResponseEntity<OrderResponse>: 생성된 발주
     * Side Effects: 없음
     * Raises: 없음
     */
    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(@Valid @RequestBody OrderCreateRequest request) {
        return ResponseEntity.ok(orderService.createOrder(request));
    }

    /**
     * 목적: 발주를 종결한다.
     * Args:
     *  - orderId: 발주 ID
     * Returns:
     *  - ResponseEntity<OrderResponse>: 종결된 발주
     * Side Effects: 없음
     * Raises: 없음
     */
    @PostMapping("/{orderId}/close")
    public ResponseEntity<OrderResponse> closeOrder(@PathVariable Long orderId) {
        return ResponseEntity.ok(orderService.closeOrder(orderId));
    }
}

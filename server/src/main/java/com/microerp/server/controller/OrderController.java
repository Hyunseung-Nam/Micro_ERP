package com.microerp.server.controller;

import com.microerp.server.dto.OrderCreateRequest;
import com.microerp.server.dto.OrderResponse;
import com.microerp.server.service.OrderService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping
    @PreAuthorize("hasAuthority('SCOPE_order.read') or hasRole('ADMIN')")
    public ResponseEntity<List<OrderResponse>> getOrders() {
        return ResponseEntity.ok(orderService.getOrders());
    }

    @PostMapping
    @PreAuthorize("hasAuthority('SCOPE_order.create') or hasRole('ADMIN')")
    public ResponseEntity<OrderResponse> createOrder(
            @Valid @RequestBody OrderCreateRequest request,
            Authentication authentication
    ) {
        return ResponseEntity.ok(orderService.createOrder(request, authentication.getName()));
    }

    @PostMapping("/{orderId}/approve")
    @PreAuthorize("hasAuthority('SCOPE_approval.approve') or hasRole('ADMIN')")
    public ResponseEntity<OrderResponse> approveOrder(@PathVariable Long orderId, Authentication authentication) {
        return ResponseEntity.ok(orderService.approveOrder(orderId, authentication.getName()));
    }

    @PostMapping("/{orderId}/close")
    @PreAuthorize("hasAuthority('SCOPE_order.close') or hasRole('ADMIN')")
    public ResponseEntity<OrderResponse> closeOrder(@PathVariable Long orderId, Authentication authentication) {
        return ResponseEntity.ok(orderService.closeOrder(orderId, authentication.getName()));
    }
}

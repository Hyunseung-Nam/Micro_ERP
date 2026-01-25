package com.microerp.server.controller;

import com.microerp.server.dto.InventoryAdjustRequest;
import com.microerp.server.dto.InventoryItemResponse;
import com.microerp.server.service.InventoryService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 역할: 재고 API를 제공한다.
 * 책임: 재고 조회 및 조정 엔드포인트 제공.
 * 외부 의존성: Spring Web.
 */
@RestController
@RequestMapping("/api/inventory")
public class InventoryController {
    private final InventoryService inventoryService;

    public InventoryController(InventoryService inventoryService) {
        this.inventoryService = inventoryService;
    }

    /**
     * 목적: 재고 목록을 조회한다.
     * Args: 없음
     * Returns:
     *  - ResponseEntity<List<InventoryItemResponse>>: 재고 목록
     * Side Effects: 없음
     * Raises: 없음
     */
    @GetMapping
    public ResponseEntity<List<InventoryItemResponse>> getInventory() {
        return ResponseEntity.ok(inventoryService.getInventory());
    }

    /**
     * 목적: 재고 수량을 조정한다.
     * Args:
     *  - request: 재고 조정 요청
     * Returns:
     *  - ResponseEntity<InventoryItemResponse>: 조정된 재고
     * Side Effects: 없음
     * Raises: 없음
     */
    @PostMapping("/adjust")
    public ResponseEntity<InventoryItemResponse> adjustInventory(
            @Valid @RequestBody InventoryAdjustRequest request
    ) {
        return ResponseEntity.ok(inventoryService.adjustInventory(request));
    }
}

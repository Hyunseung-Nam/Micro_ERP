package com.microerp.server.controller;

import com.microerp.server.dto.InventoryAdjustRequest;
import com.microerp.server.dto.InventoryItemResponse;
import com.microerp.server.service.InventoryService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/inventory")
public class InventoryController {
    private final InventoryService inventoryService;

    public InventoryController(InventoryService inventoryService) {
        this.inventoryService = inventoryService;
    }

    @GetMapping
    @PreAuthorize("hasAuthority('SCOPE_inventory.read') or hasRole('ADMIN')")
    public ResponseEntity<List<InventoryItemResponse>> getInventory() {
        return ResponseEntity.ok(inventoryService.getInventory());
    }

    @PostMapping("/adjust")
    @PreAuthorize("hasAuthority('SCOPE_inventory.adjust') or hasRole('ADMIN')")
    public ResponseEntity<InventoryItemResponse> adjustInventory(
            @Valid @RequestBody InventoryAdjustRequest request,
            Authentication authentication
    ) {
        return ResponseEntity.ok(
            inventoryService.adjustInventory(request, authentication.getName(), "manual-adjust")
        );
    }
}

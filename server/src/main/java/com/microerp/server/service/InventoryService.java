package com.microerp.server.service;

import com.microerp.server.domain.Inventory;
import com.microerp.server.domain.InventoryId;
import com.microerp.server.domain.Item;
import com.microerp.server.domain.Location;
import com.microerp.server.dto.InventoryAdjustRequest;
import com.microerp.server.dto.InventoryItemResponse;
import com.microerp.server.exception.ApiException;
import com.microerp.server.repository.InventoryRepository;
import com.microerp.server.repository.ItemRepository;
import com.microerp.server.repository.LocationRepository;
import java.util.List;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class InventoryService {
    private static final Logger logger = LoggerFactory.getLogger(InventoryService.class);

    private final InventoryRepository inventoryRepository;
    private final ItemRepository itemRepository;
    private final LocationRepository locationRepository;
    private final AuditLogService auditLogService;

    public InventoryService(
            InventoryRepository inventoryRepository,
            ItemRepository itemRepository,
            LocationRepository locationRepository,
            AuditLogService auditLogService
    ) {
        this.inventoryRepository = inventoryRepository;
        this.itemRepository = itemRepository;
        this.locationRepository = locationRepository;
        this.auditLogService = auditLogService;
    }

    @Transactional(readOnly = true)
    public List<InventoryItemResponse> getInventory() {
        try {
            logger.info("Loading inventory list");
            return inventoryRepository.findAll().stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
        } catch (DataAccessException ex) {
            logger.error("Database error while fetching inventory", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }

    @Transactional
    public InventoryItemResponse adjustInventory(InventoryAdjustRequest request, String actor, String reason) {
        try {
            Item item = itemRepository.findById(request.getItemId())
                .orElseThrow(() -> new ApiException(HttpStatus.BAD_REQUEST, "Item not found"));
            Location location = locationRepository.findById(request.getLocationId())
                .orElseThrow(() -> new ApiException(HttpStatus.BAD_REQUEST, "Location not found"));

            InventoryId id = new InventoryId(item.getItemId(), location.getLocationId());
            Inventory inventory = inventoryRepository.findById(id)
                .orElseGet(() -> new Inventory(item, location, 0));

            int newQuantity = inventory.getQuantity() + request.getDeltaQuantity();
            if (newQuantity < 0) {
                throw new ApiException(HttpStatus.BAD_REQUEST, "Inventory cannot be negative");
            }
            inventory.setQuantity(newQuantity);
            Inventory saved = inventoryRepository.save(inventory);
            logger.info("Adjusted inventory for item {} at {}", item.getItemId(), location.getLocationId());
            auditLogService.log(
                actor,
                "INVENTORY_ADJUST",
                "INVENTORY",
                item.getItemId() + "@" + location.getLocationId(),
                "delta=" + request.getDeltaQuantity() + "; reason=" + (reason == null ? "" : reason)
            );
            return toResponse(saved);
        } catch (DataAccessException ex) {
            logger.error("Database error while adjusting inventory", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }

    private InventoryItemResponse toResponse(Inventory inventory) {
        Item item = inventory.getItem();
        Location location = inventory.getLocation();
        return new InventoryItemResponse(
            item.getItemId(),
            item.getName(),
            item.getUnit(),
            item.getSafetyStock(),
            location.getLocationId(),
            location.getName(),
            inventory.getQuantity()
        );
    }
}

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

/**
 * 역할: 재고 조회 및 조정 로직을 제공한다.
 * 책임: 재고 목록 조회, 수량 조정 처리.
 * 외부 의존성: Spring Data JPA.
 */
@Service
public class InventoryService {
    private static final Logger logger = LoggerFactory.getLogger(InventoryService.class);

    private final InventoryRepository inventoryRepository;
    private final ItemRepository itemRepository;
    private final LocationRepository locationRepository;

    public InventoryService(
            InventoryRepository inventoryRepository,
            ItemRepository itemRepository,
            LocationRepository locationRepository
    ) {
        this.inventoryRepository = inventoryRepository;
        this.itemRepository = itemRepository;
        this.locationRepository = locationRepository;
    }

    /**
     * 목적: 재고 목록을 조회한다.
     * Args: 없음
     * Returns:
     *  - List<InventoryItemResponse>: 재고 목록
     * Side Effects:
     *  - 조회 로그를 기록한다.
     * Raises:
     *  - ApiException: DB 오류 발생 시
     */
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

    /**
     * 목적: 재고 수량을 조정한다.
     * Args:
     *  - request: 재고 조정 요청
     * Returns:
     *  - InventoryItemResponse: 변경된 재고
     * Side Effects:
     *  - 재고를 저장한다.
     * Raises:
     *  - ApiException: 입력 오류 또는 DB 오류 발생 시
     */
    public InventoryItemResponse adjustInventory(InventoryAdjustRequest request) {
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
            return toResponse(saved);
        } catch (DataAccessException ex) {
            logger.error("Database error while adjusting inventory", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }

    /**
     * 목적: 재고 엔티티를 응답 DTO로 변환한다.
     * Args:
     *  - inventory: 재고 엔티티
     * Returns:
     *  - InventoryItemResponse: 응답 DTO
     * Side Effects: 없음
     * Raises: 없음
     */
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

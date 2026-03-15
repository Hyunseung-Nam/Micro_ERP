package com.microerp.server.service;

import com.microerp.server.dto.EcommerceReturnExchangeRequest;
import com.microerp.server.dto.HospitalConsumeRequest;
import com.microerp.server.dto.InventoryAdjustRequest;
import com.microerp.server.dto.InventoryItemResponse;
import com.microerp.server.exception.ApiException;
import java.util.ArrayList;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class WorkflowService {
    private final InventoryService inventoryService;
    private final AuditLogService auditLogService;

    public WorkflowService(InventoryService inventoryService, AuditLogService auditLogService) {
        this.inventoryService = inventoryService;
        this.auditLogService = auditLogService;
    }

    @Transactional
    public InventoryItemResponse hospitalConsume(HospitalConsumeRequest request, String actor) {
        InventoryAdjustRequest adjust = new InventoryAdjustRequest();
        adjust.setItemId(request.getItemId());
        adjust.setLocationId(request.getLocationId());
        adjust.setDeltaQuantity(-request.getQuantity());

        String reason = "hospital-consume department=" + request.getDepartment() + "; note=" + safe(request.getNote());
        InventoryItemResponse response = inventoryService.adjustInventory(adjust, actor, reason);
        auditLogService.log(actor, "WORKFLOW_HOSPITAL_CONSUME", "INVENTORY", request.getItemId(), reason);
        return response;
    }

    @Transactional
    public List<InventoryItemResponse> ecommerceReturnExchange(EcommerceReturnExchangeRequest request, String actor) {
        if (request.getExchangeQuantity() > request.getReturnQuantity()) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Exchange quantity cannot exceed return quantity");
        }

        List<InventoryItemResponse> results = new ArrayList<>();

        InventoryAdjustRequest addReturn = new InventoryAdjustRequest();
        addReturn.setItemId(request.getItemId());
        addReturn.setLocationId(request.getReturnLocationId());
        addReturn.setDeltaQuantity(request.getReturnQuantity());
        results.add(inventoryService.adjustInventory(
            addReturn,
            actor,
            "ecommerce-return orderNo=" + request.getMarketplaceOrderNo()
        ));

        if (request.getExchangeQuantity() > 0) {
            InventoryAdjustRequest shipExchange = new InventoryAdjustRequest();
            shipExchange.setItemId(request.getItemId());
            shipExchange.setLocationId(request.getShipLocationId());
            shipExchange.setDeltaQuantity(-request.getExchangeQuantity());
            results.add(inventoryService.adjustInventory(
                shipExchange,
                actor,
                "ecommerce-exchange orderNo=" + request.getMarketplaceOrderNo()
            ));
        }

        auditLogService.log(
            actor,
            "WORKFLOW_ECOMMERCE_RETURN_EXCHANGE",
            "ORDER",
            request.getMarketplaceOrderNo(),
            "item=" + request.getItemId() + "; return=" + request.getReturnQuantity() + "; exchange=" + request.getExchangeQuantity()
        );
        return results;
    }

    private String safe(String value) {
        return value == null ? "" : value;
    }
}

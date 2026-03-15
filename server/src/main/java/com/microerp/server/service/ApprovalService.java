package com.microerp.server.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.microerp.server.domain.ApprovalRequest;
import com.microerp.server.domain.User;
import com.microerp.server.dto.ApprovalRequestCreateRequest;
import com.microerp.server.dto.ApprovalRequestResponse;
import com.microerp.server.dto.InventoryAdjustRequest;
import com.microerp.server.exception.ApiException;
import com.microerp.server.repository.ApprovalRequestRepository;
import com.microerp.server.repository.UserRepository;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ApprovalService {
    public static final String REQUEST_TYPE_INVENTORY_ADJUST = "INVENTORY_ADJUST";
    public static final String REQUEST_TYPE_ORDER_CLOSE = "ORDER_CLOSE";

    private final ApprovalRequestRepository approvalRequestRepository;
    private final UserRepository userRepository;
    private final InventoryService inventoryService;
    private final OrderService orderService;
    private final AuditLogService auditLogService;
    private final ObjectMapper objectMapper;

    public ApprovalService(
            ApprovalRequestRepository approvalRequestRepository,
            UserRepository userRepository,
            InventoryService inventoryService,
            OrderService orderService,
            AuditLogService auditLogService,
            ObjectMapper objectMapper
    ) {
        this.approvalRequestRepository = approvalRequestRepository;
        this.userRepository = userRepository;
        this.inventoryService = inventoryService;
        this.orderService = orderService;
        this.auditLogService = auditLogService;
        this.objectMapper = objectMapper;
    }

    @Transactional(readOnly = true)
    public List<ApprovalRequestResponse> getApprovals(String status) {
        List<ApprovalRequest> approvals;
        if (status == null || status.isBlank()) {
            approvals = approvalRequestRepository.findAll();
        } else {
            approvals = approvalRequestRepository.findByStatusOrderByCreatedAtDesc(status.trim().toUpperCase());
        }
        return approvals.stream().map(this::toResponse).toList();
    }

    @Transactional
    public ApprovalRequestResponse requestApproval(ApprovalRequestCreateRequest request, String actor) {
        User requestedBy = userRepository.findById(actor)
            .orElseThrow(() -> new ApiException(HttpStatus.BAD_REQUEST, "User not found"));
        ApprovalRequest approval = new ApprovalRequest(
            request.getRequestType().trim().toUpperCase(),
            request.getRequestPayload(),
            requestedBy
        );
        ApprovalRequest saved = approvalRequestRepository.save(approval);
        auditLogService.log(actor, "APPROVAL_REQUEST", "APPROVAL", String.valueOf(saved.getId()), saved.getRequestType());
        return toResponse(saved);
    }

    @Transactional
    public ApprovalRequestResponse approve(Long approvalId, String actor) {
        ApprovalRequest approval = approvalRequestRepository.findById(approvalId)
            .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "Approval request not found"));
        if (!"PENDING".equals(approval.getStatus())) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Approval request already processed");
        }

        executeApproval(approval, actor);
        User approver = userRepository.findById(actor)
            .orElseThrow(() -> new ApiException(HttpStatus.BAD_REQUEST, "User not found"));

        approval.setStatus("APPROVED");
        approval.setApprovedBy(approver);
        approval.setProcessedAt(Instant.now());
        ApprovalRequest saved = approvalRequestRepository.save(approval);
        auditLogService.log(actor, "APPROVAL_APPROVE", "APPROVAL", String.valueOf(saved.getId()), saved.getRequestType());
        return toResponse(saved);
    }

    @Transactional
    public ApprovalRequestResponse reject(Long approvalId, String actor, String reason) {
        ApprovalRequest approval = approvalRequestRepository.findById(approvalId)
            .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "Approval request not found"));
        if (!"PENDING".equals(approval.getStatus())) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Approval request already processed");
        }
        User approver = userRepository.findById(actor)
            .orElseThrow(() -> new ApiException(HttpStatus.BAD_REQUEST, "User not found"));

        approval.setStatus("REJECTED");
        approval.setApprovedBy(approver);
        approval.setRejectReason(reason);
        approval.setProcessedAt(Instant.now());
        ApprovalRequest saved = approvalRequestRepository.save(approval);
        auditLogService.log(actor, "APPROVAL_REJECT", "APPROVAL", String.valueOf(saved.getId()), reason);
        return toResponse(saved);
    }

    private void executeApproval(ApprovalRequest approval, String actor) {
        try {
            String type = approval.getRequestType();
            if (REQUEST_TYPE_INVENTORY_ADJUST.equals(type)) {
                Map<String, Object> payload = objectMapper.readValue(
                    approval.getRequestPayload(),
                    new TypeReference<Map<String, Object>>() {}
                );
                InventoryAdjustRequest request = new InventoryAdjustRequest();
                request.setItemId((String) payload.get("itemId"));
                request.setLocationId((String) payload.get("locationId"));
                Number delta = (Number) payload.get("deltaQuantity");
                request.setDeltaQuantity(delta == null ? 0 : delta.intValue());
                String reason = payload.get("reason") == null ? "approval-executed" : payload.get("reason").toString();
                inventoryService.adjustInventory(request, actor, reason);
                return;
            }
            if (REQUEST_TYPE_ORDER_CLOSE.equals(type)) {
                Map<String, Object> payload = objectMapper.readValue(
                    approval.getRequestPayload(),
                    new TypeReference<Map<String, Object>>() {}
                );
                Number orderId = (Number) payload.get("orderId");
                if (orderId == null) {
                    throw new ApiException(HttpStatus.BAD_REQUEST, "Invalid order close payload");
                }
                orderService.closeOrder(orderId.longValue(), actor);
                return;
            }
            throw new ApiException(HttpStatus.BAD_REQUEST, "Unsupported request type: " + type);
        } catch (ApiException ex) {
            throw ex;
        } catch (Exception ex) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Invalid request payload");
        }
    }

    private ApprovalRequestResponse toResponse(ApprovalRequest approval) {
        return new ApprovalRequestResponse(
            approval.getId(),
            approval.getRequestType(),
            approval.getRequestPayload(),
            approval.getStatus(),
            approval.getRequestedBy().getUsername(),
            approval.getApprovedBy() == null ? null : approval.getApprovedBy().getUsername(),
            approval.getRejectReason(),
            approval.getCreatedAt(),
            approval.getProcessedAt()
        );
    }
}

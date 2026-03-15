package com.microerp.server.controller;

import com.microerp.server.dto.ApprovalActionRequest;
import com.microerp.server.dto.ApprovalRequestCreateRequest;
import com.microerp.server.dto.ApprovalRequestResponse;
import com.microerp.server.service.ApprovalService;
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
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/approvals")
public class ApprovalController {
    private final ApprovalService approvalService;

    public ApprovalController(ApprovalService approvalService) {
        this.approvalService = approvalService;
    }

    @GetMapping
    @PreAuthorize("hasAuthority('SCOPE_approval.read') or hasRole('ADMIN')")
    public ResponseEntity<List<ApprovalRequestResponse>> getApprovals(@RequestParam(required = false) String status) {
        return ResponseEntity.ok(approvalService.getApprovals(status));
    }

    @PostMapping
    @PreAuthorize("hasAuthority('SCOPE_approval.request') or hasRole('ADMIN')")
    public ResponseEntity<ApprovalRequestResponse> createApproval(
            @Valid @RequestBody ApprovalRequestCreateRequest request,
            Authentication authentication
    ) {
        return ResponseEntity.ok(approvalService.requestApproval(request, authentication.getName()));
    }

    @PostMapping("/{approvalId}/approve")
    @PreAuthorize("hasAuthority('SCOPE_approval.approve') or hasRole('ADMIN')")
    public ResponseEntity<ApprovalRequestResponse> approve(
            @PathVariable Long approvalId,
            Authentication authentication
    ) {
        return ResponseEntity.ok(approvalService.approve(approvalId, authentication.getName()));
    }

    @PostMapping("/{approvalId}/reject")
    @PreAuthorize("hasAuthority('SCOPE_approval.reject') or hasRole('ADMIN')")
    public ResponseEntity<ApprovalRequestResponse> reject(
            @PathVariable Long approvalId,
            @RequestBody(required = false) ApprovalActionRequest request,
            Authentication authentication
    ) {
        String reason = request == null ? "" : request.getReason();
        return ResponseEntity.ok(approvalService.reject(approvalId, authentication.getName(), reason));
    }
}

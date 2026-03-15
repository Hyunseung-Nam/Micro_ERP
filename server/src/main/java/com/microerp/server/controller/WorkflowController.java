package com.microerp.server.controller;

import com.microerp.server.dto.EcommerceReturnExchangeRequest;
import com.microerp.server.dto.HospitalConsumeRequest;
import com.microerp.server.dto.InventoryItemResponse;
import com.microerp.server.service.WorkflowService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/workflows")
public class WorkflowController {
    private final WorkflowService workflowService;

    public WorkflowController(WorkflowService workflowService) {
        this.workflowService = workflowService;
    }

    @PostMapping("/hospital/consume")
    @PreAuthorize("hasAuthority('SCOPE_workflow.hospital.consume') or hasRole('ADMIN')")
    public ResponseEntity<InventoryItemResponse> hospitalConsume(
            @Valid @RequestBody HospitalConsumeRequest request,
            Authentication authentication
    ) {
        return ResponseEntity.ok(workflowService.hospitalConsume(request, authentication.getName()));
    }

    @PostMapping("/ecommerce/return-exchange")
    @PreAuthorize("hasAuthority('SCOPE_workflow.ecommerce.exchange') or hasRole('ADMIN')")
    public ResponseEntity<List<InventoryItemResponse>> ecommerceReturnExchange(
            @Valid @RequestBody EcommerceReturnExchangeRequest request,
            Authentication authentication
    ) {
        return ResponseEntity.ok(workflowService.ecommerceReturnExchange(request, authentication.getName()));
    }
}

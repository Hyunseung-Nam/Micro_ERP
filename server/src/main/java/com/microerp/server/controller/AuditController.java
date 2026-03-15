package com.microerp.server.controller;

import com.microerp.server.dto.AuditLogResponse;
import com.microerp.server.service.AuditLogService;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/audit")
public class AuditController {
    private final AuditLogService auditLogService;

    public AuditController(AuditLogService auditLogService) {
        this.auditLogService = auditLogService;
    }

    @GetMapping("/logs")
    @PreAuthorize("hasAuthority('SCOPE_audit.read') or hasRole('ADMIN')")
    public ResponseEntity<List<AuditLogResponse>> recentLogs() {
        return ResponseEntity.ok(auditLogService.recentLogs());
    }
}

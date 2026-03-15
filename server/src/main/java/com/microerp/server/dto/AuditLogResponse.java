package com.microerp.server.dto;

import java.time.Instant;

public class AuditLogResponse {
    private Long auditId;
    private String username;
    private String action;
    private String targetType;
    private String targetId;
    private String detail;
    private Instant createdAt;

    public AuditLogResponse() {
    }

    public AuditLogResponse(
            Long auditId,
            String username,
            String action,
            String targetType,
            String targetId,
            String detail,
            Instant createdAt
    ) {
        this.auditId = auditId;
        this.username = username;
        this.action = action;
        this.targetType = targetType;
        this.targetId = targetId;
        this.detail = detail;
        this.createdAt = createdAt;
    }

    public Long getAuditId() { return auditId; }
    public void setAuditId(Long auditId) { this.auditId = auditId; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getAction() { return action; }
    public void setAction(String action) { this.action = action; }
    public String getTargetType() { return targetType; }
    public void setTargetType(String targetType) { this.targetType = targetType; }
    public String getTargetId() { return targetId; }
    public void setTargetId(String targetId) { this.targetId = targetId; }
    public String getDetail() { return detail; }
    public void setDetail(String detail) { this.detail = detail; }
    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
}

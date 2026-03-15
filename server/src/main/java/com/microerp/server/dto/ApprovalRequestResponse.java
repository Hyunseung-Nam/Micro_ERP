package com.microerp.server.dto;

import java.time.Instant;

public class ApprovalRequestResponse {
    private Long approvalId;
    private String requestType;
    private String requestPayload;
    private String status;
    private String requestedBy;
    private String approvedBy;
    private String rejectReason;
    private Instant createdAt;
    private Instant processedAt;

    public ApprovalRequestResponse() {
    }

    public ApprovalRequestResponse(
            Long approvalId,
            String requestType,
            String requestPayload,
            String status,
            String requestedBy,
            String approvedBy,
            String rejectReason,
            Instant createdAt,
            Instant processedAt
    ) {
        this.approvalId = approvalId;
        this.requestType = requestType;
        this.requestPayload = requestPayload;
        this.status = status;
        this.requestedBy = requestedBy;
        this.approvedBy = approvedBy;
        this.rejectReason = rejectReason;
        this.createdAt = createdAt;
        this.processedAt = processedAt;
    }

    public Long getApprovalId() { return approvalId; }
    public void setApprovalId(Long approvalId) { this.approvalId = approvalId; }
    public String getRequestType() { return requestType; }
    public void setRequestType(String requestType) { this.requestType = requestType; }
    public String getRequestPayload() { return requestPayload; }
    public void setRequestPayload(String requestPayload) { this.requestPayload = requestPayload; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getRequestedBy() { return requestedBy; }
    public void setRequestedBy(String requestedBy) { this.requestedBy = requestedBy; }
    public String getApprovedBy() { return approvedBy; }
    public void setApprovedBy(String approvedBy) { this.approvedBy = approvedBy; }
    public String getRejectReason() { return rejectReason; }
    public void setRejectReason(String rejectReason) { this.rejectReason = rejectReason; }
    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
    public Instant getProcessedAt() { return processedAt; }
    public void setProcessedAt(Instant processedAt) { this.processedAt = processedAt; }
}

package com.microerp.server.dto;

import jakarta.validation.constraints.NotBlank;

public class ApprovalRequestCreateRequest {
    @NotBlank
    private String requestType;

    @NotBlank
    private String requestPayload;

    public ApprovalRequestCreateRequest() {
    }

    public String getRequestType() {
        return requestType;
    }

    public void setRequestType(String requestType) {
        this.requestType = requestType;
    }

    public String getRequestPayload() {
        return requestPayload;
    }

    public void setRequestPayload(String requestPayload) {
        this.requestPayload = requestPayload;
    }
}

package com.microerp.server.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

public class HospitalConsumeRequest {
    @NotBlank
    private String itemId;

    @NotBlank
    private String locationId;

    @Min(1)
    private int quantity;

    @NotBlank
    private String department;

    private String note;

    public HospitalConsumeRequest() {
    }

    public String getItemId() { return itemId; }
    public void setItemId(String itemId) { this.itemId = itemId; }
    public String getLocationId() { return locationId; }
    public void setLocationId(String locationId) { this.locationId = locationId; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
    public String getDepartment() { return department; }
    public void setDepartment(String department) { this.department = department; }
    public String getNote() { return note; }
    public void setNote(String note) { this.note = note; }
}

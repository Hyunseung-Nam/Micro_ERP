package com.microerp.server.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

public class EcommerceReturnExchangeRequest {
    @NotBlank
    private String itemId;

    @NotBlank
    private String returnLocationId;

    @NotBlank
    private String shipLocationId;

    @Min(1)
    private int returnQuantity;

    @Min(0)
    private int exchangeQuantity;

    @NotBlank
    private String marketplaceOrderNo;

    public EcommerceReturnExchangeRequest() {
    }

    public String getItemId() { return itemId; }
    public void setItemId(String itemId) { this.itemId = itemId; }
    public String getReturnLocationId() { return returnLocationId; }
    public void setReturnLocationId(String returnLocationId) { this.returnLocationId = returnLocationId; }
    public String getShipLocationId() { return shipLocationId; }
    public void setShipLocationId(String shipLocationId) { this.shipLocationId = shipLocationId; }
    public int getReturnQuantity() { return returnQuantity; }
    public void setReturnQuantity(int returnQuantity) { this.returnQuantity = returnQuantity; }
    public int getExchangeQuantity() { return exchangeQuantity; }
    public void setExchangeQuantity(int exchangeQuantity) { this.exchangeQuantity = exchangeQuantity; }
    public String getMarketplaceOrderNo() { return marketplaceOrderNo; }
    public void setMarketplaceOrderNo(String marketplaceOrderNo) { this.marketplaceOrderNo = marketplaceOrderNo; }
}

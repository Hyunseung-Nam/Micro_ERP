package com.microerp.server.dto;

import java.util.ArrayList;
import java.util.List;

public class CurrentUserResponse {
    private String username;
    private String role;
    private List<String> scopes = new ArrayList<>();

    public CurrentUserResponse() {
    }

    public CurrentUserResponse(String username, String role, List<String> scopes) {
        this.username = username;
        this.role = role;
        this.scopes = scopes;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public List<String> getScopes() {
        return scopes;
    }

    public void setScopes(List<String> scopes) {
        this.scopes = scopes;
    }
}

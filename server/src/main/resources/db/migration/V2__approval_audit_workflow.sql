CREATE TABLE IF NOT EXISTS approval_requests (
    approval_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    request_type VARCHAR(50) NOT NULL,
    request_payload TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    requested_by VARCHAR(50) NOT NULL,
    approved_by VARCHAR(50) NULL,
    reject_reason VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP NULL,
    CONSTRAINT fk_approval_requested_by FOREIGN KEY (requested_by) REFERENCES users(username),
    CONSTRAINT fk_approval_approved_by FOREIGN KEY (approved_by) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    audit_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    target_type VARCHAR(50) NOT NULL,
    target_id VARCHAR(100) NULL,
    detail VARCHAR(500) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_username FOREIGN KEY (username) REFERENCES users(username)
);

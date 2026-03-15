package com.microerp.server.service;

import com.microerp.server.domain.AuditLog;
import com.microerp.server.domain.User;
import com.microerp.server.dto.AuditLogResponse;
import com.microerp.server.repository.AuditLogRepository;
import com.microerp.server.repository.UserRepository;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuditLogService {
    private final AuditLogRepository auditLogRepository;
    private final UserRepository userRepository;

    public AuditLogService(AuditLogRepository auditLogRepository, UserRepository userRepository) {
        this.auditLogRepository = auditLogRepository;
        this.userRepository = userRepository;
    }

    public void log(String username, String action, String targetType, String targetId, String detail) {
        if (username == null || username.isBlank()) {
            return;
        }
        User user = userRepository.findById(username).orElse(null);
        if (user == null) {
            return;
        }
        auditLogRepository.save(new AuditLog(user, action, targetType, targetId, detail));
    }

    @Transactional(readOnly = true)
    public List<AuditLogResponse> recentLogs() {
        return auditLogRepository.findTop100ByOrderByCreatedAtDesc().stream()
            .map(log -> new AuditLogResponse(
                log.getId(),
                log.getUser().getUsername(),
                log.getAction(),
                log.getTargetType(),
                log.getTargetId(),
                log.getDetail(),
                log.getCreatedAt()
            ))
            .toList();
    }
}

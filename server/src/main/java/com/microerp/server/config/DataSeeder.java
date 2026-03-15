package com.microerp.server.config;

import com.microerp.server.domain.Inventory;
import com.microerp.server.domain.Item;
import com.microerp.server.domain.Location;
import com.microerp.server.domain.Partner;
import com.microerp.server.domain.User;
import com.microerp.server.repository.InventoryRepository;
import com.microerp.server.repository.ItemRepository;
import com.microerp.server.repository.LocationRepository;
import com.microerp.server.repository.PartnerRepository;
import com.microerp.server.repository.UserRepository;
import java.util.Optional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.dao.DataAccessException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * 역할: 로컬 테스트용 초기 데이터를 시드한다.
 * 책임: 기본 사용자/품목/위치/거래처 데이터 생성.
 * 외부 의존성: Spring Data JPA, Spring Security.
 */
@Component
public class DataSeeder implements ApplicationRunner {
    private static final Logger logger = LoggerFactory.getLogger(DataSeeder.class);

    private final UserRepository userRepository;
    private final ItemRepository itemRepository;
    private final LocationRepository locationRepository;
    private final PartnerRepository partnerRepository;
    private final InventoryRepository inventoryRepository;
    private final PasswordEncoder passwordEncoder;
    private final String adminUsername;
    private final String adminPassword;

    public DataSeeder(
            UserRepository userRepository,
            ItemRepository itemRepository,
            LocationRepository locationRepository,
            PartnerRepository partnerRepository,
            InventoryRepository inventoryRepository,
            PasswordEncoder passwordEncoder,
            @Value("${app.seed.admin-username:admin}") String adminUsername,
            @Value("${app.seed.admin-password:admin123}") String adminPassword
    ) {
        this.userRepository = userRepository;
        this.itemRepository = itemRepository;
        this.locationRepository = locationRepository;
        this.partnerRepository = partnerRepository;
        this.inventoryRepository = inventoryRepository;
        this.passwordEncoder = passwordEncoder;
        this.adminUsername = adminUsername;
        this.adminPassword = adminPassword;
    }

    /**
     * 목적: 애플리케이션 시작 시 초기 데이터를 생성한다.
     * Args:
     *  - args: 실행 인자
     * Returns: 없음
     * Side Effects:
     *  - DB에 기본 레코드를 삽입한다.
     * Raises: 없음
     */
    @Override
    public void run(ApplicationArguments args) {
        try {
            seedAdminUser();
            seedReferenceData();
        } catch (DataAccessException ex) {
            logger.error("Failed to seed data", ex);
        }
    }

    private void seedAdminUser() {
        Optional<User> existing = userRepository.findById(adminUsername);
        if (existing.isPresent()) {
            seedDefaultUsers();
            return;
        }
        String hashed = passwordEncoder.encode(adminPassword);
        userRepository.save(new User(adminUsername, hashed, "ADMIN"));
        logger.info("Seeded admin user {}", adminUsername);
        seedDefaultUsers();
    }

    private void seedDefaultUsers() {
        seedUserIfMissing("manager", "manager123", "MANAGER");
        seedUserIfMissing("staff", "staff123", "STAFF");
        seedUserIfMissing("auditor", "auditor123", "AUDITOR");
    }

    private void seedUserIfMissing(String username, String rawPassword, String role) {
        if (userRepository.findById(username).isPresent()) {
            return;
        }
        userRepository.save(new User(username, passwordEncoder.encode(rawPassword), role));
        logger.info("Seeded {} user {}", role, username);
    }

    private void seedReferenceData() {
        if (itemRepository.count() == 0) {
            itemRepository.save(new Item("ITEM-001", "Sample Item", "EA", 10));
        }
        if (locationRepository.count() == 0) {
            locationRepository.save(new Location("LOC-001", "Main Warehouse"));
        }
        if (partnerRepository.count() == 0) {
            partnerRepository.save(new Partner("PARTNER-001", "Sample Supplier", "SUPPLIER"));
        }

        Item item = itemRepository.findById("ITEM-001").orElse(null);
        Location location = locationRepository.findById("LOC-001").orElse(null);
        if (item != null && location != null && inventoryRepository.count() == 0) {
            inventoryRepository.save(new Inventory(item, location, 100));
        }
    }
}

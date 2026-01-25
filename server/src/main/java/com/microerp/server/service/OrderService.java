package com.microerp.server.service;

import com.microerp.server.domain.Item;
import com.microerp.server.domain.Order;
import com.microerp.server.domain.OrderLine;
import com.microerp.server.domain.Partner;
import com.microerp.server.dto.OrderCreateRequest;
import com.microerp.server.dto.OrderLineResponse;
import com.microerp.server.dto.OrderResponse;
import com.microerp.server.exception.ApiException;
import com.microerp.server.repository.ItemRepository;
import com.microerp.server.repository.OrderRepository;
import com.microerp.server.repository.PartnerRepository;
import java.util.List;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

/**
 * 역할: 발주 처리 로직을 제공한다.
 * 책임: 발주 생성, 조회, 종결 처리.
 * 외부 의존성: Spring Data JPA.
 */
@Service
public class OrderService {
    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);

    private final OrderRepository orderRepository;
    private final PartnerRepository partnerRepository;
    private final ItemRepository itemRepository;

    public OrderService(
            OrderRepository orderRepository,
            PartnerRepository partnerRepository,
            ItemRepository itemRepository
    ) {
        this.orderRepository = orderRepository;
        this.partnerRepository = partnerRepository;
        this.itemRepository = itemRepository;
    }

    /**
     * 목적: 발주 목록을 조회한다.
     * Args: 없음
     * Returns:
     *  - List<OrderResponse>: 발주 목록
     * Side Effects:
     *  - 조회 로그를 기록한다.
     * Raises:
     *  - ApiException: DB 오류 발생 시
     */
    public List<OrderResponse> getOrders() {
        try {
            logger.info("Loading orders");
            return orderRepository.findAll().stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
        } catch (DataAccessException ex) {
            logger.error("Database error while fetching orders", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }

    /**
     * 목적: 발주를 생성한다.
     * Args:
     *  - request: 발주 생성 요청
     * Returns:
     *  - OrderResponse: 생성된 발주
     * Side Effects:
     *  - 발주와 라인을 저장한다.
     * Raises:
     *  - ApiException: 입력 오류 또는 DB 오류 발생 시
     */
    public OrderResponse createOrder(OrderCreateRequest request) {
        try {
            Partner partner = partnerRepository.findById(request.getPartnerId())
                .orElseThrow(() -> new ApiException(HttpStatus.BAD_REQUEST, "Partner not found"));

            Order order = new Order(partner, "OPEN");
            request.getLines().forEach(line -> {
                Item item = itemRepository.findById(line.getItemId())
                    .orElseThrow(() -> new ApiException(HttpStatus.BAD_REQUEST, "Item not found"));
                OrderLine orderLine = new OrderLine(item, line.getQuantity(), line.getUnit());
                order.addLine(orderLine);
            });

            Order saved = orderRepository.save(order);
            logger.info("Created order {}", saved.getId());
            return toResponse(saved);
        } catch (DataAccessException ex) {
            logger.error("Database error while creating order", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }

    /**
     * 목적: 발주를 종결한다.
     * Args:
     *  - orderId: 발주 ID
     * Returns:
     *  - OrderResponse: 종결된 발주
     * Side Effects:
     *  - 발주 상태를 갱신한다.
     * Raises:
     *  - ApiException: 발주 없음 또는 DB 오류 발생 시
     */
    public OrderResponse closeOrder(Long orderId) {
        try {
            Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "Order not found"));
            order.setStatus("CLOSED");
            Order saved = orderRepository.save(order);
            logger.info("Closed order {}", orderId);
            return toResponse(saved);
        } catch (DataAccessException ex) {
            logger.error("Database error while closing order", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }

    /**
     * 목적: 발주 엔티티를 응답 DTO로 변환한다.
     * Args:
     *  - order: 발주 엔티티
     * Returns:
     *  - OrderResponse: 응답 DTO
     * Side Effects: 없음
     * Raises: 없음
     */
    private OrderResponse toResponse(Order order) {
        List<OrderLineResponse> lines = order.getLines().stream()
            .map(line -> new OrderLineResponse(
                line.getItem().getItemId(),
                line.getItem().getName(),
                line.getQuantity(),
                line.getUnit()
            ))
            .collect(Collectors.toList());

        return new OrderResponse(
            order.getId(),
            order.getPartner().getPartnerId(),
            order.getPartner().getName(),
            order.getStatus(),
            order.getCreatedAt(),
            lines
        );
    }
}

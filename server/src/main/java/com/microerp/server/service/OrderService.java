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
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderService {
    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);

    private final OrderRepository orderRepository;
    private final PartnerRepository partnerRepository;
    private final ItemRepository itemRepository;
    private final AuditLogService auditLogService;

    public OrderService(
            OrderRepository orderRepository,
            PartnerRepository partnerRepository,
            ItemRepository itemRepository,
            AuditLogService auditLogService
    ) {
        this.orderRepository = orderRepository;
        this.partnerRepository = partnerRepository;
        this.itemRepository = itemRepository;
        this.auditLogService = auditLogService;
    }

    @Transactional(readOnly = true)
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

    @Transactional
    public OrderResponse createOrder(OrderCreateRequest request, String actor) {
        try {
            Partner partner = partnerRepository.findById(request.getPartnerId())
                .orElseThrow(() -> new ApiException(HttpStatus.BAD_REQUEST, "Partner not found"));

            Order order = new Order(partner, "SUBMITTED");
            request.getLines().forEach(line -> {
                Item item = itemRepository.findById(line.getItemId())
                    .orElseThrow(() -> new ApiException(HttpStatus.BAD_REQUEST, "Item not found"));
                OrderLine orderLine = new OrderLine(item, line.getQuantity(), line.getUnit());
                order.addLine(orderLine);
            });

            Order saved = orderRepository.save(order);
            logger.info("Created order {}", saved.getId());
            auditLogService.log(actor, "ORDER_CREATE", "ORDER", String.valueOf(saved.getId()), "status=SUBMITTED");
            return toResponse(saved);
        } catch (DataAccessException ex) {
            logger.error("Database error while creating order", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }

    @Transactional
    public OrderResponse approveOrder(Long orderId, String actor) {
        Order order = findOrder(orderId);
        order.setStatus("APPROVED");
        Order saved = orderRepository.save(order);
        auditLogService.log(actor, "ORDER_APPROVE", "ORDER", String.valueOf(orderId), "status=APPROVED");
        return toResponse(saved);
    }

    @Transactional
    public OrderResponse closeOrder(Long orderId, String actor) {
        try {
            Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "Order not found"));
            if (!("APPROVED".equals(order.getStatus()) || "SUBMITTED".equals(order.getStatus()))) {
                throw new ApiException(HttpStatus.BAD_REQUEST, "Order must be APPROVED or SUBMITTED to close");
            }
            order.setStatus("CLOSED");
            Order saved = orderRepository.save(order);
            logger.info("Closed order {}", orderId);
            auditLogService.log(actor, "ORDER_CLOSE", "ORDER", String.valueOf(orderId), "status=CLOSED");
            return toResponse(saved);
        } catch (DataAccessException ex) {
            logger.error("Database error while closing order", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }

    private Order findOrder(Long orderId) {
        try {
            return orderRepository.findById(orderId)
                .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "Order not found"));
        } catch (DataAccessException ex) {
            logger.error("Database error while loading order", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }

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

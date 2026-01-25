package com.microerp.server.domain;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

/**
 * 역할: 발주 정보를 표현한다.
 * 책임: 거래처, 상태, 라인 정보 보관.
 * 외부 의존성: JPA.
 */
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "order_id")
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "partner_id")
    private Partner partner;

    @Column(name = "status", nullable = false, length = 20)
    private String status;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderLine> lines = new ArrayList<>();

    /**
     * 목적: JPA 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public Order() {
        this.createdAt = Instant.now();
    }

    /**
     * 목적: 발주 객체를 생성한다.
     * Args:
     *  - partner: 거래처
     *  - status: 상태
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public Order(Partner partner, String status) {
        this.partner = partner;
        this.status = status;
        this.createdAt = Instant.now();
    }

    /**
     * 목적: 발주 ID를 반환한다.
     * Args: 없음
     * Returns:
     *  - Long: 발주 ID
     * Side Effects: 없음
     * Raises: 없음
     */
    public Long getId() {
        return id;
    }

    /**
     * 목적: 발주 ID를 설정한다.
     * Args:
     *  - id: 발주 ID
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setId(Long id) {
        this.id = id;
    }

    /**
     * 목적: 거래처를 반환한다.
     * Args: 없음
     * Returns:
     *  - Partner: 거래처
     * Side Effects: 없음
     * Raises: 없음
     */
    public Partner getPartner() {
        return partner;
    }

    /**
     * 목적: 거래처를 설정한다.
     * Args:
     *  - partner: 거래처
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setPartner(Partner partner) {
        this.partner = partner;
    }

    /**
     * 목적: 상태를 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 상태
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getStatus() {
        return status;
    }

    /**
     * 목적: 상태를 설정한다.
     * Args:
     *  - status: 상태
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setStatus(String status) {
        this.status = status;
    }

    /**
     * 목적: 생성 시각을 반환한다.
     * Args: 없음
     * Returns:
     *  - Instant: 생성 시각
     * Side Effects: 없음
     * Raises: 없음
     */
    public Instant getCreatedAt() {
        return createdAt;
    }

    /**
     * 목적: 생성 시각을 설정한다.
     * Args:
     *  - createdAt: 생성 시각
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }

    /**
     * 목적: 발주 라인 목록을 반환한다.
     * Args: 없음
     * Returns:
     *  - List<OrderLine>: 라인 목록
     * Side Effects: 없음
     * Raises: 없음
     */
    public List<OrderLine> getLines() {
        return lines;
    }

    /**
     * 목적: 발주 라인 목록을 설정한다.
     * Args:
     *  - lines: 라인 목록
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setLines(List<OrderLine> lines) {
        this.lines = lines;
    }

    /**
     * 목적: 라인을 추가한다.
     * Args:
     *  - line: 발주 라인
     * Returns: 없음
     * Side Effects:
     *  - 라인에 주문 참조를 설정한다.
     * Raises: 없음
     */
    public void addLine(OrderLine line) {
        line.setOrder(this);
        this.lines.add(line);
    }
}

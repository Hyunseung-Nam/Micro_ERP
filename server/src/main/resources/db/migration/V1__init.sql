CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) NOT NULL PRIMARY KEY,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items (
    item_id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    safety_stock INT NOT NULL
);

CREATE TABLE IF NOT EXISTS locations (
    location_id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS partners (
    partner_id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory (
    item_id VARCHAR(50) NOT NULL,
    location_id VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (item_id, location_id),
    CONSTRAINT fk_inventory_item FOREIGN KEY (item_id) REFERENCES items(item_id),
    CONSTRAINT fk_inventory_location FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    partner_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_partner FOREIGN KEY (partner_id) REFERENCES partners(partner_id)
);

CREATE TABLE IF NOT EXISTS order_lines (
    line_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    item_id VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    unit VARCHAR(20) NOT NULL,
    CONSTRAINT fk_order_lines_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_order_lines_item FOREIGN KEY (item_id) REFERENCES items(item_id)
);

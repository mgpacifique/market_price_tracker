-- Migration: Add Authentication, Authorization, and Orders System
-- Date: 2025-11-20
-- Description: Adds users, roles, sessions, orders, and updates existing tables

-- ============================================
-- USERS AND AUTHENTICATION
-- ============================================

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    role ENUM('super_admin', 'seller', 'customer') NOT NULL DEFAULT 'customer',
    status ENUM('active', 'pending', 'suspended', 'deleted') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_role (role)
);

-- Create user sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(255) NOT NULL UNIQUE,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_session_token (session_token),
    INDEX idx_user_id (user_id)
);

-- ============================================
-- UPDATE EXISTING TABLES
-- ============================================

-- Add user_id to markets table (sellers own markets)
-- Note: Using separate statements for better compatibility
ALTER TABLE markets 
ADD COLUMN user_id INT NULL;

ALTER TABLE markets
ADD COLUMN status ENUM('active', 'inactive') DEFAULT 'active';

ALTER TABLE markets
ADD COLUMN description TEXT;

-- Add foreign key if it doesn't exist
ALTER TABLE markets
ADD CONSTRAINT fk_markets_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL;

-- Add user_id to products table (track who added the product)
ALTER TABLE products
ADD COLUMN user_id INT NULL;

ALTER TABLE products
ADD COLUMN market_id INT NULL;

ALTER TABLE products
ADD COLUMN description TEXT;

ALTER TABLE products
ADD COLUMN image_url VARCHAR(255);

ALTER TABLE products
ADD CONSTRAINT fk_products_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL;

ALTER TABLE products
ADD CONSTRAINT fk_products_market FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE SET NULL;

-- ============================================
-- ORDERS SYSTEM
-- ============================================

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    market_id INT NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    status ENUM('pending', 'confirmed', 'processing', 'ready', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
    delivery_address TEXT,
    delivery_phone VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE,
    INDEX idx_customer (customer_id),
    INDEX idx_market (market_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    INDEX idx_order (order_id),
    INDEX idx_product (product_id)
);

-- ============================================
-- ANALYTICS TABLES
-- ============================================

-- Create price_history_summary for faster analytics
CREATE TABLE IF NOT EXISTS price_history_summary (
    summary_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    market_id INT NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    avg_price DECIMAL(10, 2),
    min_price DECIMAL(10, 2),
    max_price DECIMAL(10, 2),
    price_change_percent DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE,
    UNIQUE KEY unique_summary (product_id, market_id, year, month),
    INDEX idx_date (year, month)
);

-- ============================================
-- NOTIFICATIONS SYSTEM
-- ============================================

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type ENUM('order', 'price_alert', 'system', 'account') NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_read (user_id, is_read),
    INDEX idx_created_at (created_at)
);

-- ============================================
-- INITIAL DATA
-- ============================================

-- Insert default super admin (password: admin123)
-- Note: This should be changed immediately after first login
INSERT IGNORE INTO users (username, email, password_hash, full_name, role, status)
VALUES (
    'admin',
    'admin@marketpricetracker.com',
    '$2b$12$S0Sis8ePqsoILhW938LJ8ewSXcOtTYgSMHZdX9Idxg4U2l2OJR6iq',
    'System Administrator',
    'super_admin',
    'active'
);

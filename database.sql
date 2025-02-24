CREATE DATABASE online_delivery_db;
USE online_delivery_db;

-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role ENUM('admin', 'vendor', 'delivery', 'customer') NOT NULL
);

-- Products table
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    vendor_id INT NOT NULL, 
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    availability BOOLEAN DEFAULT TRUE,
    category VARCHAR(100)
);

-- Orders table
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL, 
    status ENUM('Placed', 'Processing', 'Shipped', 'Out for Delivery', 'Delivered', 'Canceled') DEFAULT 'Placed',
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order Items table
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL, 
    product_id INT NOT NULL, 
    quantity INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL
);

-- Deliveries table
CREATE TABLE deliveries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL, 
    delivery_personnel_id INT NOT NULL,
    status ENUM('Assigned', 'Out for Delivery', 'Delivered', 'Failed') DEFAULT 'Assigned',
    tracking_link VARCHAR(255)
);

-- Payments table
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL, 
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('Credit Card', 'Debit Card', 'Wallet') NOT NULL,
    payment_status ENUM('Success', 'Failed', 'Pending') DEFAULT 'Pending'
);

INSERT INTO users (username, email, password_hash, role) VALUES
('admin_user', 'admin@example.com', 'hashed_password1', 'admin'),
('vendor_user', 'vendor1@example.com', 'hashed_password2', 'vendor'),
('delivery_user', 'delivery@example.com', 'hashed_password3', 'delivery'),
('customer_user', 'customer@example.com', 'hashed_password4', 'customer');

INSERT INTO products (vendor_id, name, description, price, availability, category) VALUES
(2, 'Gaming Laptop', 'High-end gaming laptop', 1500.00, TRUE, 'Electronics'),
(2, 'Wireless Headphones', 'Noise-canceling wireless headphones', 200.00, TRUE, 'Electronics'),
(2, 'Office Chair', 'Ergonomic office chair', 120.00, TRUE, 'Furniture');

INSERT INTO orders (customer_id, status, total_amount) VALUES
(4, 'Placed', 1700.00),
(4, 'Processing', 320.00);

INSERT INTO order_items (order_id, product_id, quantity, subtotal) VALUES
(1, 1, 1, 1500.00),
(1, 2, 1, 200.00),
(2, 3, 1, 120.00);

INSERT INTO deliveries (order_id, delivery_personnel_id, status, tracking_link) VALUES
(1, 3, 'Assigned', 'https://track.delivery/12345'),
(2, 3, 'Out for Delivery', 'https://track.delivery/67890');

INSERT INTO payments (order_id, amount, payment_method, payment_status) VALUES
(1, 1700.00, 'Credit Card', 'Success'),
(2, 320.00, 'Wallet', 'Pending');

DELETE from users where id in (1,2,3);

ALTER TABLE users ADD COLUMN phone_number VARCHAR(15) NOT NULL;





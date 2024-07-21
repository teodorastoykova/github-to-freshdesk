CREATE DATABASE IF NOT EXISTS github_users;
USE github_users;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    github_username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    bio TEXT,
    location VARCHAR(255),
    created_at DATETIME,
    is_recorded_fd BOOLEAN NOT NULL DEFAULT 0,
    freshdesk_contact_id INT
);

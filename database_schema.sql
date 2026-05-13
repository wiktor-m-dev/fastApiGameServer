-- Game Server Database Schema
-- This script creates all necessary tables for the FastAPI Game Server

-- Drop existing tables (optional - for fresh setup)
-- DROP TABLE IF EXISTS matches;
-- DROP TABLE IF EXISTS users;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    character_name VARCHAR(100),
    level INT DEFAULT 1,
    attack INT DEFAULT 10,
    defense INT DEFAULT 10,
    health INT DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username)
);

-- Matches Table
CREATE TABLE IF NOT EXISTS matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    player1_id INT NOT NULL,
    player2_id INT NOT NULL,
    status ENUM('searching', 'found', 'in_progress', 'completed', 'cancelled') DEFAULT 'in_progress',
    winner_id INT,
    player1_damage INT DEFAULT 0,
    player2_damage INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (player1_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (player2_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (winner_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_player1 (player1_id),
    INDEX idx_player2 (player2_id),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
);

-- Sample data (optional)
-- INSERT INTO users (username, password, character_name, level, attack, defense, health)
-- VALUES 
--     ('player1', 'hashed_password_1', 'Hero', 5, 15, 12, 120),
--     ('player2', 'hashed_password_2', 'Warrior', 3, 12, 10, 100);

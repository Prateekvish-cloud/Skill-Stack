CREATE DATABASE IF NOT EXISTS skill_stack;
USE skill_stack;

-- Phase 1: authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(190) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL
);

-- Phase 2: coding profile connections, one row per platform per user
CREATE TABLE IF NOT EXISTS coding_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    platform VARCHAR(40) NOT NULL,       -- 'leetcode', 'github', 'codechef', 'codeforces', 'geeksforgeeks', 'hackerrank'
    username VARCHAR(120) NOT NULL,
    problems_solved INT DEFAULT 0,
    rating VARCHAR(100) DEFAULT '—',
    solved_label VARCHAR(100) DEFAULT '0 Solved',
    connected BOOLEAN DEFAULT TRUE,
    last_synced DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY user_platform_unique (user_id, platform)
);

-- Sync Activity Logs
CREATE TABLE IF NOT EXISTS sync_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    platform VARCHAR(40) NOT NULL,
    status VARCHAR(50) NOT NULL,         -- 'Synced (200 OK)', 'Error', etc.
    message TEXT,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Phase 3: projects a student adds to their profile
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    stars INT DEFAULT 0,
    forks INT DEFAULT 0,
    tags VARCHAR(255),
    repo_url VARCHAR(255),
    demo_url VARCHAR(255),
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Phase 3: badges earned
CREATE TABLE IF NOT EXISTS badges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    badge_name VARCHAR(100) NOT NULL,
    earned_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


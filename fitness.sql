-- create database and tables for fitness management system
DROP DATABASE IF EXISTS fitness;
CREATE DATABASE IF NOT EXISTS fitness;
USE fitness;

-- create roles table
CREATE TABLE IF NOT EXISTS roles (
    role_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(255) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create users table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role_id INT not NULL,
    status TINYINT DEFAULT 0,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create members table
CREATE TABLE IF NOT EXISTS members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE not null,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    position VARCHAR(255),
    phone_number VARCHAR(20),
    address VARCHAR(255),
    birth_date DATE,
    health_info TEXT,
    profile_image VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create subscription plans table
CREATE TABLE IF NOT EXISTS subscription_plans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(255),
    price DECIMAL(10, 2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create specific subscriptions table
CREATE TABLE IF NOT EXISTS specific_subscriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT not null,
    subscription_plan_id INT not null,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (subscription_plan_id) REFERENCES subscription_plans(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create trainers table
CREATE TABLE IF NOT EXISTS trainers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE not null,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    title VARCHAR(255),
    phone_number VARCHAR(20),
    profile_image VARCHAR(255),
    description text,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create managers table
CREATE TABLE IF NOT EXISTS managers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE not null,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    title VARCHAR(255),
    phone_number VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create course types table
CREATE TABLE IF NOT EXISTS course_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create fitness class locations table
CREATE TABLE IF NOT EXISTS location(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create fitness classes table
CREATE TABLE IF NOT EXISTS fitness_classes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    description TEXT,
    course_type_id INT not null,
    trainer_id INT not null,
    schedule_time DATETIME,
    location_id INT not null,
    price DECIMAL(10, 2),
    capacity INT not null,
    FOREIGN KEY (course_type_id) REFERENCES course_types(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES trainers(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    fitness_class_id INT,
    booking_date DATETIME,
    status TINYINT DEFAULT 0,
    is_attend TINYINT DEFAULT 0,
    is_paid TINYINT DEFAULT 0,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (fitness_class_id) REFERENCES fitness_classes(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- create news table
CREATE TABLE IF NOT EXISTS news (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    content TEXT,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    manager_id INT not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

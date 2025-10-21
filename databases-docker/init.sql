-- init.sql : setting up users table with two example rows
CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    fullname VARCHAR(100),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, fullname) VALUES
  ('mona99', 'mona.ayoub@school.edu', 'Mona Ayoub'),
  ('jamal22', 'jamal.benali@school.edu', 'Jamal Benali');

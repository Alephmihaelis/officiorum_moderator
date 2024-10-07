DROP DATABASE IF EXISTS officiorum_db;

CREATE DATABASE officiorum_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE officiorum_db;

CREATE TABLE officia (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(127) NOT NULL,
    description TEXT NOT NULL,
    expire DATETIME DEFAULT NULL,
    status ENUM('pending', 'completed', 'deleted') DEFAULT 'pending'
);

DROP TRIGGER IF EXISTS before_insert_task;

DELIMITER //

CREATE TRIGGER before_insert_task
BEFORE INSERT ON task
FOR EACH ROW
BEGIN
    IF NEW.expire IS NULL THEN
        SET NEW.expire = DATE_ADD(NOW(), INTERVAL 30 DAY);
    END IF;
END;

//

DELIMITER ;

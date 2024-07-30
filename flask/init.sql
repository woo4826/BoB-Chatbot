DROP DATABASE IF EXISTS `chatbot`;

CREATE DATABASE `chatbot`;

USE `chatbot`;

CREATE TABLE `access_table` (
    id INT AUTO_INCREMENT NOT NULL, 
    access_id VARCHAR(100), 
    user_id VARCHAR(100), 
    channel_id VARCHAR(100), 
    access_time DATETIME, 
    PRIMARY KEY (id)
);

CREATE TABLE `user_table` (
    id INT AUTO_INCREMENT NOT NULL, 
    user_id VARCHAR(100), 
    PRIMARY KEY (id)
);
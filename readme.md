
현재 config.json 파일 관련하여
db 사용자 생성 및 권한부여 방법
1. maridadb/mysql 유저 생성
create user '{사용자이름}'@'{접속가능호스트}' identified by '{비번}'
// create user 'chatbot.user'@'localhost' identified by 'password';

2. database 생성
create database {데이터베이스 이름};
// create database chatbot;

2-1. database 내부에 access_table 생성
CREATE TABLE access_table (
    id INT AUTO_INCREMENT NOT NULL, 
    access_id VARCHAR(100), 
    user_id VARCHAR(100), 
    channel_id VARCHAR(100), 
    access_time DATETIME, 
    PRIMARY KEY (id)
);
2-2. database 내부에 user_table 생성
CREATE TABLE user_table (
    id INT AUTO_INCREMENT NOT NULL, 
    user_id VARCHAR(100), 
    PRIMARY KEY (id)
);

3. 사용자에게 해당 db 권한부여
grant all privileges on {데이터베이스 이름}.{} to '{사용자이름}'@'{접속가능호스트}';
// grant all privileges on chatbot.* to 'chatbot.user'@'localhost';



4. 완료

현재 config.json 파일 관련하여
db 사용자 생성 및 권한부여 방법
## 1. maridadb/mysql 유저 생성
create user '{사용자이름}'@'{접속가능호스트}' identified by '{비번}'
// create user 'chatbot.user'@'localhost' identified by 'password';

## 2. database 생성
create database {데이터베이스 이름};
// create database chatbot;

# 2-1. database 내부에 access_table 생성
CREATE TABLE access_table (
    id INT AUTO_INCREMENT NOT NULL, 
    access_id VARCHAR(100), 
    user_id VARCHAR(100), 
    channel_id VARCHAR(100), 
    access_time DATETIME, 
    PRIMARY KEY (id)
);
# 2-2. database 내부에 user_table 생성
CREATE TABLE user_table (
    id INT AUTO_INCREMENT NOT NULL, 
    user_id VARCHAR(100), 
    PRIMARY KEY (id)
);
   
CREATE TABLE ioclog_table(
    id INT AUTO_INCREMENT NOT NULL,
    access_user_id VARCHAR(100),
    access_ch_id VARCHAR(100),
    message_text VARCHAR(100),
    access_time DATETIME,
    PRIMARY KEY (id)
    

)
# Forign key 는 일부러 연결시키지 않음.

## 3. 사용자에게 해당 db 권한부여
grant all privileges on {데이터베이스 이름}.{} to '{사용자이름}'@'{접속가능호스트}';
// grant all privileges on chatbot.* to 'chatbot.user'@'localhost';



## 4. 완료

## 5. 사용방법
## 1- [POST] http://0.0.0.0:8080/user/create 
## body : { "user_id" : ${userid} } 
위 요청을 보내 사용자 등록


## 2- [POST] http://0.0.0.0:8080/access
## body : { "user_id" : ${userid}, "channel_id" : ${channel_id} } 
위 요청을 보내 access_table 에 사용자 접근 시각 등록. (서버시간 기준 UTC)


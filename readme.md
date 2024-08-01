
# Compose 실행방법
`docker compose up`

------
# WEB UI
localhost:3000  접속
### 좌측 : IoC Details, 유저생성, access 생성
우측의 유저 목록 중 유저를 눌러서도 access 생성 가능.

### 우측 : 유저목록, 시스템정보
유저 목록 / 시스템 정보

-------
## local 실행방법
db 사용자 생성 및 권한부여 방법
## 1. maridadb/mysql 유저 생성
create user '{사용자이름}'@'{접속가능호스트}' identified by '{비번}'

create user 'chatbot.user'@'localhost' identified by 'password';

## 2. database 생성
create database {데이터베이스 이름};

create database chatbot;

### 2-1. database 내부에 access_table 생성
CREATE TABLE access_table (
    id INT AUTO_INCREMENT NOT NULL, 
    access_id VARCHAR(100), 
    user_id VARCHAR(100), 
    channel_id VARCHAR(100), 
    access_time DATETIME, 
    PRIMARY KEY (id)
);
### 2-2. database 내부에 user_table 생성

CREATE TABLE user_table (
    id INT AUTO_INCREMENT NOT NULL, 
    user_id VARCHAR(100), 
    PRIMARY KEY (id)
);
Forign key 는 일부러 연결시키지 않음.

## 3. 사용자에게 해당 db 권한부여
grant all privileges on {데이터베이스 이름}.{} to '{사용자이름}'@'{접속가능호스트}';

grant all privileges on chatbot.* to 'chatbot.user'@'localhost';



## 5. APIS
### 1. [POST] http://0.0.0.0:3000/user/create 
body : { "user_id" : ${userid} } 
위 요청을 보내 사용자 등록


### 2- [POST] http://0.0.0.0:3000/access
body : { "user_id" : ${userid}, "channel_id" : ${channel_id} } 
위 요청을 보내 access_table 에 사용자 접근 시각 등록. (서버시간 기준 UTC)

### 3- [GET] http://0.0.0.0:3000/ioc
과거 사용자 접근 목록과 server PC 의 상태정보 값을 리턴받는다.



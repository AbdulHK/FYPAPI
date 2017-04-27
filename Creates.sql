drop trigger rate;
drop trigger mapping;
drop table Menu;
drop table Review;
drop table Users;
drop table Numbers;
drop table Hours;
drop table Restaurant;


CREATE TABLE Users
(
id int AUTO_INCREMENT  PRIMARY KEY,
username varchar(32) unique,
password_hash varchar(512),
address varchar(128),
firstname varchar(32),
lastname varchar(32),
createdAt timestamp,
deleted boolean DEFAULT 0,
pre1 varchar(32),
pre2 varchar(32),
pre3 varchar(32),
image_filename varchar(100),
image_url varchar(100)
);


CREATE TABLE Restaurant
(
id int AUTO_INCREMENT PRIMARY KEY,
name varchar(64),
address1 varchar(128),
address2 varchar(64),
phone int,
lat decimal(12,10),
lng decimal(12,10),
cost int,
menu_type varchar(64),
rate decimal(2,1),
has_delivery varchar(1) default 0,
has_parking varchar(1)default 0,
has_wifi varchar(1) default 0,
has_reservation varchar(1) default 0,
has_cards varchar(1)default 0,
has_bar varchar(1) default 0,
has_terrace varchar(1) default 0,
offer varchar(128),
createdAt timestamp,
image_filename varchar(100),
image_url varchar(100),
deleted boolean DEFAULT 0
);

Create Table Menu
(
id int AUTO_INCREMENT PRIMARY KEY,
restid int,
dish varchar(64),
price decimal,
description varchar(128),
createdAt timestamp,
deleted boolean DEFAULT 0,
FOREIGN KEY fk_menu(restid)
   REFERENCES Restaurant(id)
);
CREATE TABLE Review
(
id int AUTO_INCREMENT PRIMARY KEY,
username varchar(32),
rest_id int,
title varchar(64),
overall_rate int NOT NULL,
discription varchar(512),
createdAt timestamp,
image_filename varchar(100),
image_url varchar(100),
deleted boolean DEFAULT 0,
FOREIGN KEY fk_user(username)
   REFERENCES Users(username),
FOREIGN KEY restaurant_id(rest_id)
   REFERENCES Restaurant(id)
);

CREATE TABLE Numbers
(
id int AUTO_INCREMENT PRIMARY KEY,
userid int  unique,
num1 varchar(32),
num2 varchar(32),
num3 varchar(32)
);


CREATE TABLE Hours
(
id int AUTO_INCREMENT PRIMARY KEY,
restid int ,
Day VARCHAR(32),
StartTime VARCHAR(32),
FinishTime VARCHAR(32),
FOREIGN KEY fk_res(restid)
   REFERENCES Restaurant(id)
);
DELIMITER //
CREATE  TRIGGER `mapping` AFTER INSERT ON `UserPref`
        FOR EACH ROW
        BEGIN
        DECLARE  n1 INT;
		    DECLARE  n2 INT;
        DECLARE  n3 INT;
				if new.pre1 = "Irish" THEN
                SET  n1=1;
                ELSEIF new.pre1 = "American" THEN
                SET n1=2;
                ELSEIF new.pre1 = "Italian" THEN
                SET n1=3;
                ELSEIF new.pre1 = "International" THEN
                SET n1=4;
                ELSEIF new.pre1 = "Thai" THEN
                SET n1=5;
                ELSEIF new.pre1 = "Middle Eastren" THEN
                SET n1=6;
				        ELSEIF new.pre1 = "Burger" THEN
                SET n1=7;
                ELSEIF new.pre1 = "BBQ" THEN
                SET n1=8;
				END IF ;
        if new.pre2 = "Irish" THEN
                SET  n2=1;
                ELSEIF new.pre2 = "American" THEN
                SET n2=2;
                ELSEIF new.pre2 = "Italian" THEN
                SET n2=3;
                ELSEIF new.pre2 = "International" THEN
                SET n2=4;
                ELSEIF new.pre2 = "Thai" THEN
                SET n2=5;
                ELSEIF new.pre2 = "Middle Eastren" THEN
                SET n2=6;
				        ELSEIF new.pre2 = "Burger" THEN
                SET n2=7;
                ELSEIF new.pre2 = "BBQ" THEN
                SET n2=8;
        END IF;
				if new.pre3 = "Irish" THEN
                SET  n3=1;
                ELSEIF new.pre3 = "American" THEN
                SET n3=2;
                ELSEIF new.pre3 = "Italian" THEN
                SET n3=3;
                ELSEIF new.pre3 = "International" THEN
                SET n3=4;
                ELSEIF new.pre3 = "Thai" THEN
                SET n3=5;
                ELSEIF new.pre3 = "Middle Eastren" THEN
                SET n3=6;
				        ELSEIF new.pre3 = "Burger" THEN
                SET n3=7;
                ELSEIF new.pre3 = "BBQ" THEN
                SET n3=8;
        END IF;
        INSERT INTO Numbers(userid,num1,num2,num3) VALUES(new.userid,`n1`,`n2`,`n3`);
        END; //
DELIMITER ;


DELIMITER //
CREATE  TRIGGER `rate` AFTER INSERT ON `Review`
        FOR EACH ROW
        BEGIN
			DECLARE  n1 decimal;
		 select AVG(overall_rate)  into n1 from Review where rest_id=new.rest_id;

            UPDATE Restaurant SET Restaurant.rate=n1 where id=new.rest_id;
        END; //
DELIMITER ;
DELIMITER //
CREATE  TRIGGER `rate` AFTER UPDATE ON `Review`
        FOR EACH ROW
        BEGIN
			DECLARE  n1 decimal;
		 select AVG(overall_rate)  into n1 from Review where rest_id=new.rest_id;

            UPDATE Restaurant SET Restaurant.rate=n1 where id=new.rest_id;
        END; //
DELIMITER ;
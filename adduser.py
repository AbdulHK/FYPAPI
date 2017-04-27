# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String,Float,ForeignKey
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
import names,json,random
from sqlalchemy.ext.declarative import declarative_base
from faker import Faker


SECERT_KEY="Hello there my name is Abdul"
engine = create_engine('cmysql+mysqldb://Abdul:Abdul1993@52.24.39.230:3306/test')
Base = declarative_base()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)  # once engine is available
session = Session()
fake = Faker()

class Menu(Base):
    __tablename__ = 'Menu'
    id = Column(Integer, primary_key=True)
    restid = Column(Integer)
    dish = Column(String(64))
    price = Column(Integer)
    description = Column(String(128))

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(512))
    address =Column(String(128))
    firstname = Column(String(32))
    lastname = Column(String(32))
 
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

class UserPref(Base):
    __tablename__ = 'UserPref'
    prefid= Column(Integer,primary_key=True)
    userid = Column(Integer)
    pre1 = Column(String(32))
    pre2 = Column(String(32))
    pre3 = Column(String(32))

class Review(Base):
    __tablename__ = 'Review'
    id = Column(Integer, primary_key=True)
    username = Column(Integer)
    rest_id = Column(Integer)
    title=Column(String(64))
    overall_rate =Column(Integer)
    discription = Column(String(64))

class Hours(Base):
    __tablename__ = 'Hours'
    id= Column(Integer,primary_key=True)
    restid = Column(Integer)
    Day = Column(String(32))
    StartTime = Column(String(32))
    FinishTime = Column(String(32))

class Restaurant(Base):
    __tablename__ ='Restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    address1 =Column(String(128))
    address2 = Column(String(32))
    phone =Column(Integer)
    lat = Column(Float(precision='12,10'))
    lng = Column(Float(precision='12,10'))
    cost = Column(Integer)
    menu_type = Column(String(64))
    rate =Column(Float(precision='3,2'))
    offer=Column(String(128))
    has_delivery=Column(String(1))
    has_parking=Column(String(1))
    has_wifi=Column(String(1))
    has_reservation=Column(String(1))
    has_cards=Column(String(1))
    has_bar=Column(String(1))
    has_terrace=Column(String(1))


def new_user():
    count=0
    print(" I will be creating some random users so please give me some time (up to 5 minutes) to finish!")
    while (count <100):

        username="dody" + str(count)
        password=names.get_full_name()
        user = User(username=username,address=fake.address(),firstname=names.get_first_name(),lastname=names.get_last_name())
        user.hash_password(password)
        session.add(user)
        print (count)
        count = 1+ count
    print(" I have Added 100 Users, waiting for the commit!")

def new_dish():
    count=0
    menulist=["Pizza","Kebab","Irish Breakfast","Burger","Chips","Shrimp","Seabas","Fish&Chips","1/4 chicken","Pasta Ravioli"
              "Chicken fillet pitta","Chicken burger","Chicken Tikka Masala","Chicken Korma","Margareta Pizza","Pepproni Pizza"
        ,"Fuzzy Drink","chicken Burrito", "lamb burrito","Mexican Rice","Sushi","Spring Rolls","Chicken Balls"
              ]
    Descriptionlist="A short descirption of the item"
    price=[10,20,30,5,15,25,18,8]
    while (count < 1000):
        dish = random.choice(menulist)
        price = count
        desc = "desc" + str(count)
        restid=random.randrange(1,100)
        dish= Menu(restid=restid,dish=dish,price=price,description=desc)
        session.add(dish)
        count = count + 1
    print(" Done, I have added 1000 dishs! Waiting for the commit!")


def time():
    count=1
    r=0
    while (count <= 100):
        day = 0
        while (day < 7):
            restid=count
            Day = day
            FinishTime = "23:00:00"
            StartTime = "09:00:00"
            hours= Hours(restid=restid,Day=Day,FinishTime=FinishTime,StartTime=StartTime)
            session.add(hours)
            day = day + 1
        count = count +1

    print(" Done, I have added 1000 times! Waiting for the commit!")

def add_review():
    count=1
    while (count <= 500):
        id="dody1"
        rest_id=random.randrange(1,100)
        desc="so good"
        title="Test Review"
        rate=random.randrange(1,5)
        review=Review(username=id,rest_id=rest_id,discription=desc,overall_rate=rate,title=title)
        session.add(review)
        count= count +1

    print(" Done, I have added 500 reviews! Waiting for the commit!, this takes time due to Triggers.")


#new_restaurant()
#session.commit()

#new_user()
#session.commit()

#new_pref()
#session.commit()

#new_dish()
#session.commit()

#time()
#session.commit()
add_review()
session.commit()
print ("commited")
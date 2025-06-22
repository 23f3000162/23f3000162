
# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL
# from sqlalchemy.orm import relationship, declarative_base
# from datetime import datetime


# this is my models.py file for the Flask application using SQLAlchemy ORM

# Base = declarative_base()

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username= db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String, unique=True)
    phone = db.Column(db.String)
    address = db.Column(db.Text)
    pincode = db.Column(db.Integer)
    
    role = db.Column(db.Integer, default=1)  # 'admin' or 'user'

    reservations = db.relationship('Reservation', back_populates='user')


class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prime_location_name = db.Column(db.String, nullable=False)
    price_per_hour = db.Column(db.DECIMAL, nullable=False)
    address = db.Column(db.Text)
    pin_code = db.Column(db.String)
    number_of_spots = db.Column(db.Integer)
    occuipied_spots = db.Column(db.Integer, default=0)
    abliable_spots = db.Column(db.Integer, default=0)
    
    

    spots = db.relationship('ParkingSpot', back_populates='lot')

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    spot_number = db.Column(db.String)
    status = db.Column(db.String)  # 'A' or 'O'
    level = db.Column(db.Integer)
   

    lot = db.relationship('ParkingLot', back_populates='spots')
    reservations = db.relationship('Reservation', back_populates='spot')

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False)
    leaving_timestamp = db.Column(db.DateTime, nullable=False)
    parking_cost = db.Column(db.DECIMAL)
    status = db.Column(db.String, default='Active')

    user = db.relationship('User', back_populates='reservations')
    spot = db.relationship('ParkingSpot', back_populates='reservations')
    payment = db.relationship('Payment', back_populates='reservation', uselist=False)

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'), nullable=False)
    amount = db.Column(db.DECIMAL)
    payment_method = db.Column(db.String)
    payment_status = db.Column(db.String)
    payment_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    reservation = db.relationship('Reservation', back_populates='payment')

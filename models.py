from flask_sqlalchemy import SQLAlchemy
from database import db


# Create the User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    password= db.Column(db.String, nullable=False)


    bookings = db.relationship('Booking', back_populates='user')


# Create the ServiceProvider model
class ServiceProvider(db.Model):
    __tablename__ = 'service_providers'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    type_of_service = db.Column(db.String, nullable=False)
    nb_of_clients_served = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    password= db.Column(db.String, nullable=False)
    bookings = db.relationship('Booking', back_populates='service_provider')


# Create the Booking model
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_provider_id = db.Column(db.String, db.ForeignKey('service_providers.id'), nullable=False)
    date = db.Column(db.String, nullable=False)
    #duration = db.Column(db.Interval, nullable=False)

    user = db.relationship('User', back_populates='bookings')
    service_provider = db.relationship('ServiceProvider', back_populates='bookings')

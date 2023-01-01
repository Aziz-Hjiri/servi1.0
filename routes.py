from xml.dom import ValidationErr
from flask_restful import Resource
from flask import request
from database import db
from models import User, ServiceProvider, Booking
from schemas import UserSchema, ServiceProviderSchema, BookingSchema
import uuid
import json

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from security import authenticate, authenticate_service_provider


# Use the Marshmallow schema to serialize/deserialize the data
user_schema = UserSchema()
users_schema = UserSchema(many=True)
service_provider_schema = ServiceProviderSchema()
service_providers_schema = ServiceProviderSchema(many=True)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

# Create the UserList resource
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        # Use the schema to serialize the data
        result = users_schema.dump(users)
        return result

# Create the User resource
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        # Use the schema to serialize the data
        result = user_schema.dump(user)
        return result

class UpdateUser(Resource):
    @jwt_required()
    def put(self):
        # Get the authenticated user's information from the JWT
        current_user = get_jwt_identity()

        # Find the user with the specified ID
        user = User.query.filter_by(id=current_user).first()
        if not user:
            # If no user was found, return a 404 Not Found error
            return {'message': 'User not found'}, 404

        # Parse the request data
        data = request.get_json()

        # Validate the data
        user_schema = UserSchema(session=db.session, partial=True)
        errors = user_schema.validate(data)
        if errors:
            # If the data is invalid, return a 422 Unprocessable Entity error
            return {'message': 'Validation errors', 'errors': errors}, 422

        # If the data is valid, update the user with the new information
        for key, value in data.items():
            if key != 'id':
                setattr(user, key, value)
        db.session.commit()

        # Serialize the updated user data and return it as the response
        result = user_schema.dump(user)
        return result, 200




# Create the ServiceProviderList resource
class ServiceProviderListResource(Resource):
    def get(self):
        service_providers = ServiceProvider.query.all()
        # Use the schema to serialize the data
        result = service_providers_schema.dump(service_providers)

        return result

# Create the ServiceProvider resource
class ServiceProviderResource(Resource):
    def get(self, service_provider_id):
        service_provider = ServiceProvider.query.get(service_provider_id)
        # Use the schema to serialize the da
        result = service_provider_schema.dump(service_provider)
        
        return result

# Create the BookingList resource
class BookingListResource(Resource):
    def get(self):
        bookings = Booking.query.all()
        # Use the schema to serialize the data
        result = bookings_schema.dump(bookings)
        return result

# Create the Booking resource
class BookingResource(Resource):
    def get(self, booking_id):
        booking = Booking.query.get(booking_id)
        # Use the schema to serialize the data
        result = booking_schema.dump(booking)
        return result

class UserRegister(Resource):
    def post(self):
        # Parse the request data
        data = request.get_json()

        # Initialize the schema with the current session
        user_schema = UserSchema(session=db.session)

        # Validate the data
        errors = user_schema.validate(data)
        if errors:
            # If the data is invalid, return a 422 Unprocessable Entity error
            return {'message': 'Validation errors', 'errors': errors}, 422

        # If the data is valid, create a new user instance
        new_user = User(name=data['name'], age=data['age'], phone_number=data['phone_number'],
                        email=data['email'], location=data['location'], password=data['password'])

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Serialize the user data and return it as the response
        result = user_schema.dump(new_user)
        return {'message': 'User Created Successfully'}, 201
class ServiceProviderRegister(Resource):
    def post(self):
        # Parse the request data
        data = request.get_json()
        service_provider_schema = ServiceProviderSchema(session=db.session)
        data['id'] = str(uuid.uuid4())
        data['nb_of_clients_served']=0 
        data['rate']=0
        # Validate the data
        errors = service_provider_schema.validate(data)
        if errors:
            # If the data is invalid, return a 422 Unprocessable Entity error
            return {'message': 'Validation errors', 'errors': errors}, 422       

        # Create a new service provider instance with the new ID
        new_service_provider = ServiceProvider(**data)

        # Add the service provider to the database
        db.session.add(new_service_provider)
        db.session.commit()

        # Serialize the service provider data and return it as the response
        return {'message':'Service Provider Created Successfully'}, 201
    
class UserLogin(Resource):
    def post(self):
        # Parse the request data
        data = request.get_json()
        # Authenticate the user
        user = authenticate(data['email'], data['password'])
        if user:
            # Generate a JWT token
            access_token = create_access_token(identity=user.id)
            return {'welcome_message': 'Welcome, {}!'.format(user.name), 'access_token': access_token}, 200       
        else:
            return {'message': 'Invalid credentials'}, 401
class BookingCreate(Resource):
    @jwt_required()
    def post(self):
        # Parse the request data
        data = request.get_json()
        booking_schema = BookingSchema(session=db.session)

        # Validate the data
        errors = booking_schema.validate(data)
        if errors:
            # If the data is invalid, return a 422 Unprocessable Entity error
            return {'message': 'Validation errors', 'errors': errors}, 422
        try:
            # If the data is valid, create a new booking instance
            new_booking = Booking(**data)
            # Add the booking to the database
            db.session.add(new_booking)
            db.session.commit()
            # Serialize the booking data and return it as the response
            result = booking_schema.dump(new_booking)
            return {'id': new_booking.id}, 201
        except TypeError:
            
            return {'message': 'Error Serializing data'}, 500

class UpdateBook(Resource):            
    @jwt_required()
    def put(self, booking_id):
    # Get the authenticated user's information from the JWT
        current_user = get_jwt_identity()

    # Find the booking with the specified ID
        booking = Booking.query.filter_by(id=booking_id).first()
        if not booking:
        # If no booking was found, return a 404 Not Found error
          return {'message': 'Booking not found'}, 404

    # Check if the authenticated user is the owner of the booking
        if booking.user_id != current_user:
        # If the authenticated user is not the owner, return a 403 Forbidden error
          return {'message': 'Forbidden'}, 403

    # Parse the request data
        data = request.get_json()

    # Validate the data
        booking_schema = BookingSchema(session=db.session, partial=True)
        errors = booking_schema.validate(data)
        if errors:
        # If the data is invalid, return a 422 Unprocessable Entity error
             return {'message': 'Validation errors', 'errors': errors}, 422

    # If the data is valid, update the booking with the new information
        booking.date = data['date']
        booking.service_provider_id= data['service_provider_id']

        db.session.commit()

    # Serialize the updated booking data and return it as the response
        result = booking_schema.dump(booking)
    
        return result, 200
class DeleteBooking(Resource):
    @jwt_required()
    def delete(self, booking_id):
        # Get the authenticated user's information from the JWT
        current_user = get_jwt_identity()

        # Find the booking with the specified ID
        booking = Booking.query.filter_by(id=booking_id).first()
        if not booking:
            # If no booking was found, return a 404 Not Found error
            return {'message': 'You don''t have a booking with this id'}, 404

        # Check if the authenticated user is the owner of the booking
        if booking.user_id != current_user:
            # If the authenticated user is not the owner, return a 403 Forbidden error
            return {'message': 'You are not the owner of this booking'}, 403

        # If the authenticated user is the owner of the booking, delete the booking
        db.session.delete(booking)
        db.session.commit()

        # Return a success message and a 200 OK status code
        return {'message': 'Booking successfully deleted'}, 200
class SPLogin(Resource):
    def post(self):
        # Parse the request data
        data = request.get_json()
        # Authenticate the service provider
        service_provider = authenticate_service_provider(data['email'], data['password'])
        if service_provider:
            # Generate a JWT token
            access_token = create_access_token(identity=service_provider.id)
            return {'welcome_message': 'Welcome, {}!'.format(service_provider.name), 'access_token': access_token}, 200       
        else:
            return {'message': 'Invalid credentials'}, 401
class ServiceProviderBookingListResource(Resource):
    @jwt_required()
    def get(self):
        # Get the authenticated service provider's ID from the JWT
        current_service_provider_id = get_jwt_identity()

        # Find the service provider object using the ID
        service_provider = ServiceProvider.query.get(current_service_provider_id)
        if not service_provider:
            # If the service provider was not found, return a 404 Not Found error
            return {'message': 'Service provider not found'}, 404

        # Find the bookings associated with the service provider's ID
        bookings = Booking.query.filter_by(service_provider_id=current_service_provider_id).all()
        if not bookings:
            # If no bookings were found, return a 404 Not Found error
            return {'message': 'Bookings not found'}, 404

        # Serialize the data and return it as the response
        booking_schema = BookingSchema(many=True, only=['user_id', 'date'])
        result = booking_schema.dump(bookings)
        return result, 200










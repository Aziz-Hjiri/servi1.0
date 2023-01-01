from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
import routes
from database import db
from flask_jwt_extended import JWTManager
from security import authenticate, identity


app = Flask(__name__)
jwt = JWTManager(app)

api = Api(app)
app.config['JWT_SECRET_KEY'] = 'hjiri'
jwt.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Add the API endpoints
api.add_resource(routes.UserListResource, '/users')
api.add_resource(routes.UserResource, '/users/<int:user_id>')
api.add_resource(routes.ServiceProviderListResource, '/service_providers')
#api.add_resource(routes.ServiceProviderResource, '/service_providers/<str:service_provider_id>')
api.add_resource(routes.BookingListResource, '/bookings')
api.add_resource(routes.BookingResource, '/bookings/<int:booking_id>')
api.add_resource(routes.UserRegister, '/register')
api.add_resource(routes.ServiceProviderRegister, '/service-providers/register')
api.add_resource(routes.UserLogin, '/UserLogin')
api.add_resource(routes.BookingCreate, '/bookings/newBooking')
api.add_resource(routes.UpdateBook, '/bookings/<int:booking_id>')
api.add_resource(routes.DeleteBooking, '/bookings/<int:booking_id>')
api.add_resource(routes.UpdateUser, '/user/update')
api.add_resource(routes.SPLogin, '/service_provider_login')
api.add_resource(routes.ServiceProviderBookingListResource, '/service-providers/bookings')












if __name__ == '__main__':
    app.run()

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import User, ServiceProvider, Booking

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ServiceProviderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceProvider

class BookingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        include_fk = True
        exclude=('id',)
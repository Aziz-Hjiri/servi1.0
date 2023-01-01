import hmac
from models import User, ServiceProvider

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return user
    return {"message": "Please verify your credentials"}

def authenticate_service_provider(email, password):
    service_provider = ServiceProvider.query.filter_by(email=email).first()
    if service_provider and hmac.compare_digest(service_provider.password, password):
        return service_provider
    return {"message": "Verify your credentials"}

   
def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

def identitySP(payload):
    service_provider_id = payload['identity']
    return ServiceProvider.query.get(service_provider_id)


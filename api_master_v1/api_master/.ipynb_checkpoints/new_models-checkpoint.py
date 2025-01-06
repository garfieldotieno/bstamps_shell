# api_master_v1/api_master/new_models.py
from sqlalchemy import Column, String, Integer, DateTime, func, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Auth(Base):
    __tablename__ = 'auth'

    uid = Column(Integer, primary_key=True)
    user_email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String)
    current_auth_verification_status = Column(String)
    current_client_type = Column(String)
    current_auth_token = Column(String)
    current_auth_token_expiry = Column(DateTime)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self):
        """Convert the Auth instance to a dictionary."""
        return {
            'uid': self.uid,
            'user_email': self.user_email,
            'role': self.role,
            'current_auth_verification_status': self.current_auth_verification_status,
            'current_client_type': self.current_client_type,
            'current_auth_token': self.current_auth_token,
            'current_auth_token_expiry': self.current_auth_token_expiry,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @classmethod
    def index(cls, session):
        """Retrieve all Auth records as dictionaries."""
        return [auth.to_dict() for auth in session.query(cls).all()]

    @classmethod
    def store(cls, session, user_email, password_hash, role):
        """Store a new Auth record and return its dictionary representation."""
        new_auth = cls(user_email=user_email, password_hash=password_hash, role=role)
        session.add(new_auth)
        session.commit()
        return new_auth.to_dict()

    @classmethod
    def show(cls, session, uid):
        """Show a specific Auth record by uid as a dictionary."""
        auth_record = session.query(cls).filter_by(uid=uid).first()
        return auth_record.to_dict() if auth_record else None

    @classmethod
    def update(cls, session, uid, **kwargs):
        """Update an Auth record and return its dictionary representation."""
        auth_record = session.query(cls).filter_by(uid=uid).first()
        if auth_record:
            for key, value in kwargs.items():
                setattr(auth_record, key, value)
            session.commit()
        return auth_record.to_dict() if auth_record else None

    @classmethod
    def destroy(cls, session, uid):
        """Delete an Auth record."""
        auth_record = session.query(cls).filter_by(uid=uid).first()
        if auth_record:
            session.delete(auth_record)
            session.commit()
            return True
        return False

    @staticmethod
    def resetAuth(session, uid):
        """Logic to reset authentication for a user."""
        auth_record = session.query(Auth).filter_by(uid=uid).first()
        if auth_record:
            auth_record.current_auth_token = None  # Clear the current auth token
            auth_record.current_auth_token_expiry = None  # Clear the token expiry
            session.commit()
            return auth_record.to_dict()  # Return updated record as dict
        return None  # Return None if user not found

    @staticmethod
    def updateAuthToken(session, uid, new_token, expiry):
        """Logic to update the authentication token for a user."""
        auth_record = session.query(Auth).filter_by(uid=uid).first()
        if auth_record:
            auth_record.current_auth_token = new_token  # Set new token
            auth_record.current_auth_token_expiry = expiry  # Set new expiry
            session.commit()
            return auth_record.to_dict()  # Return updated record as dict
        return None  # Return None if user not found

    @staticmethod
    def verifyAuthToken(session, uid, token):
        """Logic to verify the authentication token for a user."""
        auth_record = session.query(Auth).filter_by(uid=uid).first()
        if auth_record:
            if auth_record.current_auth_token == token:
                current_time = session.execute(func.now()).scalar()  # Get the current time from the database
                if auth_record.current_auth_token_expiry and auth_record.current_auth_token_expiry > current_time:
                    print(f"token is valid")
                    return True  # Token is valid
                print(f"token has expired")
                return False  # Token expired
            print(f"token does not match")
            return False  # Token does not match
        print(f"user is not found")
        return None  # Return None if user not found


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)  # Primary key
    uid = Column(Integer, unique=True, nullable=False)  # Unique identifier
    name = Column(String, nullable=False)  # Name of the location
    location_pin_type = Column(String, nullable=False)  # Type of location pin (e.g., "restaurant", "park")
    latitude = Column(String)  # Latitude of the location (can also be Float)
    longitude = Column(String)  # Longitude of the location (can also be Float)
    user_id = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self):
        """Convert the Location instance to a dictionary."""
        return {
            'id': self.id,
            'uid': self.uid,
            'name': self.name,
            'location_pin_type': self.location_pin_type,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'user_id' : self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @classmethod
    def index(cls, session):
        """Retrieve all Location records as dictionaries."""
        return [location.to_dict() for location in session.query(cls).all()]

    @classmethod
    def store(cls, session, uid, name, location_pin_type, latitude, longitude):
        """Store a new Location record and return its dictionary representation."""
        new_location = cls(uid=uid, name=name, location_pin_type=location_pin_type, latitude=latitude, longitude=longitude)
        session.add(new_location)
        session.commit()
        return new_location.to_dict()

    @classmethod
    def show(cls, session, uid):
        """Show a specific Location record by uid as a dictionary."""
        location_record = session.query(cls).filter_by(uid=uid).first()
        return location_record.to_dict() if location_record else None

    @classmethod
    def update(cls, session, uid, **kwargs):
        """Update a Location record and return its dictionary representation."""
        location_record = session.query(cls).filter_by(uid=uid).first()
        if location_record:
            for key, value in kwargs.items():
                setattr(location_record, key, value)
            session.commit()
        return location_record.to_dict() if location_record else None

    @classmethod
    def destroy(cls, session, uid):
        """Delete a Location record."""
        location_record = session.query(cls).filter_by(uid=uid).first()
        if location_record:
            session.delete(location_record)
            session.commit()
            return True
        return False


# Database setup
if __name__ == "__main__":
    # Database setup
   DATABASE_URL = 'sqlite:///new_models_db.sqlite'  # Use SQLite database
   engine = create_engine(DATABASE_URL)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
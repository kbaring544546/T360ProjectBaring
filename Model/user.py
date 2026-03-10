import bcrypt
import logging
logger = logging.getLogger(__name__)

class User:
    def __init__(self, username, password, role, active=1,
                 first_name="", last_name="", email="", phone_number=""):
        self.id = None
        self.username = username
        self.password = password
        self.role = role
        self.active = active
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def is_active(self):
        return self.active == 1

    def is_admin(self):
        return self.role == 'admin'

    def is_staff(self):
        return self.role == 'staff'

    def verify_password(self, password):
        if not self.is_active():
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        except (ValueError, AttributeError):
            return self.password == password

    def deactivate(self):
        self.active = 0

    def reactivate(self):
        self.active = 1

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'active': self.active,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
        }

    @staticmethod
    def from_dict(data):
        user = User(
            data['username'], data['password'], data['role'], data.get('active', 1),
            data.get('first_name', ''), data.get('last_name', ''),
            data.get('email', ''), data.get('phone_number', '')
        )
        user.id = data.get('id')
        return user

    @staticmethod
    def create_with_hashed_password(username, plain_password, role,
                                    first_name="", last_name="", email="", phone_number=""):
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
        return User(username, hashed_password.decode('utf-8'), role, active=1,
                    first_name=first_name, last_name=last_name,
                    email=email, phone_number=phone_number)

    def authenticate(self, password):
        if self.verify_password(password):
            logger.info(f"User '{self.username}' authenticated successfully")
            return True
        logger.warning(f"Authentication failed for user '{self.username}'")
        return False

    def __repr__(self):
        status = "Active" if self.is_active() else "Inactive"
        return f"User(ID: {self.id}, {self.username}, {self.full_name}, {self.role}, {status})"
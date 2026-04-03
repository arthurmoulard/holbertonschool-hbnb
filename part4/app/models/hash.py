from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User:
    def init(self):
        self.password = None

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
user = User()

user.hash_password("mypassword123")

print("Password hash:", user.password)

print("Correct password:", user.check_password("mypassword123"))
print("Wrong password:", user.check_password("wrongpassword"))
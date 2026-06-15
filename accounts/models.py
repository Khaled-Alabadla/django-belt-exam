from django.db import models
import bcrypt
import re
from datetime import datetime




class UserManager(models.Manager):

    def validate_login(self, email, password):
        errors = {}
        user = self.filter(email=email).first()

        if user:
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return errors, user
            else:
                errors['login'] = "Invalid email or password."
        else:
            errors['login'] = "Invalid email or password."

        return errors, None
    

    def validate_registration(self, data):
        errors = {}
        if not data.get('first_name', ''):
            errors['first_name'] = 'First Name is required'
        if not data.get('last_name', ''):
            errors['last_name'] = 'Last Name is required'
        
        if not data.get('birthday'):
            errors['birthday'] = "Birthday is required."
        else:
            try:
                birthday_obj = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
            except ValueError:
                errors['birthday'] = "Invalid birthday format."

        if not data.get('email', ''):
            errors['email']= 'Email is required'
            
        if not data.get('password', ''):
            errors['password']= 'password is required'

        if len(data.get('first_name', '')) < 4:
            errors['first_name'] = "first name must be at least 4 characters long."
        if len(data.get('last_name', '')) < 4:
            errors['last_name'] = "last name must be at least 4 characters long."

        if not data.get('email') or '@' not in data['email']:
            errors['email'] = "Invalid email address."

        if len(data.get('password', '')) < 8:
            errors['password'] = "Password must be at least 8 characters long."

        if data.get('password') != data.get('confirm_password'):
            errors['confirm_password'] = "Passwords do not match."

        if data.get('email') and self.filter(email=data['email']).exists():
            errors['email'] = "Email is already registered."

        if birthday_obj:
            if birthday_obj > datetime.today().date():
                errors['birthday'] = "Birthday cannot be in the future."
            else:
                age = (datetime.today().date() - birthday_obj).days // 365
                if age < 18:
                    errors['birthday'] = "You must be at least 18 years old."


        return errors

    def create_user(self, data):
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()


        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = self.model(first_name=first_name, last_name = last_name, email=email, password=hashed)
        user.save()
        return user


class User(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def check_password(self, raw_password):
        """Verify password using bcrypt."""
        try:
            return bcrypt.checkpw(raw_password.encode(), self.password.encode())
        except Exception:
            return False

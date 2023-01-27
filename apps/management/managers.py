from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Manager for users"""
    def create_user(self,email,username,password=None):
        """Create a new user """
        if not email:
            raise ValueError('User must have an email.')
        email = self.normalize_email(email)
        user = self.model(email = email,username =username)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,email,username,password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
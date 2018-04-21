from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def create_user(self, email, usertype, password=None,is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        if not usertype:
            raise ValueError("User must have a usertype")

        user_obj = self.model(
            email = self.normalize_email(email),
            usertype=usertype
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, usertype, password=None):
        user = self.create_user(
            email,
            usertype,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, usertype, password=None):
        user = self.create_user(
            email,
            usertype,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    usertype = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usertype']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=100,default='')
    city = models.CharField(max_length=100, default='')
    website=models.URLField(default='')
    phone=models.IntegerField(default=0)
    total_usage=models.IntegerField(default=0)
    flag=models.IntegerField(default=0)

    def __str__(self):
        return self.user.email


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile=UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)

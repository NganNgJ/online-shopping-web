from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model



class AbstractEntity(models.Model):
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(AbstractEntity, self).save(*args, **kwargs)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class Users(AbstractEntity,AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address", unique=True, max_length=255)
    phone = models.CharField(unique=True, max_length=30)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'users'
    

def category_image_path(instance, filename):
    return "product/category/icons/{0}/{1}".format(instance.name,filename)


def product_image_path(instance, filename):
    return "product/images/{0}/{1}".format(instance.name,filename)

class ProductCategory(AbstractEntity, models.Model):
    name = models.CharField(verbose_name='Category name',max_length=255)
    icon = models.ImageField(upload_to=category_image_path, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_categories'

    def __str__(self):
        return self.name

class Product(AbstractEntity, models.Model):
    category = models.ForeignKey(ProductCategory, on_delete= models.CASCADE, related_name='product_lists')
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    image = models.ImageField(upload_to=product_image_path, blank=True)
    price =  models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
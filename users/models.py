from django.db import models
from django.contrib.auth.models import AbstractUser

class Member(AbstractUser):
    email = models.EmailField(unique=True,)
    full_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='media',default='1.jpg')
    cover = models.ImageField(upload_to='media',default='1.jpg')


    first_name = None
    last_name = None
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =[]
    def natural_key(self):
        return dict(email=self.email)
    
    def __str__(self):
        return self.full_name
    
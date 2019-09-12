from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
# Create your models here.
class User(AbstractUser):
	mobile = models.CharField(max_length=11, validators=[MinLengthValidator(11)])


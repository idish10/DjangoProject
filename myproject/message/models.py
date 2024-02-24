from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Users(AbstractUser):
    


    """
    Represents a user in the system. Inherits from AbstractUser for built-in authentication functionalities.

    Attributes:
        name (CharField): The user's full name. (max_length=255)
        email (CharField): The user's unique email address. (max_length=255)
        password (CharField): The user's password. (max_length=255)
    """

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class MessageDetails(models.Model):
    """
    Represents a message sent between users.

    Attributes:
        receiver (CharField): The name of the message recipient. (max_length=500)
        receiver_email (CharField): The email address of the message recipient. (max_length=500)
        sender (CharField): The name of the message sender. (max_length=500)
        subject (CharField): The subject of the message. (max_length=500)
        message (CharField): The message content. (max_length=500)
        message_time (CharField): The date and time the message was sent. (max_length=500)
        is_read (CharField): Flag indicating whether the message has been read. (default: 'unread', options: 'read', 'unread')
    """
  
    receiver = models.CharField(max_length=500)
    receiver_email = models.CharField(max_length=500)
    sender = models.CharField(max_length=500)
    subject = models.CharField(max_length=500)
    message = models.CharField(max_length=500)
    message_time = models.CharField(max_length=500)
    is_read = models.CharField(max_length=500, default='unread')
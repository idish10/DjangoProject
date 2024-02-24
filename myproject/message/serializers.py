from rest_framework import serializers
from message.models import MessageDetails,Users


class UserSerializer(serializers.ModelSerializer):
    """
   
    Serializer for the Users model.

    This serializer is used for creating, updating, and retrieving user data.

    Fields:
        id (int): The unique identifier of the user.
        name (str): The user's full name.
        email (str): The user's email address (required, unique).
        password (str): The user's password (required during creation, write-only).

    """
    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Creates a new user instance.
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class MessageSerializer(serializers.ModelSerializer):
    """
   
    Serializer for the MessageDetails model.

    This serializer is used for creating, updating, and retrieving message data.

    Fields:
        receiver_email (str): The email address of the message recipient (required).
        receiver (str): The name of the message recipient.
        sender (str): The name of the message sender.
        subject (str): The subject of the message (required).
        message (str): The content of the message (required).
        message_time (str): The date and time the message was sent.
        is_read (str): Flag indicating whether the message has been read.


    """
    class Meta:
        model = MessageDetails
        fields = ['receiver_email','receiver', 'sender', 'subject','message','message_time','is_read']
       

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from message.serializers import UserSerializer,MessageSerializer
from message.models import Users,MessageDetails
import jwt, datetime
from django.db import transaction
from django.shortcuts import get_object_or_404




def get_payload(request):

    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('ExpiredSignatureError!')
    return payload
    


class LoginView(APIView):
    """
        
    Handles user login and returns a JWT token for authentication.

    **Request:**

    - POST:
        - email (str): The user's email address.
        - password (str): The user's password.

    **Response:**

    - On successful login:
        - 200 OK:
    - On authentication failure:
        - 401 Unauthorized:
            - Error message indicating "User not found!" or "Incorrect password!".

        
    """
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Users.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'email':email,
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        
        token = jwt.encode(payload, "secret", algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    

    
class RegisterView(APIView):
    """
    Registers a new user.

    **Request:**

    - POST:
        - username (str, optional): The user's username.
        - email (str): The user's email address.
        - password (str): The user's password.

    **Response:**

    - On successful registration:
        - 201 Created:
            - Serialized user data, including ID and email.
    - On validation error:
        - 400 Bad Request:
            - Error message explaining the validation errors.
            
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    
class UserView(APIView):
    """
    API view for retrieving a list of users.

    Requires valid JWT authentication.
    """

    def get(self, request):
        """
        Handles GET requests for retrieving users.

        Authenticates the user, retrieves a list of users from the database,
        serializes them, and returns them in the response.

        Raises:
            AuthenticationFailed: If the user is not authenticated or the JWT is invalid.
        """

        
        payload = get_payload(request)

        user_list = Users.objects.all()
        serialized_users = UserSerializer(user_list, many=True).data
        return Response(serialized_users)
        


class MessageView(APIView):

    def post(self, request):
        """
        Creates a new message.

        **Request:**

        - POST:
            - receiver (str): The name of the message recipient. (required)
            - receiver_email (str): The email address of the message recipient. (required)
            - sender (str): The name of the message sender. (required)
            - subject (str): The subject of the message. (required)
            - message (str): The message content. (required)

        **Response:**

        - On successful creation:
            - 201 Created:
                - Serialized message data.
        - On validation error:
            - 400 Bad Request:
                - Error message explaining the validation errors.
        - On authentication error:
            - 401 Unauthorized:
                - Error message indicating missing or invalid JWT token.

        
        
        """
        payload = get_payload(request)


             # Get current date and time
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        

        # Update request data with current time
        request.data['message_time'] = now
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response("data is not valid")
    
    def get(self, request):
        """
        Retrieves all the messages for the authenticated user.

        **Request:**

        - GET:
            - Optional: unread_messages (str): "read_only" to filter only unread messages.
            - Optional: message_by_id (int): The ID of a specific message to retrieve.


        **Response:**

        - On successful retrieval:
            - 200 OK:
                - List of serialized unread message data.
        - On authentication error:
            - 401 Unauthorized:
                - Error message indicating missing or invalid JWT token.
        """

        payload = get_payload(request)


        unread_messages = MessageDetails.objects.filter(receiver_email=payload['email'])
       

        # Check for query parameters
        unread_messages_filter = request.query_params.get('unread_messages')
        message_by_id = request.query_params.get('message_by_id')
        # Filter only unread messages if requested
        if unread_messages_filter == "unread":
            unread_messages = unread_messages.filter(is_read='unread')

       

        # Filter for a specific message by ID if requested
        if message_by_id:
            try:
                message_id = message_by_id
                unread_messages = unread_messages.filter(id=message_id)
            except ValueError:
                return Response(
                    {'message': 'Invalid message_by_id. Please provide a valid integer.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        unread_messages_list = list(unread_messages.values())

        # Update the is_read field for all unread messages
        with transaction.atomic():
            unread_messages.update(is_read='read')
           

        # Return the serialized unread messages **after** updating
        return Response(unread_messages_list)
    


    def delete(self, request):
        """
        Deletes a message.

        **Request:**

        - DELETE:
            - id_message (int): The ID of the message to delete.

        **Response:**

        - On successful deletion:
            - 200 OK:
                - {"message": "Message deleted successfully"}
        - On authentication error:
            - 401 Unauthorized:
                - Error message indicating missing or invalid JWT token.
        - On object not found:
            - 404 Not Found:
                - Error message indicating message not found or unauthorized to delete.
        """

        payload = get_payload(request)


        message_id = request.data.get('id_message')

        if not message_id:
            return Response({'message': 'Missing "id_message" in request body'}, status=400)

        try:
            message = get_object_or_404(MessageDetails, id=message_id)
        except get_object_or_404:
            return Response({'message': 'Message with ID {} not found or unauthorized to delete'.format(message_id)}, status=404)

        message.delete()
        return Response({'message': 'Message deleted successfully'})

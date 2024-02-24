# Message API Readme

This document provides a comprehensive overview of the available API endpoints within the message application.

## Authentication

To access most endpoints, valid JWT authentication is mandatory. You can obtain a JWT token by sending a POST request to `/login` with your email and password credentials.
```json
{
  "email": "user@example.com",
  "password": "password123"
}






## Registration

To register a new user, send a POST request to `/register` with the following JSON payload:

```json
{
  "username": "username123",
  "email": "user@example.com",
  "password": "password123"
}

## Endpoints

### UserView (GET):

- Requires JWT authentication.
- Retrieves a list of all registered users.

#### Response:

- List of serialized user data.

### MessageView (POST):

- Creates a new message.
- Requires JWT authentication.

#### Request:

- `receiver`: Name of the message recipient (required).
- `receiver_email`: Email address of the message recipient (required).
- `sender`: Name of the message sender (required).
- `subject`: Subject of the message (required).
- `message`: Content of the message (required).

#### Response:

- Serialized message data.

### MessageView (GET):

- Retrieves all messages for the authenticated user.
- Requires JWT authentication.

#### Optional Query Parameters:

- `unread_messages`: Set to "unread" to filter only unread messages.
- `message_by_id`: Specify the ID of a specific message to retrieve.

#### Response:

- List of serialized unread message data.

### MessageView (DELETE):

- Deletes a message.
- Requires JWT authentication.

#### Request:

- `id_message`: ID of the message to delete (required).

#### Response:

- `{"message": "Message deleted successfully"}`

## Error Handling

- Authentication errors return a 401 status code with a specific error message.
- Validation errors return a 400 status code with detailed explanations.
- Other errors return a 404 or 500 status code with an informative message.

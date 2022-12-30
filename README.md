# Flask Bookmark API

This API, written in Flask, allows users to perform several actions related to bookmarking links. The following endpoints are available:


## Summary

| Endpoint | Method | Description | Output |
|----------|--------|-------------|--------|
| `GET /users/<int:id>` | GET | Retrieve information about a specific user | User information |
| `POST /users` | POST | Create a new user | New user information |
| `POST /bookmark` | POST | Create a new bookmark | New bookmark information |
| `GET /bookmarks` | GET | Retrieve a list of all bookmarks for a user | List of bookmark objects |
| `GET /bookmark/<int:bookmark_id>` | GET | Retrieve information about a specific bookmark | Bookmark information |
| `POST /tokens` | POST | Request a new token | Token |
| `DELETE /tokens` | DELETE | Revoke current token | None |

Here are the endpoints described in detail:

## `GET /users/<int:id>`

This endpoint allows a user to retrieve information about a specific user. The user's ID is passed as a URL parameter. If the user is requesting their own information, the endpoint will return the user's email address in addition to their other information. Otherwise, only the user's name and ID will be returned. This endpoint is protected with token authentication, and can only be accessed by authorized users.

## `POST /users`

This endpoint allows a user to create a new account. The user's email and password must be included in the request body as JSON. If the email is already in use, or if the request is missing either the email or password, the endpoint will return an error. Otherwise, it will create a new user and return the new user's information.

## `POST /bookmark`

This endpoint allows a user to create a new bookmark. The bookmark's URL must be included in the request body as JSON. If the URL is invalid, the endpoint will return an error. Otherwise, it will create a new bookmark and return the new bookmark's information. This endpoint is protected with token authentication, and can only be accessed by authorized users.

## `GET /bookmarks`

This endpoint allows a user to retrieve a list of all their bookmarks. It will return a list of bookmark objects, each containing the bookmark's ID, URL, and title. This endpoint is protected with token authentication, and can only be accessed by authorized users.

## `GET /bookmark/<int:bookmark_id>`

This endpoint allows a user to retrieve information about a specific bookmark. The bookmark's ID is passed as a URL parameter. If the bookmark does not exist, or if the user has no bookmarks, the endpoint will return an error. Otherwise, it will return the bookmark's information. This endpoint is protected with token authentication, and can only be accessed by authorized users.


User data related to users and bookmarks is stored using a SQLite database created with Flask-SQLAlchemy.


This API uses Flask-HTTPAuth to protect certain endpoints with tokens, in order to restrict certain behaviors to authorized users. The following endpoints relate to the AuthN and AuthZ processes:

## `POST /tokens`

This endpoint allows a user to request a new token. The user must provide their email and password as basic authentication credentials. If the email and password are valid, a new token will be issued and returned in the response.

## `DELETE /tokens`

This endpoint allows a user to revoke their current token. The user must provide a valid token as authentication. If the token is valid, it will be revoked and the user will have to request a new token in order to access protected endpoints.
 

**Note:** This API was created for educational purposes and is not intended for production use.

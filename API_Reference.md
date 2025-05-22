# API Reference

This document provides details for each API endpoint available in the Baller project.

## Authentication

Most endpoints require JWT authentication. Obtain a token using the `/api/token/` endpoint and include it in the `Authorization` header as a Bearer token:

`Authorization: Bearer <your_access_token>`

---

## Endpoints

### 1. User Registration

- **Endpoint:** `/api/register/`
- **Method:** `POST`
- **Description:** Registers a new user.
- **Permissions:** Allow any
- **Request Body (JSON):**
  ```json
  {
    "username": "string (required)",
    "password": "string (required, write-only)",
    "password2": "string (required, write-only, must match password)",
    "email": "string (email format, required)",
    "first_name": "string (required)",
    "last_name": "string (required)"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Data received",
    "data": {
      "username": "string",
      "email": "string",
      "first_name": "string",
      "last_name": "string"
    }
  }
  ```
- **Error Response (e.g., validation error):**
  ```json
  {
    "message": "No data received",
    "error": {
      "field_name": ["Error message"]
    }
  }
  ```

### 2. Obtain JWT Token

- **Endpoint:** `/api/token/`
- **Method:** `POST`
- **Description:** Obtains JWT access and refresh tokens for a registered user. Uses `TokenObtainPairView` from `rest_framework_simplejwt`.
- **Request Body (JSON):**
  ```json
  {
    "username": "string (required)",
    "password": "string (required)"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "refresh": "string (refresh token)",
    "access": "string (access token with custom claim 'usrname')"
  }
  ```
  _(Refer to `MyTokenObtainPairSerializer` for custom claims)_
- **Error Response:** (Standard Simple JWT error responses)

### 3. Refresh JWT Token

- **Endpoint:** `/api/token/refresh/`
- **Method:** `POST`
- **Description:** Refreshes an expired JWT access token. Uses `TokenRefreshView` from `rest_framework_simplejwt`.
- **Request Body (JSON):**
  ```json
  {
    "refresh": "string (valid refresh token, required)"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "access": "string (new access token)"
  }
  ```
- **Error Response:** (Standard Simple JWT error responses)

### 4. User Profiles

- **Endpoint:** `/api/users/`
- **Description:** Manage user profiles.
- **Permissions (GET):** Allow any (based on commented out auth in view, confirm if auth is intended)
  - **Note:** POST method is commented out in `UsersProfileView`.
- **Serializer:** `UserProfileSerializer`
  - **Fields:** `user_id` (CharField, required on POST), `address` (PrimaryKeyRelatedField to Address, optional), `wishlist` (PrimaryKeyRelatedField to Book, many=True), `favorite_authors` (PrimaryKeyRelatedField to Author, many=True), `favorite_categories` (PrimaryKeyRelatedField to Category, many=True), `favorite_tags` (PrimaryKeyRelatedField to Tag, many=True). _(Refer to `UserProfile` model for underlying structure)._

#### GET `/api/users/`

- **Description:** Retrieves a list of all user profiles.
- **Success Response (200 OK):**
  ```json
  [
    {
      "user_id": "string",
      "address": "integer (ID of Address object) / null",
      "wishlist": ["integer (ID of Book object)"],
      "favorite_authors": ["integer (ID of Author object)"],
      "favorite_categories": ["integer (ID of Category object)"],
      "favorite_tags": ["integer (ID of Tag object)"]
    }
    // ... more user profiles
  ]
  ```

### 5. User Address

- **Endpoint:** `/api/address/`
- **Description:** Manage user addresses.
- **Permissions:** IsAuthenticated (JWT Authentication)
- **Serializer:** `AddressSerializer`
  - **Fields:** `pin_code` (integer, 6 digits), `sub_address` (string), `city` (string), `district` (string), `state` (string). `user_id` is automatically handled or required based on context. _(Refer to `Address` model for underlying structure and `AddressSerializer` for create/update logic and validations like `pin_code` length)._

#### GET `/api/address/`

- **Description:** Retrieves the address of the authenticated user.
- **Success Response (200 OK):**
  ```json
  {
    "id": "integer",
    "pin_code": "integer",
    "sub_address": "string",
    "city": "string",
    "district": "string",
    "state": "string"
    // user_id is not part of the response for GET
  }
  ```
- **Response if no address found (200 OK with message):**
  ```json
  {
    "message": "No address found"
  }
  ```

#### POST `/api/address/`

- **Description:** Creates or updates the address for the authenticated user.
- **Request Body (JSON):**
  ```json
  {
    "pin_code": "integer (required, 6 digits)",
    "sub_address": "string (required)",
    "city": "string (required)",
    "district": "string (required)",
    "state": "string (required)"
    // user_id is added internally from the authenticated user
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Data received",
    "data": {
      // Note: The serializer's create method returns validated_data, which might not include the 'id' of the address immediately after creation. Confirm actual response structure.
      "pin_code": "integer",
      "sub_address": "string",
      "city": "string",
      "district": "string",
      "state": "string",
      "user_id": "string (user's ID)"
    }
  }
  ```
- **Error Response (e.g., validation error):**
  ```json
  {
    "message": "No data received",
    "error": {
      "field_name": ["Error message"]
    }
  }
  ```

### 6. Books

- **Endpoint:** `/api/books/`
- **Description:** Manage books.
- **Permissions:** Allow any (based on commented out auth in view, confirm if auth is intended for POST)
- **Serializer:** `BookSerializer`
  - **Fields:** `title`, `description`, `isbn`, `publication_date`, `price`, `stock_quantity`, `cover_image`, `author` (PrimaryKeyRelatedField, many=True to Author), `tags` (PrimaryKeyRelatedField, many=True to Tag), `category` (PrimaryKeyRelatedField to Category), `language` (PrimaryKeyRelatedField to Language), `publisher` (PrimaryKeyRelatedField to Publisher). _(Refer to `Book` model for field types and `BookSerializer` for how relations are handled)._

#### GET `/api/books/`

- **Description:** Retrieves a list of all books.
- **Success Response (200 OK):**
  ```json
  [
    {
      "id": "integer",
      "title": "string",
      "description": "string",
      "isbn": "string",
      "publication_date": "date",
      "price": "decimal",
      "stock_quantity": "integer",
      "cover_image": "url/path to image",
      "author": ["integer (ID of Author object)"],
      "tags": ["integer (ID of Tag object)"],
      "category": "integer (ID of Category object)",
      "language": "integer (ID of Language object)",
      "publisher": "integer (ID of Publisher object)"
    }
    // ... more books
  ]
  ```

#### POST `/api/books/`

- **Description:** Creates a new book.
- **Request Body (JSON):**
  ```json
  {
    "title": "string (required)",
    "description": "string (optional)",
    "isbn": "string (required, unique)",
    "publication_date": "date (YYYY-MM-DD, required)",
    "price": "decimal (required)",
    "stock_quantity": "integer (required)",
    "cover_image": "image file (optional)",
    "author": ["integer (ID of Author object, required)"],
    "tags": ["integer (ID of Tag object, optional)"],
    "category": "integer (ID of Category object, required)",
    "language": "integer (ID of Language object, required)",
    "publisher": "integer (ID of Publisher object, required)"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Data received",
    "data": {
      "id": "integer",
      "title": "string"
      // ... other book fields including relational IDs
    }
  }
  ```
- **Error Response (e.g., validation error):**
  ```json
  {
    "message": "No data received",
    "error": {
      "field_name": ["Error message"]
    }
  }
  ```

### 7. Authors

- **Endpoint:** `/api/authors/`
- **Description:** Manage authors.
- **Permissions:** IsAuthenticated (JWT Authentication)
- **Serializer:** `AuthorSerializer` (fields: `__all__`)
  - _(Refer to `Author` model for all fields: `name`, `bio`, `profile_picture`, `date_of_birth`, `nationality`)_

#### GET `/api/authors/`

- **Description:** Retrieves a list of all authors.
- **Success Response (200 OK):**
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "bio": "string",
      "profile_picture": "url/path to image",
      "date_of_birth": "date",
      "nationality": "string"
    }
    // ... more authors
  ]
  ```

#### POST `/api/authors/`

- **Description:** Creates a new author.
- **Request Body (JSON):**
  ```json
  {
    "name": "string (required)",
    "bio": "string (optional)",
    "profile_picture": "image file (optional)",
    "date_of_birth": "date (YYYY-MM-DD, optional)",
    "nationality": "string (optional)"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Data received",
    "data": {
      "id": "integer",
      "name": "string"
      // ... other author fields
    }
  }
  ```
- **Error Response (e.g., validation error):**
  ```json
  {
    "message": "No data received",
    "error": {
      "field_name": ["Error message"]
    }
  }
  ```

### 8. Languages

- **Endpoint:** `/api/languages/`
- **Description:** Manage languages.
- **Permissions:** Allow any (based on commented out auth in view, confirm if auth is intended for POST)
- **Serializer:** `LanguageSerializer` (fields: `__all__`)
  - _(Refer to `Language` model for all fields: `name`, `code`)_

#### GET `/api/languages/`

- **Description:** Retrieves a list of all languages.
- **Success Response (200 OK):**
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "code": "string"
    }
    // ... more languages
  ]
  ```

#### POST `/api/languages/`

- **Description:** Creates a new language.
- **Request Body (JSON):**
  ```json
  {
    "name": "string (required)",
    "code": "string (required, e.g., 'en', 'es')"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Data received",
    "data": {
      "id": "integer",
      "name": "string",
      "code": "string"
    }
  }
  ```
- **Error Response (e.g., validation error):**
  ```json
  {
    "message": "No data received",
    "error": {
      "field_name": ["Error message"]
    }
  }
  ```

### 9. Publishers

- **Endpoint:** `/api/publishers/`
- **Description:** Manage publishers.
- **Permissions:** Allow any (based on commented out auth in view, confirm if auth is intended for POST)
- **Serializer:** `PublisherSerializer` (fields: `__all__`)
  - _(Refer to `Publisher` model for all fields: `name`, `address`, `website`)_

#### GET `/api/publishers/`

- **Description:** Retrieves a list of all publishers.
- **Success Response (200 OK):**
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "address": "string",
      "website": "url string"
    }
    // ... more publishers
  ]
  ```

#### POST `/api/publishers/`

- **Description:** Creates a new publisher.
- **Request Body (JSON):**
  ```json
  {
    "name": "string (required)",
    "address": "string (optional)",
    "website": "url string (optional)"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Data received",
    "data": {
      "id": "integer",
      "name": "string"
      // ... other publisher fields
    }
  }
  ```
- **Error Response (e.g., validation error):**
  ```json
  {
    "message": "No data received",
    "error": {
      "field_name": ["Error message"]
    }
  }
  ```

### 10. Categories

- **Endpoint:** `/api/categories/`
- **Description:** Manage categories.
- **Permissions:** Allow any (based on commented out auth in view, confirm if auth is intended for POST)
- **Serializer:** `CategorySerializer` (fields: `__all__`)
  - _(Refer to `Category` model for all fields: `name`, `description`)_

#### GET `/api/categories/`

- **Description:** Retrieves a list of all categories.
- **Success Response (200 OK):**
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "description": "string"
    }
    // ... more categories
  ]
  ```

#### POST `/api/categories/`

- **Description:** Creates a new category.
- **Request Body (JSON):**
  ```json
  {
    "name": "string (required)",
    "description": "string (optional)"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Data received",
    "data": {
      "id": "integer",
      "name": "string",
      "description": "string"
    }
  }
  ```
- **Error Response (e.g., validation error):**
  ```json
  {
    "message": "No data received",
    "error": {
      "field_name": ["Error message"]
    }
  }
  ```

### 11. Tags

- **Endpoint:** `/api/tags/`
- **Description:** Manage tags.
- **Permissions:** Allow any (based on commented out auth in view, confirm if auth is intended for POST)
- **Serializer:** `TagSerializer` (fields: `__all__`)
  - _(Refer to `Tag` model for all fields: `name`)_

#### GET `/api/tags/`

- **Description:** Retrieves a list of all tags.
- **Success Response (200 OK):**
  ```json
  [
    {
      "id": "integer",
      "name": "string"
    }
    // ... more tags
  ]
  ```

#### POST `/api/tags/`

- **Description:** Creates a new tag.
- **Request Body (JSON):**
  ```json
  {
    "name": "string (required)"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "message": "Data received",
    "data": {
      "id": "integer",
      "name": "string"
    }
  }
  ```
- **Error Response (e.g., validation error):**
  ```json
  {
    "message": "No data received",
    "error": {
      "field_name": ["Error message"]
    }
  }
  ```

---

_Note: For serializers with `fields = '__all__'`, please refer to the corresponding model definition in `main/models.py` for a complete list of fields and their types. Some endpoints have authentication commented out in `main/views.py`; their actual permission requirements should be confirmed and updated here if necessary._

# Baller

**Baller** is a robust backend application built with Django and Django REST Framework. It provides a comprehensive RESTful API for managing an online bookstore, including functionalities for books, authors, user profiles, authentication, and more. This project serves as a foundational platform for e-commerce solutions centered around literature.

## Features

- User registration and authentication (JWT-based)
- Manage user profiles and addresses
- Manage books, authors, languages, publishers, categories, and tags

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** SQLite (default, configurable)
- **Authentication:** JWT (JSON Web Tokens) via `djangorestframework-simplejwt`
- **Image Handling:** Pillow

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/thisisdkyadav/Baller.git
    cd baller
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

## API Endpoints

The following API endpoints are available under the `/api/` prefix:

- `/users/`: Manage user profiles.
- `/address/`: Manage user addresses.
- `/books/`: Manage books.
- `/authors/`: Manage authors.
- `/languages/`: Manage languages.
- `/publishers/`: Manage publishers.
- `/categories/`: Manage categories.
- `/register/`: User registration.
- `/tags/`: Manage tags.
- `/token/`: Obtain JWT token.
- `/token/refresh/`: Refresh JWT token.

For detailed information on each endpoint, including request/response formats and parameters, please see the [API Reference](API_Reference.md).

## Dependencies

- asgiref==3.8.1
- Django==5.1
- djangorestframework==3.15.2
- djangorestframework-simplejwt==5.3.1
- pillow==11.2.1
- PyJWT==2.10.1
- sqlparse==0.5.3
- tzdata==2025.2

## Contributing

Contributions are welcome! If you'd like to contribute to Baller, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a pull request.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

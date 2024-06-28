# My Django Project

This is a Django project that includes functionality for posting and viewing posts and reels, with a search feature for finding users and their posts/reels.

## Features

- Add and view posts
- Add and view reels
- Search for posts and reels by caption
- Search for users and view their posts and reels

## Prerequisites

- Python 3.x
- Django 3.x or higher
- Git

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/my-django-project.git
    cd my-django-project
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

7. **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:8000`.

## Usage

### Adding Posts and Reels

- Log in with your superuser account.
- Navigate to the `Add Post` or `Add Reel` page to upload new content.

### Searching

- Use the search bar on the home page to search for posts and reels by caption.
- Use the user search bar to find specific users and view their posts and reels.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

1. Fork the repository
2. Create a branch: `git checkout -b feature-branch`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch`
5. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

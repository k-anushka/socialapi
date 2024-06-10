# Social Network API

This project is a social networking API built with Django and Django Rest Framework (DRF). It includes user registration, login functionality, and various social features like searching for users, sending/accepting/rejecting friend requests, listing friends, and pending friend requests.

## Features

- User registration with email and password.
- User login with email and password (case insensitive).
- Search for other users by email or name (paginated, up to 10 records per page).
- Send, accept, or reject friend requests.
- List friends (users who have accepted friend requests).
- List pending friend requests (received but not yet accepted/rejected).
- Limit of 3 friend requests per minute.

## Installation

### Prerequisites

- Python 3.11.1+
- Django 5.0.6+
- Django Rest Framework 3.15.1+
- Django Rest Framework SimpleJWT

### Steps

1. Clone the repository:

   git clone  https://github.com/k-anushka/socialapi.git
   
   cd socialapi

3. Run the project:

     a. python manage.py makemigrations
     
     b. python manage.py migrate
     
     c. python manage.py runserver



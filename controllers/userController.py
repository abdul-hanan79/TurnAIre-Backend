from flask import Blueprint, render_template

# Define a blueprint for user-related routes
users_bp = Blueprint('users', __name__)

# Route for the users page
@users_bp.route('/')
def users():
    return 'Hello, World! user'

# Another route for creating users
@users_bp.route('/create', methods=['POST'])
def create_user():
    return "User Created!"

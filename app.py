from flask import Flask
from controllers.userController import users_bp  # Make sure the import is correct

app = Flask(__name__)

# Register the users blueprint
app.register_blueprint(users_bp, url_prefix='/users')  # All user routes will be prefixed with /users

# Define other routes
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug=True)

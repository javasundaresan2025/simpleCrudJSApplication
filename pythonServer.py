from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage (replace with database in production)
users = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'age': 30},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'age': 25},
    {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com', 'age': 35}
]

next_id = 4

def find_user_by_id(user_id):
    """Find user by ID helper function"""
    return next((user for user in users if user['id'] == int(user_id)), None)

def find_user_by_email(email, exclude_id=None):
    """Find user by email helper function"""
    for user in users:
        if user['email'] == email:
            if exclude_id is None or user['id'] != exclude_id:
                return user
    return None

@app.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    print("Inside get")
    
    return jsonify({
        'success': True,
        'data': users,
        'count': len(users)
    })

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get particular user by ID"""
    user = find_user_by_id(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': user
    })

@app.route('/users', methods=['POST'])
def create_user():
    """Create new user"""
    global next_id
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': 'No data provided'
        }), 400
    
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    
    # Basic validation
    if not name or not email or not age:
        return jsonify({
            'success': False,
            'message': 'Name, email, and age are required'
        }), 400
    
    # Check if email already exists
    if find_user_by_email(email):
        return jsonify({
            'success': False,
            'message': 'Email already exists'
        }), 400
    
    new_user = {
        'id': next_id,
        'name': name,
        'email': email,
        'age': int(age)
    }
    
    users.append(new_user)
    next_id += 1
    
    return jsonify({
        'success': True,
        'message': 'User created successfully',
        'data': new_user
    }), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    user = find_user_by_id(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': 'No data provided'
        }), 400
    
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    
    # Basic validation
    if not name or not email or not age:
        return jsonify({
            'success': False,
            'message': 'Name, email, and age are required'
        }), 400
    
    # Check if email already exists (excluding current user)
    existing_user = find_user_by_email(email, exclude_id=user['id'])
    if existing_user:
        return jsonify({
            'success': False,
            'message': 'Email already exists'
        }), 400
    
    # Update user properties
    user['name'] = name
    user['email'] = email
    user['age'] = int(age)
    
    return jsonify({
        'success': True,
        'message': 'User updated successfully',
        'data': user
    })

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    global users
    
    user_index = -1
    for i, user in enumerate(users):
        if user['id'] == user_id:
            user_index = i
            break
    
    if user_index == -1:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404
    
    deleted_user = users.pop(user_index)
    
    return jsonify({
        'success': True,
        'message': 'User deleted successfully',
        'data': deleted_user
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Route not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': 'Something went wrong!'
    }), 500

if __name__ == '__main__':
    print("Server is running on port 3000")
    print("Try the following endpoints:")
    print("GET    http://localhost:3000/users")
    print("GET    http://localhost:3000/users/1")
    print("POST   http://localhost:3000/users")
    print("PUT    http://localhost:3000/users/1")
    print("DELETE http://localhost:3000/users/1")
    
    app.run(host='0.0.0.0', port=3000, debug=True)
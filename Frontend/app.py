from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key in production

# In-memory storage (replace with a proper database in production)
users = {
    'educator@example.com': {
        'password': generate_password_hash('educator123'),
        'role': 'educator'
    },
    'student@example.com': {
        'password': generate_password_hash('student123'),
        'role': 'student'
    }
}

exams = [
    {
        'id': 1,
        'name': 'Mathematics',
        'examDate': '2024-04-15',
        'status': 'Upcoming',
        'students': 45,
        'topics': 12
    },
    {
        'id': 2,
        'name': 'Physics',
        'examDate': '2024-04-18',
        'status': 'Upcoming',
        'students': 38,
        'topics': 10
    }
]

students = [
    {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@example.com',
        'subjects': ['Mathematics', 'Physics']
    },
    {
        'id': 2,
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'subjects': ['Mathematics', 'Chemistry']
    }
]

# JWT token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users.get(data['email'])
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Authentication routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')  # Default role is student
    
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    if email in users:
        return jsonify({'message': 'User already exists'}), 400
    
    users[email] = {
        'password': generate_password_hash(password),
        'role': role
    }
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = users.get(email)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'email': email,
        'role': user['role'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'role': user['role'],
        'email': email
    })

@app.route('/api/logout', methods=['POST'])
@token_required
def logout(current_user):
    # In a real application, you might want to blacklist the token
    return jsonify({'message': 'Logged out successfully'})

# Protected exam routes
@app.route('/api/exams', methods=['GET'])
@token_required
def get_exams(current_user):
    return jsonify(exams)

@app.route('/api/exams', methods=['POST'])
@token_required
def create_exam(current_user):
    if current_user['role'] != 'educator':
        return jsonify({'message': 'Only educators can create exams'}), 403
    
    if not request.is_json:
        return jsonify({'error': 'Invalid request'}), 400
    
    data = request.json
    new_exam = {
        'id': len(exams) + 1,
        'name': data['name'],
        'examDate': data['examDate'],
        'status': 'Upcoming',
        'students': data['students'],
        'topics': data['topics']
    }
    exams.append(new_exam)
    return jsonify(new_exam), 201

@app.route('/api/exams/<int:exam_id>', methods=['GET'])
def get_exam(exam_id):
    exam = next((e for e in exams if e['id'] == exam_id), None)
    if exam:
        return jsonify(exam)
    return jsonify({'error': 'Exam not found'}), 404

@app.route('/api/exams/<int:exam_id>', methods=['PUT'])
def update_exam(exam_id):
    data = request.json
    exam = next((e for e in exams if e['id'] == exam_id), None)
    if exam:
        exam.update(data)
        return jsonify(exam)
    return jsonify({'error': 'Exam not found'}), 404

@app.route('/api/exams/<int:exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    exam = next((e for e in exams if e['id'] == exam_id), None)
    if exam:
        exams.remove(exam)
        return '', 204
    return jsonify({'error': 'Exam not found'}), 404

# Student routes
@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({'error': 'Student not found'}), 404

@app.route('/api/students/<int:student_id>/subjects', methods=['GET'])
def get_student_subjects(student_id):
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return jsonify(student['subjects'])
    return jsonify({'error': 'Student not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
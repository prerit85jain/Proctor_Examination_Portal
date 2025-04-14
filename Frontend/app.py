from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory storage (replace with a proper database in production)
users = {
    'educator@example.com': {
        'password': 'educator123',
        'role': 'educator'
    },
    'student@example.com': {
        'password': 'student123',
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

# Authentication routes
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = users.get(email)
    if user and user['password'] == password:
        return jsonify({
            'success': True,
            'role': user['role'],
            'email': email
        })
    
    return jsonify({
        'success': False,
        'message': 'Invalid credentials'
    }), 401

# Exam routes
@app.route('/api/exams', methods=['GET'])
def get_exams():
    return jsonify(exams)

@app.route('/api/exams', methods=['POST'])
def create_exam():
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
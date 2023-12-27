from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:110515@localhost:3306/employee'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Person(db.Model):
    __tablename__ = 'person'
    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    birthdate = db.Column(db.Date)
    hire_date = db.Column(db.Date)
    salary = db.Column(db.DECIMAL(10, 2))
    department_id = db.Column(db.Integer)
    is_manager = db.Column(db.Boolean)

# Create a new person
@app.route('/api/person', methods=['POST'])
def create_person():
    data = request.get_json()
    new_person = Person(**data)
    db.session.add(new_person)
    db.session.commit()
    return jsonify({'message': 'Person created successfully'}), 201

# Retrieve all persons
@app.route('/api/person', methods=['GET'])
def get_all_persons():
    persons = Person.query.all()
    result = [
        {
            'person_id': person.person_id,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'email': person.email,
            'phone_number': person.phone_number,
            'birthdate': str(person.birthdate),
            'hire_date': str(person.hire_date),
            'salary': str(person.salary),
            'department_id': person.department_id,
            'is_manager': person.is_manager,
        }
        for person in persons
    ]
    return jsonify(result)

# Retrieve a specific person by ID
@app.route('/api/person/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = Person.query.get(person_id)
    if person is None:
        abort(404, 'Person not found')
    result = {
        'person_id': person.person_id,
        'first_name': person.first_name,
        'last_name': person.last_name,
        'email': person.email,
        'phone_number': person.phone_number,
        'birthdate': str(person.birthdate),
        'hire_date': str(person.hire_date),
        'salary': str(person.salary),
        'department_id': person.department_id,
        'is_manager': person.is_manager,
    }
    return jsonify(result)

# Update a specific person by ID
@app.route('/api/person/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    person = Person.query.get(person_id)
    if person is None:
        abort(404, 'Person not found')
    
    data = request.get_json()
    person.first_name = data.get('first_name', person.first_name)
    # Update other fields similarly
    
    db.session.commit()
    return jsonify({'message': 'Person updated successfully'})

# Delete a specific person by ID
@app.route('/api/person/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    person = Person.query.get(person_id)
    if person is None:
        abort(404, 'Person not found')
    
    db.session.delete(person)
    db.session.commit()
    return jsonify({'message': 'Person deleted successfully'})

# Other routes remain unchanged
# XML Formatting logic remains unchanged
# Search functionality remains unchanged

# User Loader Callback and Error Handler remain unchanged

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

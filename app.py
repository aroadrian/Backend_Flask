from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_backend:admin@localhost/basic_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, disables a warning

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Event {self.description}>"
    
    def __init__(self, description):
        self.description = description

def format_event(event):
    return {
        'description': event.description,
        'id': event.id,
        'created_at': event.created_at
    }

# Define a simple route
@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/events', methods=['POST']) 
def create_event():
    description = request.json['description']
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    return format_event(event)

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.order_by(Event.id.asc()).all()
    event_list =[]
    for event in events:
        event_list.append(format_event(event))
    return {'events': event_list}

@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.filter_by(id=id).one()
    formattted_event = format_event(event)
    return {'event': formattted_event}


@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.filter_by(id=id).one()
    db.session.delete(event)
    db.session.commit()
    return {'message': 'Event deleted successfully'}


@app.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    event = Event.query.filter_by(id=id)
    description = request.json['description']
    event.update(dict(description=description, created_at=datetime.utcnow()))
    db.session.commit()
    return {'event': format_event(event.one())}


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([message.to_dict() for message in messages]), 200
    except Exception as e:
        return jsonify({'error': f'Error retrieving messages: {str(e)}'}), 500

# POST route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    try:
        data = request.get_json()
        if 'body' not in data or 'username' not in data:
            return jsonify({'error': 'Missing required data: body and username'}), 400

        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.to_dict()), 201
    except Exception as e:
        return jsonify({'error': f'Error creating message: {str(e)}'}), 500

# PATCH route to update the body of a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    try:
        message = Message.query.get(id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404

        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
            db.session.commit()

        return jsonify(message.to_dict()), 200
    except Exception as e:
        return jsonify({'error': f'Error updating message: {str(e)}'}), 500

# DELETE route to delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    try:
        message = Message.query.get(id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404

        db.session.delete(message)
        db.session.commit()

        return jsonify({'message': 'Message deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Error deleting message: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5555)

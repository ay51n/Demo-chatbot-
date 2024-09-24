from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import uuid

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['project_chatbot']
conversations = db['conversation']

# Categories and corresponding items
categories= {
    'Électronique': ['smartphone', 'phone', 'mobile', 'laptop', 'computer', 'camera', 'headphones', 'speaker', 'tablet'],
    'Loisirs': ['game', 'console', 'puzzle', 'card game', 'board game', 'sport equipment'],
    'Bien-être': ['fitness tracker', 'yoga mat', 'treadmill', 'dumbbell', 'gym membership'],
    'Cuisine': ['blender', 'microwave', 'cookbook', 'knife set', 'grill'],
    'Voyage': ['luggage', 'backpack', 'travel guide', 'plane ticket', 'travel pillow'],
    'Maison': ['furniture', 'bedding', 'tool kit', 'lighting', 'home decor'],
    'Financier': ['bank account', 'credit card', 'investment fund', 'stock market', 'cryptocurrency'],
    'Éducation': ['textbook', 'online course', 'study guide', 'educational app', 'stationery'],
    'Animaux de compagnie': ['pet food', 'leash', 'aquarium', 'pet toy', 'grooming service'],
    'Sport': ['football', 'basketball', 'tennis', 'soccer', 'baseball', 'volleyball', 'swimming', 'golf', 'cycling', 'running'],
    'Mode': ['clothing', 'shoes', 'accessories', 'handbags', 'jewelry', 'watches','bag']
}

greetings = ['hi', 'hello', 'hey', 'good morning', 'salut', 'greetings']

def find_items(message):
    """ Return items related to the message. """
    message = message.lower()
    items = []
    for category, items_list in categories.items():
        items += [item for item in items_list if item in message]
    return items


def log_conversation(sender_id, address, text, speaker):

    timestamp = int(datetime.utcnow().timestamp())
    event = {
        'event': speaker,
        'timestamp': timestamp,
        'text': text,
        
        'address': address
    }
    # Update MongoDB document
    conversations.update_one({'sender_id': sender_id}, {'$push': {'events': event}}, upsert=True)


@app.route('/')
def index():
    """ Render the chat interface from a static HTML file. """
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    address = request.form['address']
    sender_id = request.form.get('sender_id', str(uuid.uuid4()))

    log_conversation(sender_id, address, message, 'user')

    if any(greet in message.lower() for greet in greetings):
        response_message = "Hello! How can I assist you today?"
    else:
        related_items = find_items(message)
        response_message = f"Here are some items related to your interest: {', '.join(related_items)}" if related_items else "I'm sorry, I couldn't find any related items."

    log_conversation(sender_id, address, response_message, 'bot')

    return jsonify({'message': response_message, 'sender_id': sender_id, 'address': address})

@app.route('/new_conversation', methods=['GET'])
def new_conversation():
    sender_id = str(uuid.uuid4())
    address = request.args.get('address', '')
    conversations.insert_one({'sender_id': sender_id, 'address': address, 'events': []})
    return jsonify({'sender_id': sender_id, 'address': address})

if __name__ == '__main__':
    app.run(debug=True)

# Flask Chatbot with MongoDB

This is a simple Flask-based chatbot that processes user messages, identifies relevant items based on predefined categories, and stores conversation logs in a MongoDB database.

## Features
- **Message Logging**: Stores conversations (user and bot responses) in a MongoDB database.
- **Item Recognition**: Detects relevant items mentioned in user messages from predefined categories.
- **Greet Recognition**: The bot responds to common greetings with a friendly message.
- **RESTful API**: Provides endpoints for sending and receiving messages in a conversation, starting new conversations, and rendering the chat interface.

## Technologies Used
- **Python**: The core language used for backend development.
- **Flask**: A lightweight web framework for handling HTTP requests and serving the chatbot interface.
- **MongoDB**: Used to store conversation data, including user messages and bot responses.
- **HTML/CSS/JavaScript**: For rendering the chat interface (to be developed as `index.html`).

## Setup Instructions

### Prerequisites
- **Python 3.x** installed on your system.
- **MongoDB** installed and running locally (or a MongoDB URI if using a remote instance).

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/flask-chatbot-mongodb.git](https://github.com/ay51n/Demo-chatbot-)
   cd Demo-chatbot-

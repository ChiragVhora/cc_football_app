If you want to integrate a single page with a Socket.IO server into your existing Flask project, you can follow these steps:

Create a Blueprint (Optional but Recommended):
In your Flask project, you can create a Blueprint to encapsulate the routes and logic related to the Socket.IO functionality.
This keeps your project organized and modular.
python
Copy code
# socket_bp.py

from flask import Blueprint, render_template
from flask_socketio import SocketIO

socket_bp = Blueprint('socket', __name__)
socketio = SocketIO()

@socket_bp.route('/your_socket_page')
def socket_page():
    return render_template('socket_page.html')
Create the Socket.IO Logic:
In your Blueprint, you can define the Socket.IO events and logic.
This includes handling connections, messages, emitting events, etc.
Note that the socketio object should be initialized with the Flask app instance.
python
Copy code
# socket_bp.py

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('custom_event')
def handle_custom_event(data):
    # Handle the data and emit response
    response_data = {'message': 'Response from server'}
    socketio.emit('response_event', response_data)
Create the Socket.IO HTML Page:
Create an HTML template for your Socket.IO page.
Include the necessary JavaScript to connect to the Socket.IO server and handle events.
html
Copy code
<!-- socket_page.html -->

<!DOCTYPE html>
<html>
<head>
    <!-- Include necessary scripts and CSS -->
</head>
<body>
    <!-- Your page content -->

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.1.3/socket.io.js"></script>
    <script>
        // Connect to the Socket.IO server
        const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

        // Event listener for custom_event
        socket.on('response_event', data => {
            console.log('Received response:', data);
        });

        // Emit a custom_event to the server
        socket.emit('custom_event', { message: 'Hello from client' });
    </script>
</body>
</html>
Integrate the Blueprint in Your App:
In your main Flask app, register the Blueprint and initialize the socketio object with your app instance.
python
Copy code
# app.py

from flask import Flask
from socket_bp import socket_bp
from flask_socketio import SocketIO

app = Flask(__name__)
app.register_blueprint(socket_bp)
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app, debug=True)
Run Your Flask App:
Run your Flask app with socketio.run() as usual.
Now, you have integrated a Socket.IO page into your existing Flask project using a Blueprint. This allows you to keep the Socket.IO functionality separated from the rest of your project and manage the Socket.IO connections and events effectively. Remember to adjust the routes, events, and page content to match your specific use case.
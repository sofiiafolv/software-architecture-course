from flask import jsonify, Flask
import argparse
import hazelcast

class MessagesController:
    def __init__(self):
        self.messages_service = Flask(__name__)

        @self.messages_service.route('/messages_service', methods=['GET'])
        def get_message():
            return jsonify("not implemented yet")

    def run(self, messaging_port):
        self.messages_service.run(port=messaging_port, debug=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('messaging_port')  
    args = parser.parse_args()

    messages_controller = MessagesController()
    messages_controller.run(args.messaging_port)

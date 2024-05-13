from flask import jsonify, Flask


class MessagesController:
    def __init__(self):
        self.messages_service = Flask(__name__)

        @self.messages_service.route('/messages_service', methods=['GET'])
        def get_message():
            return jsonify("not implemented yet")

    def run(self):
        self.messages_service.run(port=8082, debug=True)


if __name__ == "__main__":
    messages_controller = MessagesController()
    messages_controller.run()

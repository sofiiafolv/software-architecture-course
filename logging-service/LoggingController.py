from flask import jsonify, request, Flask, make_response


class LoggingController:
    def __init__(self):
        self.logging_service = Flask(__name__)
        self.messages = {}

        @self.logging_service.route('/logging_service', methods=['POST'])
        def post_request():
            data = request.get_json()
            print("Received:", data)
            unique_uuid = data['uuid']
            msg = data['msg']
            self.messages[unique_uuid] = msg
            print("Message received: " + msg + ". Saved with unique id: " + unique_uuid)
            return '', 200

        @self.logging_service.route('/logging_service', methods=['GET'])
        def get_response():
            return jsonify(list(self.messages.values()))

    def run(self):
        self.logging_service.run(port=8081, debug=True)


if __name__ == '__main__':
    app = LoggingController()
    app.run()

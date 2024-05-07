from flask import jsonify, request, Flask, make_response
import argparse
import hazelcast

class LoggingController:
    def __init__(self):
        self.logging_service = Flask(__name__)
        self.client = hazelcast.HazelcastClient()
        self.messages_map = self.client.get_map("logging_service_messages").blocking()

        @self.logging_service.route('/logging_service', methods=['POST'])
        def post_request():
            data = request.get_json()
            print("Received:", data)
            unique_uuid = data['uuid']
            msg = data['msg']
            self.messages_map.put(unique_uuid, msg)
            print("Message received: " + msg + ". Saved with unique id: " + unique_uuid)
            return '', 200

        @self.logging_service.route('/logging_service', methods=['GET'])
        def get_response():
            return jsonify(list(self.messages_map.values()))

    def run(self, logging_port):
        try:
            self.logging_service.run(port=logging_port, debug=True)
        finally:
            self.client.shutdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('logging_port')  
    args = parser.parse_args()

    app = LoggingController()
    app.run(args.logging_port)

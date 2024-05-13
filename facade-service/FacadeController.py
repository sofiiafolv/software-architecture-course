from flask import jsonify, request, Flask, make_response
import requests
import uuid
import random
import os

LOGGING_SERVICES_NUMBER = int(os.getenv("LOGGING_SERVICES_NUMBER"))

class FacadeController:
    def __init__(self):
        self.facade_service = Flask(__name__)
        self.logging_ports = [8001 + i for i in range(LOGGING_SERVICES_NUMBER)]

        @self.facade_service.route('/facade_service', methods=['POST'])
        def post_request():
            data = request.get_json()
            print(data)
            unique_uuid = str(uuid.uuid4())
            requests.post(f'http://localhost:{random.choice(self.logging_ports)}/logging_service', json={'uuid': unique_uuid, 'msg': data})
            return '', 200

        @self.facade_service.route('/facade_service', methods=['GET'])
        def get_response():
            logging_service_response = requests.get(f'http://localhost:{random.choice(self.logging_ports)}/logging_service')
            message_service_response = requests.get('http://localhost:8082/messages_service')

            return jsonify(logging_service_response.json(), message_service_response.json())

    def run(self):
        self.facade_service.run(port=8081, debug=True)


if __name__ == '__main__':
    facade = FacadeController()
    facade.run()

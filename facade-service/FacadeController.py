from flask import jsonify, request, Flask, make_response
import requests
import uuid
import random
import hazelcast
import argparse
import consul

class FacadeController:
    def __init__(self, ip_address, facade_port):
        self.facade_service = Flask(__name__)
        # self.logging_ports = [8082, 8083, 8084]
        # self.messaging_ports = [8085, 8086]
        # self.messaging_queue = self.client.get_queue("messaging_queue")
        self.consul_service = consul.Consul()
        self.ip_address = ip_address
        self.facade_port = facade_port
        self.consul_service.agent.service.register('facade-service', service_id='facade-service-' + facade_port, port=int(facade_port), address=ip_address)

        self.client_name = self.consul_service.kv.get('cluster-name')[1]['Value'].decode()
        self.client = hazelcast.HazelcastClient(cluster_name=self.client_name)

        self.messaging_queue_name = self.consul_service.kv.get('queue-name')[1]['Value'].decode()
        self.messaging_queue = self.client.get_queue(self.messaging_queue_name)

        @self.facade_service.route('/facade_service', methods=['POST'])
        def post_request():
            data = request.get_json()
            print(data)
            unique_uuid = str(uuid.uuid4())
            self.messaging_queue.put(data)

            logging_service = random.choice(self.consul_service.health.service('logging-service')[1])
            logging_ip_address = logging_service['Service']['Address']
            logging_port = logging_service['Service']['Port']
            requests.post(f'http://{logging_ip_address}:{logging_port}/logging_service', json={'uuid': unique_uuid, 'msg': data})
            return '', 200

        @self.facade_service.route('/facade_service', methods=['GET'])
        def get_response():
            logging_service = random.choice(self.consul_service.health.service('logging-service')[1])
            logging_ip_address = logging_service['Service']['Address']
            logging_port = logging_service['Service']['Port']

            messages_service = random.choice(self.consul_service.health.service('messages-service')[1])
            messages_ip_address = messages_service['Service']['Address']
            messages_port = messages_service['Service']['Port']


            logging_service_response = requests.get(f'http://{logging_ip_address}:{logging_port}/logging_service')
            message_service_response = requests.get(f'http://{messages_ip_address}:{messages_port}/messages_service')

            return jsonify(logging_service_response.json(), message_service_response.json())

    def run(self):
        self.facade_service.run(port=self.facade_port, debug=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address')
    parser.add_argument('facade_port')  
    args = parser.parse_args()
    app = FacadeController(args.ip_address, args.facade_port)
    app.run()

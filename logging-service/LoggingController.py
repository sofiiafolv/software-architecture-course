from flask import jsonify, request, Flask, make_response
import argparse
import hazelcast
import consul

class LoggingController:
    def __init__(self, ip_address, logging_port):
        self.logging_service = Flask(__name__)
        # self.messages_map = self.client.get_map("logging_service_messages").blocking()
        self.ip_address = ip_address
        self.logging_port = logging_port
        self.consul_service = consul.Consul()
        self.consul_service.agent.service.register('logging-service', service_id='logging-service-' + logging_port, port=int(logging_port), address=ip_address)

        self.client_name = self.consul_service.kv.get('cluster-name')[1]['Value'].decode()
        self.client = hazelcast.HazelcastClient(cluster_name=self.client_name)

        self.messages_map_name = self.consul_service.kv.get('map-name')[1]['Value'].decode()
        self.messages_map = self.client.get_map(self.messages_map_name).blocking()

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

    def run(self):
        try:
            self.logging_service.run(port=self.logging_port, debug=True)
        finally:
            self.client.shutdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address')
    parser.add_argument('logging_port')  
    args = parser.parse_args()
    app = LoggingController(args.ip_address, args.logging_port)
    app.run()


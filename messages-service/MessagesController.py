from flask import jsonify, Flask
import argparse
import hazelcast
import threading
import consul

class MessagesController:
    def __init__(self, ip_address, messaging_port):
        self.messages_service = Flask(__name__)
        # self.client = hazelcast.HazelcastClient()
        # self.message_queue = self.client.get_queue("messaging_queue").blocking()

        self.messages = []
        self.messages_lock = threading.Lock()
        self.ip_address = ip_address
        self.messaging_port = messaging_port
        self.consul_service = consul.Consul()
        self.consul_service.agent.service.register('messages-service', service_id='messages-service-' + messaging_port, port=int(messaging_port), address=ip_address)

        self.client_name = self.consul_service.kv.get('cluster-name')[1]['Value'].decode()
        self.client = hazelcast.HazelcastClient(cluster_name=self.client_name)

        self.messaging_queue_name = self.consul_service.kv.get('queue-name')[1]['Value'].decode()
        self.messaging_queue = self.client.get_queue(self.messaging_queue_name).blocking()

        @self.messages_service.route('/messages_service', methods=['GET'])
        def get_message():
            with self.messages_lock:
                return jsonify(self.messages)
        
    def queue_listener(self):
        while True:
            message = self.messaging_queue.take()
            with self.messages_lock:
                self.messages.append(message)
            print(f"Received message: {message}")

    def run(self):
        self.queue_listener_thread = threading.Thread(target=self.queue_listener)
        self.queue_listener_thread.start()
        try:
            self.messages_service.run(port=self.messaging_port, debug=False)
            self.queue_listener_thread.join()
        finally:
            self.stop()

    def stop(self):
        print("Shutting down Hazelcast client")
        self.client.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address')
    parser.add_argument('messages_port')  
    args = parser.parse_args()
    app = MessagesController(args.ip_address, args.messages_port)
    app.run()

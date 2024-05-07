from flask import jsonify, Flask
import argparse
import hazelcast
import threading

class MessagesController:
    def __init__(self):
        self.messages_service = Flask(__name__)
        self.client = hazelcast.HazelcastClient()
        self.message_queue = self.client.get_queue("messaging_queue").blocking()

        self.messages = []
        self.messages_lock = threading.Lock()

        # print(self.message_queue.size().result())
        @self.messages_service.route('/messages_service', methods=['GET'])
        def get_message():
            with self.messages_lock:
                return jsonify(self.messages)
        
    def queue_listener(self):
        while True:
            message = self.message_queue.take()
            with self.messages_lock:
                self.messages.append(message)
            print(f"Received message: {message}")

    def run(self, messaging_port):
        self.queue_listener_thread = threading.Thread(target=self.queue_listener)
        self.queue_listener_thread.start()

        self.messages_service.run(port=messaging_port, debug=False)

        self.queue_listener_thread.join()

    def stop(self):
        self.message_queue.remove_listener(self.message_listener_id)
        print("Shutting down Hazelcast client")
        self.client.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('messaging_port')  
    args = parser.parse_args()

    messages_controller = MessagesController()
    try:
        messages_controller.run(args.messaging_port)
    finally:
        messages_controller.stop()

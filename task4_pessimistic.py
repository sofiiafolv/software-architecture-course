import threading
import hazelcast

def increment():
    client = hazelcast.HazelcastClient()
    my_map = client.get_map("distributed-map-task4-pessimistic").blocking()
    my_map.put_if_absent("key", 0)
    for i in range(10000):
        my_map.lock("key")
        try:
            value = my_map.get("key")
            value += 1
            my_map.put("key", value)
        finally:
            my_map.unlock("key")
    print("Finished! Result:", my_map.get("key"))

    client.shutdown()

threads = []

for i in range(3):
    t = threading.Thread(target=increment)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
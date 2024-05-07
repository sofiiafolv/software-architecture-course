import threading
import hazelcast
import time

def increment():
    client = hazelcast.HazelcastClient()
    my_map = client.get_map("distributed-map-task4-optmistic").blocking()
    my_map.put_if_absent("key", 0)
    for i in range(10000):
        while True:
            old_value = my_map.get("key")
            time.sleep(0.01)
            new_value = old_value + 1
            if my_map.replace_if_same("key", old_value, new_value):
                break
    client.shutdown()

threads = []

for i in range(3):
    t = threading.Thread(target=increment)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
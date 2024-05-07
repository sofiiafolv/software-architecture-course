import hazelcast
import threading

def produce():
    client = hazelcast.HazelcastClient()
    my_queue = client.get_queue("myqueue")
    print('Producer started')
    for i in range(100):
        my_queue.offer("value-" + str(i))
        print("Producer produced", "value-" + str(i))
    my_queue.put(-1).result()
    client.shutdown()

def consume(thread_name):
    client = hazelcast.HazelcastClient()
    my_queue = client.get_queue("myqueue")
    print('Consumer', thread_name, 'started')
    consumed_count = 0
    while consumed_count < 100:
        head = my_queue.take().result()
        if head == -1:
            my_queue.put(-1).result()   
            break
        print("Consumer", thread_name, "consumed", head)
        consumed_count += 1
    client.shutdown()

threads = []
t1 = threading.Thread(target=produce)
threads.append(t1)

t2 = threading.Thread(target=consume, args=("1",))
t3 = threading.Thread(target=consume, args=("2",))
threads.append(t2)
threads.append(t3)



for t in threads:
    t.start()

for t in threads:
    t.join()

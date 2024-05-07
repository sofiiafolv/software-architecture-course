import hazelcast

client = hazelcast.HazelcastClient()

my_map = client.get_map("distributed-map").blocking()

for i in range(1000):
    my_map.put(i, str(i))

client.shutdown()


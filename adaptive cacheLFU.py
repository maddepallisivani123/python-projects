from collections import OrderedDict

class AdaptiveLFUCache:
    def __init__(self, capacity, aging_factor=0.9, burst_threshold=5):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.frequency = {}
        self.aging_factor = aging_factor
        self.burst_threshold = burst_threshold

    def get(self, key):
        if key in self.cache:
            # Increment frequency and adjust for bursts
            self.frequency[key] += 1
            if self.frequency[key] > self.burst_threshold:
                self.frequency[key] -= 1  # Prevent aging too quickly for burst items
            return self.cache[key]
        return -1

    def put(self, key, value):
        if key in self.cache:
            # Update value and increment frequency
            self.cache[key] = value
            self.frequency[key] += 1
        else:
            # Check and remove the least frequently used item if at capacity
            if len(self.cache) >= self.capacity:
                min_key = min(self.frequency, key=lambda k: (self.frequency[k], k))
                del self.cache[min_key]
                del self.frequency[min_key]
            # Add new item
            self.cache[key] = value
            self.frequency[key] = 1

        # Adjust frequencies based on aging factor
        for k in self.frequency:
            self.frequency[k] *= self.aging_factor

def simulate_adaptive_lfu_from_file(file_path, cache_capacity):
    with open(file_path, "r") as file:
        cpu_operations = [tuple(line.strip().split()) for line in file]

    cache = AdaptiveLFUCache(cache_capacity)

    for i, operation in enumerate(cpu_operations):
        op_type, *op_args = operation

        if op_type == 'get':
            key = int(op_args[0])
            result = cache.get(key)
            print(f"Operation {i + 1}: Get {key}, Result: {result}")
        elif op_type == 'put':
            key, value = map(int, op_args)
            cache.put(key, value)
            print(f"Operation {i + 1}: Put {key}, Cache Updated: {cache.cache}")
        else:
            print(f"Operation {i + 1}: Unknown Operation")

def main():
    # Specify the path to the CPU operations file
    cpu_operations_file_path = "cpu_operations.txt"

    # Get cache capacity from the user
    cache_capacity = int(input("Enter cache size: "))

    # Simulate adaptive LFU cache from the file
    simulate_adaptive_lfu_from_file(cpu_operations_file_path, cache_capacity)

if __name__ == "__main__":
    main()



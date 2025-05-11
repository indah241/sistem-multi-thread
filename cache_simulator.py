
import threading
import time
import random
from collections import defaultdict

class CacheSimulator:
    def __init__(self, protocol='MESI'):
        self.protocol = protocol
        self.caches = {}
        self.shared_memory = {}
        self.lock = threading.Lock()
        self.metrics = {
            'cache_misses': 0,
            'coherence_messages': 0,
            'memory_accesses': 0
        }
        self.coherence_states = {}
        
    def init_thread_cache(self, thread_id):
        self.caches[thread_id] = {}
        if self.protocol == 'MESI':
            self.coherence_states[thread_id] = defaultdict(lambda: 'I')
    
    def access_memory(self, thread_id, address, access_type):
        with self.lock:
            self.metrics['memory_accesses'] += 1
            if self.protocol == 'none':
                return self.access_without_coherence(thread_id, address, access_type)
            else:
                return self.access_with_mesi(thread_id, address, access_type)
    
    def access_without_coherence(self, thread_id, address, access_type):
        cache = self.caches[thread_id]
        if address not in cache:
            self.metrics['cache_misses'] += 1
            if address not in self.shared_memory:
                self.shared_memory[address] = 0
            cache[address] = self.shared_memory[address]
        if access_type == 'read':
            return cache[address]
        else:
            value = random.randint(1, 100)
            cache[address] = value
            self.shared_memory[address] = value
            return value
    
    def access_with_mesi(self, thread_id, address, access_type):
        cache = self.caches[thread_id]
        state = self.coherence_states[thread_id][address]
        if address not in cache or state == 'I':
            self.metrics['cache_misses'] += 1
            other_has_copy = any(address in c for tid, c in self.caches.items() if tid != thread_id)
            if address not in self.shared_memory:
                self.shared_memory[address] = 0
            if access_type == 'read':
                if other_has_copy:
                    for tid in self.caches:
                        if address in self.coherence_states[tid]:
                            self.coherence_states[tid][address] = 'S'
                    self.metrics['coherence_messages'] += 2
                    self.coherence_states[thread_id][address] = 'S'
                else:
                    self.coherence_states[thread_id][address] = 'E'
                    self.metrics['coherence_messages'] += 1
            else:
                for tid in self.caches:
                    if tid != thread_id and address in self.coherence_states[tid]:
                        self.coherence_states[tid][address] = 'I'
                self.coherence_states[thread_id][address] = 'M'
                self.metrics['coherence_messages'] += 2
            cache[address] = self.shared_memory[address]
        if access_type == 'read':
            return cache[address]
        else:
            if state == 'S':
                self.coherence_states[thread_id][address] = 'M'
                for tid in self.caches:
                    if tid != thread_id and address in self.coherence_states[tid]:
                        self.coherence_states[tid][address] = 'I'
                self.metrics['coherence_messages'] += 1
            value = random.randint(1, 100)
            cache[address] = value
            self.shared_memory[address] = value
            return value

def worker(thread_id, cache_sim, num_operations):
    cache_sim.init_thread_cache(thread_id)
    for _ in range(num_operations):
        address = random.choice(['A', 'B', 'C', 'D'])
        access_type = random.choice(['read', 'write'])
        cache_sim.access_memory(thread_id, address, access_type)
        time.sleep(0.001)

def run_simulation(num_threads=4, num_operations=100, protocol='MESI'):
    print(f"\nMenjalankan simulasi dengan {num_threads} thread, {num_operations} operasi/thread, protokol {protocol}")
    cache_sim = CacheSimulator(protocol=protocol)
    threads = []
    start_time = time.time()
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i, cache_sim, num_operations))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Waktu eksekusi: {execution_time:.4f} detik")
    print(f"Total akses memori: {cache_sim.metrics['memory_accesses']}")
    print(f"Cache misses: {cache_sim.metrics['cache_misses']}")
    print(f"Pesan koherensi: {cache_sim.metrics['coherence_messages']}")
    return execution_time, cache_sim.metrics

def compare_protocols():
    print("=== Perbandingan Protokol Koherensi Cache ===")
    time_no_proto, metrics_no_proto = run_simulation(protocol='none')
    time_mesi, metrics_mesi = run_simulation(protocol='MESI')
    time_diff = time_no_proto - time_mesi
    miss_diff = metrics_no_proto['cache_misses'] - metrics_mesi['cache_misses']
    print("\n=== Hasil Perbandingan ===")
    print(f"Perbedaan waktu eksekusi: {time_diff:.4f} detik ({'MESI lebih cepat' if time_diff > 0 else 'Tanpa protokol lebih cepat'})")
    print(f"Perbedaan cache misses: {miss_diff} ({'Lebih banyak miss tanpa protokol' if miss_diff > 0 else 'Lebih banyak miss dengan MESI'})")
    print(f"Pesan koherensi dengan MESI: {metrics_mesi['coherence_messages']}")
    print(f"Pesan koherensi tanpa protokol: {metrics_no_proto['coherence_messages']}")

if __name__ == "__main__":
    compare_protocols()

import threading
import time
import random
import numpy as np

class GlobalRecommendationModelServer:
    def __init__(self, initial_embeddings, embedding_dim):
        self.item_embeddings = {item_id: np.random.rand(embedding_dim) for item_id in initial_embeddings['items']}
        self.user_embeddings = {user_id: np.random.rand(embedding_dim) for user_id in initial_embeddings['users']}
        self.lock = threading.Lock()
        print(f"Server initialized with {len(self.item_embeddings)} item and {len(self.user_embeddings)} user embeddings.")

    def pull_embedding(self, entity_type, entity_id):
        with self.lock:
            if entity_type == 'item':
                return self.item_embeddings.get(entity_id, np.zeros_like(next(iter(self.item_embeddings.values())))).copy()
            elif entity_type == 'user':
                return self.user_embeddings.get(entity_id, np.zeros_like(next(iter(self.user_embeddings.values())))).copy()
            else:
                raise ValueError("Invalid entity type")

    def push_updates(self, updates):
        with self.lock:
            learning_rate = 0.05
            for entity_type, entity_updates in updates.items():
                target_embeddings = self.item_embeddings if entity_type == 'item' else self.user_embeddings
                for entity_id, delta in entity_updates.items():
                    if entity_id in target_embeddings:
                        target_embeddings[entity_id] += learning_rate * delta
                    else:
                        pass
            print(f"Server applied updates from a worker.")

class RegionalDataCenterWorker(threading.Thread):
    def __init__(self, worker_id, parameter_server, local_interactions, embedding_dim):
        super().__init__()
        self.worker_id = worker_id
        self.parameter_server = parameter_server
        self.local_interactions = local_interactions
        self.embedding_dim = embedding_dim
        print(f"Worker {self.worker_id} initialized with {len(self.local_interactions)} local interactions.")

    def run(self):
        print(f"Worker {self.worker_id} starting processing interactions...")
        for epoch in range(2):
            local_updates = {'user': {}, 'item': {}}
            for user_id, item_id, rating in self.local_interactions:
                user_embedding = self.parameter_server.pull_embedding('user', user_id)
                item_embedding = self.parameter_server.pull_embedding('item', item_id)

                user_delta = np.random.rand(self.embedding_dim) - 0.5
                item_delta = np.random.rand(self.embedding_dim) - 0.5

                local_updates['user'][user_id] = local_updates['user'].get(user_id, np.zeros(self.embedding_dim)) + user_delta
                local_updates['item'][item_id] = local_updates['item'].get(item_id, np.zeros(self.embedding_dim)) + item_delta
                
                time.sleep(random.uniform(0.01, 0.05))

            print(f"Worker {self.worker_id} (Epoch {epoch+1}) computed {len(local_updates['user'])} user and {len(local_updates['item'])} item updates.")
            self.parameter_server.push_updates(local_updates)
        print(f"Worker {self.worker_id} finished processing.")

if __name__ == "__main__":
    EMBEDDING_DIM = 8
    NUM_WORKERS = 2
    NUM_USERS = 10
    NUM_ITEMS = 20
    INTERACTIONS_PER_WORKER = 50

    # Real-world usage: E-commerce recommendation system training.
    # Regional data centers (workers) process local user interaction data.
    # A central E-commerce platform (parameter server) maintains and updates
    # global user and item embeddings for personalized recommendations.

    # Simulation pattern:
    # Multiple threads (representing regional data centers) send their embedding updates
    # to a shared in-memory object (representing the central recommendation model server).

    all_users = [f"user_{i}" for i in range(NUM_USERS)]
    all_items = [f"item_{i}" for i in range(NUM_ITEMS)]

    initial_embeddings = {'users': all_users, 'items': all_items}
    parameter_server = GlobalRecommendationModelServer(initial_embeddings, EMBEDDING_DIM)

    workers = []
    for i in range(NUM_WORKERS):
        local_interactions = []
        for _ in range(INTERACTIONS_PER_WORKER):
            user = random.choice(all_users)
            item = random.choice(all_items)
            rating = random.uniform(1, 5)
            local_interactions.append((user, item, rating))
        
        worker = RegionalDataCenterWorker(i + 1, parameter_server, local_interactions, EMBEDDING_DIM)
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()

    print("\nAll workers finished.")
    print(f"Final embedding for user_0 (head): {parameter_server.user_embeddings['user_0'][:3]}")
    print(f"Final embedding for item_0 (head): {parameter_server.item_embeddings['item_0'][:3]}")
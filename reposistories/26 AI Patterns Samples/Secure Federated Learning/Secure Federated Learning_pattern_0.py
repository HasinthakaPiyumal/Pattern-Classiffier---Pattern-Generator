import numpy as np

class Client:
    def __init__(self, client_id, data_size, feature_dim):
        self.client_id = client_id
        self.X = np.random.rand(data_size, feature_dim) * 10
        self.y = (self.X @ np.array([0.5]*feature_dim) + np.random.randn(data_size) * 0.5 > 3).astype(int)
        self.local_weights = None
        self.learning_rate = 0.01

    def set_global_weights(self, global_weights):
        self.local_weights = np.copy(global_weights)

    def train_local_model(self, epochs=5):
        if self.local_weights is None:
            self.local_weights = np.zeros(self.X.shape[1])

        for _ in range(epochs):
            logits = self.X @ self.local_weights
            predictions = 1 / (1 + np.exp(-logits))
            error = predictions - self.y
            gradient = self.X.T @ error / len(self.y)
            self.local_weights -= self.learning_rate * gradient

    def get_model_update(self, global_weights):
        update = self.local_weights - global_weights
        return update

class Server:
    def __init__(self, feature_dim, num_clients):
        self.global_weights = np.zeros(feature_dim)
        self.num_clients = num_clients

    def aggregate_updates(self, updates):
        if not updates:
            return np.zeros_like(self.global_weights)
        
        aggregated_update = np.mean(updates, axis=0)
        return aggregated_update

    def update_global_model(self, aggregated_update):
        self.global_weights += aggregated_update

    def get_global_weights(self):
        return self.global_weights

NUM_CLIENTS = 5
DATA_SIZE_PER_CLIENT = 100
FEATURE_DIM = 10
FEDERATED_ROUNDS = 10

server = Server(feature_dim=FEATURE_DIM, num_clients=NUM_CLIENTS)
clients = [Client(i, DATA_SIZE_PER_CLIENT, FEATURE_DIM) for i in range(NUM_CLIENTS)]

print("Starting Federated Learning Simulation for Healthcare (Disease Prediction)...")

for round_num in range(FEDERATED_ROUNDS):
    print(f"\n--- Federated Round {round_num + 1} ---")
    global_weights = server.get_global_weights()
    
    client_updates = []
    for client in clients:
        client.set_global_weights(global_weights)
        client.train_local_model()
        update = client.get_model_update(global_weights)
        client_updates.append(update)
        print(f"  Client {client.client_id} local training complete, update generated.")
    
    aggregated_update = server.aggregate_updates(client_updates)
    print("  Server aggregated updates.")
    
    server.update_global_model(aggregated_update)
    print("  Server updated global model.")

print("\nFederated Learning Simulation Complete.")
print("Final Global Model Weights:", server.get_global_weights())
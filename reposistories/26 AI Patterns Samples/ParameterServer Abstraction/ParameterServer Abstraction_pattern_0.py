import threading
import time
import random
import numpy as np

class CentralModelServer:
    def __init__(self, num_features):
        self.parameters = np.zeros(num_features)
        self.lock = threading.Lock()
        print(f"Server initialized with parameters: {self.parameters}")

    def pull_parameters(self):
        with self.lock:
            return self.parameters.copy()

    def push_gradients(self, gradients):
        with self.lock:
            learning_rate = 0.01
            self.parameters -= learning_rate * gradients
            print(f"Server updated parameters. New head: {self.parameters[:3]}...")

class HospitalWorker(threading.Thread):
    def __init__(self, worker_id, parameter_server, num_features, num_samples):
        super().__init__()
        self.worker_id = worker_id
        self.parameter_server = parameter_server
        self.local_features = np.random.rand(num_samples, num_features)
        self.local_labels = np.random.randint(0, 2, num_samples)
        print(f"Worker {self.worker_id} initialized with {num_samples} local samples.")

    def run(self):
        print(f"Worker {self.worker_id} starting training...")
        for epoch in range(3):
            current_parameters = self.parameter_server.pull_parameters()
            
            time.sleep(random.uniform(0.1, 0.5))
            
            predictions = np.dot(self.local_features, current_parameters)
            errors = predictions - self.local_labels
            gradients = np.dot(self.local_features.T, errors) / len(self.local_labels)
            
            print(f"Worker {self.worker_id} (Epoch {epoch+1}) computed gradients. Head: {gradients[:3]}...")
            self.parameter_server.push_gradients(gradients)
        print(f"Worker {self.worker_id} finished training.")

if __name__ == "__main__":
    NUM_FEATURES = 10
    NUM_WORKERS = 3
    SAMPLES_PER_WORKER = 100

    # Real-world usage: Federated learning for disease prediction in healthcare.
    # Hospitals (workers) train models on their patient data locally.
    # A central research institute (parameter server) aggregates model updates
    # to build a global, robust disease prediction model without sharing raw patient data.

    # Simulation pattern:
    # Multiple threads (representing hospitals) send their local model updates
    # to a shared in-memory object (representing the central server).

    parameter_server = CentralModelServer(NUM_FEATURES)
    workers = []
    for i in range(NUM_WORKERS):
        worker = HospitalWorker(i + 1, parameter_server, NUM_FEATURES, SAMPLES_PER_WORKER)
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()

    print("\nAll workers finished.")
    print(f"Final global parameters: {parameter_server.parameters}")
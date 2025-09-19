import numpy as np
from sklearn.linear_model import SGDClassifier

class BankClient:
    def __init__(self, client_id, data_size, feature_dim):
        self.client_id = client_id
        self.X = np.random.rand(data_size, feature_dim) * 100
        fraud_indicator = np.sum(self.X[:, :3], axis=1) > 150
        self.y = np.where(np.random.rand(data_size) < 0.05, 1, 0)
        self.y = np.where(fraud_indicator, 1, self.y)
        
        self.local_model = SGDClassifier(loss='log_loss', max_iter=1, warm_start=True, random_state=42)
        self.local_model.fit(np.zeros((1, feature_dim)), np.zeros(1)) 

    def set_global_model_params(self, global_coef, global_intercept):
        self.local_model.coef_ = np.copy(global_coef)
        self.local_model.intercept_ = np.copy(global_intercept)

    def train_local_model(self):
        self.local_model.partial_fit(self.X, self.y, classes=np.array([0, 1]))

    def get_model_parameters(self):
        return self.local_model.coef_, self.local_model.intercept_

class FinancialConsortiumServer:
    def __init__(self, feature_dim):
        self.global_coef = np.zeros((1, feature_dim))
        self.global_intercept = np.zeros(1)

    def aggregate_parameters(self, client_params_list):
        if not client_params_list:
            return self.global_coef, self.global_intercept
        
        total_coef = np.zeros_like(self.global_coef)
        total_intercept = np.zeros_like(self.global_intercept)
        
        for coef, intercept in client_params_list:
            total_coef += coef
            total_intercept += intercept
            
        aggregated_coef = total_coef / len(client_params_list)
        aggregated_intercept = total_intercept / len(client_params_list)
        
        return aggregated_coef, aggregated_intercept

    def update_global_model(self, aggregated_coef, aggregated_intercept):
        self.global_coef = aggregated_coef
        self.global_intercept = aggregated_intercept

    def get_global_model_params(self):
        return self.global_coef, self.global_intercept

NUM_BANKS = 4
DATA_SIZE_PER_BANK = 200
FEATURE_DIM_BANK = 8
FEDERATED_ROUNDS_BANK = 8

server_bank = FinancialConsortiumServer(feature_dim=FEATURE_DIM_BANK)
bank_clients = [BankClient(i, DATA_SIZE_PER_BANK, FEATURE_DIM_BANK) for i in range(NUM_BANKS)]

print("Starting Federated Learning Simulation for Banking (Fraud Detection)...")

for round_num in range(FEDERATED_ROUNDS_BANK):
    print(f"\n--- Federated Round {round_num + 1} ---")
    global_coef, global_intercept = server_bank.get_global_model_params()
    
    client_params_updates = []
    for client in bank_clients:
        client.set_global_model_params(global_coef, global_intercept)
        client.train_local_model()
        coef, intercept = client.get_model_parameters()
        client_params_updates.append((coef, intercept))
        print(f"  Bank Client {client.client_id} local training complete, parameters generated.")
    
    aggregated_coef, aggregated_intercept = server_bank.aggregate_parameters(client_params_updates)
    print("  Server aggregated parameters.")
    
    server_bank.update_global_model(aggregated_coef, aggregated_intercept)
    print("  Server updated global model.")

print("\nFederated Learning Simulation Complete for Banking.")
print("Final Global Model Coefficients:", server_bank.get_global_model_params()[0])
print("Final Global Model Intercept:", server_bank.get_global_model_params()[1])
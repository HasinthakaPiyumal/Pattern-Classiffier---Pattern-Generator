import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from abc import ABC, abstractmethod

class AnomalyDetector(ABC):
    @abstractmethod
    def train(self, X_train, y_train=None):
        pass

    @abstractmethod
    def detect(self, X_new):
        pass

class SupervisedFraudDetector(AnomalyDetector):
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train, y_train):
        print("Training Supervised Fraud Detector (RandomForestClassifier)...")
        self.model.fit(X_train, y_train)

    def detect(self, X_new):
        print("Detecting anomalies using Supervised model...")
        predictions = self.model.predict(X_new)
        return predictions

class SemiSupervisedFraudDetector(AnomalyDetector):
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)

    def train(self, X_train, y_train=None):
        print("Training Semi-Supervised Fraud Detector (IsolationForest) on normal data...")
        if y_train is not None:
            normal_data = X_train[y_train == 0]
            self.model.fit(normal_data)
        else:
            self.model.fit(X_train)

    def detect(self, X_new):
        print("Detecting anomalies using Semi-Supervised model...")
        predictions = self.model.predict(X_new)
        return np.where(predictions == -1, 1, 0)

class FraudDetectionStrategySelector:
    def __init__(self, has_labeled_anomalies: bool):
        self.has_labeled_anomalies = has_labeled_anomalies
        self.detector: AnomalyDetector = None

    def select_and_create_detector(self):
        if self.has_labeled_anomalies:
            print("Labeled anomalies available. Selecting Supervised Fraud Detection.")
            self.detector = SupervisedFraudDetector()
        else:
            print("Only normal data labeled. Selecting Semi-Supervised Fraud Detection.")
            self.detector = SemiSupervisedFraudDetector()
        return self.detector

if __name__ == "__main__":
    np.random.seed(42)
    num_samples = 1000
    X = np.random.rand(num_samples, 5) * 100
    y = np.zeros(num_samples, dtype=int)

    num_anomalies = 50
    anomaly_indices = np.random.choice(num_samples, num_anomalies, replace=False)
    y[anomaly_indices] = 1
    X[anomaly_indices, 0] += 50

    print("\n--- Scenario 1: Labeled anomalies ARE available (Supervised) ---")
    selector1 = FraudDetectionStrategySelector(has_labeled_anomalies=True)
    detector1 = selector1.select_and_create_detector()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    detector1.train(X_train, y_train)
    predictions1 = detector1.detect(X_test)
    print("\nSupervised Anomaly Detection Report:")
    print(classification_report(y_test, predictions1, target_names=["Normal", "Fraud"]))

    print("\n--- Scenario 2: Only normal data labeled (Semi-Supervised) ---")
    selector2 = FraudDetectionStrategySelector(has_labeled_anomalies=False)
    detector2 = selector2.select_and_create_detector()

    X_train_normal_only = X_train[y_train == 0]
    detector2.train(X_train_normal_only)

    predictions2 = detector2.detect(X_test)
    print("\nSemi-Supervised Anomaly Detection Report:")
    print(classification_report(y_test, predictions2, target_names=["Normal", "Fraud"]))
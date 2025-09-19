import numpy as np
from sklearn.svm import OneClassSVM
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from abc import ABC, abstractmethod

class PatientAnomalyDetector(ABC):
    @abstractmethod
    def train(self, X_train, y_train=None):
        pass

    @abstractmethod
    def detect(self, X_new):
        pass

class SupervisedVitalSignDetector(PatientAnomalyDetector):
    def __init__(self):
        from sklearn.linear_model import LogisticRegression
        self.model = LogisticRegression(random_state=42, solver='liblinear')

    def train(self, X_train, y_train):
        print("Training Supervised Vital Sign Detector (LogisticRegression)...")
        self.model.fit(X_train, y_train)

    def detect(self, X_new):
        print("Detecting vital sign anomalies using Supervised model...")
        predictions = self.model.predict(X_new)
        return predictions

class SemiSupervisedVitalSignDetector(PatientAnomalyDetector):
    def __init__(self):
        self.model = OneClassSVM(nu=0.05, kernel="rbf", gamma="auto")

    def train(self, X_train, y_train=None):
        print("Training Semi-Supervised Vital Sign Detector (OneClassSVM) on normal data...")
        if y_train is not None:
            normal_data = X_train[y_train == 0]
            self.model.fit(normal_data)
        else:
            self.model.fit(X_train)

    def detect(self, X_new):
        print("Detecting vital sign anomalies using Semi-Supervised model...")
        predictions = self.model.predict(X_new)
        return np.where(predictions == -1, 1, 0)

class VitalSignDetectionStrategySelector:
    def __init__(self, has_labeled_anomalies: bool):
        self.has_labeled_anomalies = has_labeled_anomalies
        self.detector: PatientAnomalyDetector = None

    def select_and_create_detector(self):
        if self.has_labeled_anomalies:
            print("Labeled critical vital sign patterns available. Selecting Supervised Detection.")
            self.detector = SupervisedVitalSignDetector()
        else:
            print("Only normal vital sign patterns labeled. Selecting Semi-Supervised Detection.")
            self.detector = SemiSupervisedVitalSignDetector()
        return self.detector

if __name__ == "__main__":
    np.random.seed(42)
    num_patients = 800
    num_features = 4
    X = np.random.normal(loc=[70, 120, 37, 98], scale=[5, 10, 0.5, 1], size=(num_patients, num_features))
    y = np.zeros(num_patients, dtype=int)

    num_anomalies = 40
    anomaly_indices = np.random.choice(num_patients, num_anomalies, replace=False)
    X[anomaly_indices, 0] = np.random.normal(loc=130, scale=10, size=num_anomalies)
    X[anomaly_indices, 3] = np.random.normal(loc=85, scale=3, size=num_anomalies)
    y[anomaly_indices] = 1

    print("\n--- Scenario 1: Labeled critical patterns available (Supervised) ---")
    selector1 = VitalSignDetectionStrategySelector(has_labeled_anomalies=True)
    detector1 = selector1.select_and_create_detector()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    detector1.train(X_train, y_train)
    predictions1 = detector1.detect(X_test)
    print("\nSupervised Vital Sign Anomaly Detection Report:")
    print(classification_report(y_test, predictions1, target_names=["Normal", "Critical"]))

    print("\n--- Scenario 2: Only normal patterns labeled (Semi-Supervised) ---")
    selector2 = VitalSignDetectionStrategySelector(has_labeled_anomalies=False)
    detector2 = selector2.select_and_create_detector()

    X_train_normal_only = X_train[y_train == 0]
    detector2.train(X_train_normal_only)

    predictions2 = detector2.detect(X_test)
    print("\nSemi-Supervised Vital Sign Anomaly Detection Report:")
    print(classification_report(y_test, predictions2, target_names=["Normal", "Critical"]))
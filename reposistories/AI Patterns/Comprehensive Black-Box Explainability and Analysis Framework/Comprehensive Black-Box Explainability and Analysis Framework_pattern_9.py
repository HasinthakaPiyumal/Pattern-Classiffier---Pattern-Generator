import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import lime
import lime.lime_tabular
import shap

np.random.seed(100)
n_patients = 800
data = {
    'age': np.random.randint(18, 90, n_patients),
    'fever_score': np.random.uniform(0, 1, n_patients),
    'cough_score': np.random.uniform(0, 1, n_patients),
    'fatigue_score': np.random.uniform(0, 1, n_patients),
    'blood_pressure_sys': np.random.randint(90, 180, n_patients),
    'cholesterol_level': np.random.randint(150, 300, n_patients),
}
df = pd.DataFrame(data)

df['diagnosis_X'] = ((df['fever_score'] > 0.6) * 0.2 +
                     (df['cough_score'] > 0.7) * 0.25 +
                     (df['fatigue_score'] > 0.5) * 0.15 +
                     (df['age'] > 60) * 0.15 +
                     (df['cholesterol_level'] > 220) * 0.1 -
                     (df['blood_pressure_sys'] < 120) * 0.05 +
                     np.random.rand(n_patients) * 0.2 > 0.6).astype(int)

X = df[['age', 'fever_score', 'cough_score', 'fatigue_score', 'blood_pressure_sys', 'cholesterol_level']]
y = df['diagnosis_X']
feature_names = X.columns.tolist()
class_names = ['No DiseaseX', 'Has DiseaseX']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

black_box_model_healthcare = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=100)
black_box_model_healthcare.fit(X_train, y_train)

class HealthcareExplainabilityFramework:
    def __init__(self, model, X_train, feature_names, class_names):
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names
        self.class_names = class_names

    def get_global_surrogate(self):
        surrogate_model = LogisticRegression(solver='liblinear', random_state=100)
        surrogate_model.fit(self.X_train, self.model.predict(self.X_train))
        return surrogate_model

    def explain_local_lime(self, instance):
        explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=self.X_train.values,
            feature_names=self.feature_names,
            class_names=self.class_names,
            mode='classification'
        )
        explanation = explainer.explain_instance(
            data_row=instance.values,
            predict_fn=self.model.predict_proba,
            num_features=len(self.feature_names)
        )
        return explanation.as_list()

    def explain_local_shap(self, instance):
        explainer = shap.Explainer(self.model, self.X_train)
        shap_values = explainer(instance)
        predicted_class_idx = np.argmax(self.model.predict_proba(instance.to_frame().T))
        return {
            'base_value': shap_values.base_values[predicted_class_idx],
            'feature_contributions': dict(zip(self.feature_names, shap_values.values[0][predicted_class_idx]))
        }

    def get_local_rules(self, instance, top_features_lime):
        rules = []
        for feature, weight in top_features_lime:
            feat_val = instance[feature]
            if weight > 0 and feat_val > np.mean(self.X_train[feature]):
                rules.append(f"IF {feature} ({feat_val:.2f}) is higher than average (positive influence)")
            elif weight < 0 and feat_val < np.mean(self.X_train[feature]):
                rules.append(f"IF {feature} ({feat_val:.2f}) is lower than average (negative influence)")
            elif weight > 0 and feat_val < np.mean(self.X_train[feature]):
                 rules.append(f"IF {feature} ({feat_val:.2f}) is lower than average (unexpected positive influence)")
            elif weight < 0 and feat_val > np.mean(self.X_train[feature]):
                 rules.append(f"IF {feature} ({feat_val:.2f}) is higher than average (unexpected negative influence)")
            else:
                rules.append(f"IF {feature} ({feat_val:.2f}) has a notable influence ({weight:.2f})")
        return rules

    def get_counterfactual(self, instance, desired_prediction_class_idx=1, max_iter=100, step_size_factor=0.01):
        original_prediction_proba = self.model.predict_proba(instance.to_frame().T)[0]
        original_prediction_class = np.argmax(original_prediction_proba)

        if original_prediction_class == desired_prediction_class_idx:
            return "Instance already has the desired prediction."

        counterfactual_instance = instance.copy()
        feature_ranges = {col: (self.X_train[col].min(), self.X_train[col].max()) for col in self.feature_names}

        for _ in range(max_iter):
            current_prediction_proba = self.model.predict_proba(counterfactual_instance.to_frame().T)[0]
            current_prediction_class = np.argmax(current_prediction_proba)

            if current_prediction_class == desired_prediction_class_idx:
                return counterfactual_instance, original_prediction_class, desired_prediction_class_idx

            explainer = shap.Explainer(self.model, self.X_train)
            shap_values = explainer(counterfactual_instance.to_frame().T)
            
            contributions = shap_values.values[0][desired_prediction_class_idx]
            
            for i, feature in enumerate(self.feature_names):
                change = contributions[i] * step_size_factor
                
                if desired_prediction_class_idx == 1:
                    counterfactual_instance[feature] += change
                else:
                    counterfactual_instance[feature] -= change

                min_val, max_val = feature_ranges[feature]
                counterfactual_instance[feature] = np.clip(counterfactual_instance[feature], min_val, max_val)

        return "Could not find a counterfactual within iterations.", original_prediction_class, desired_prediction_class_idx

    def perform_subgroup_analysis(self, X_data, y_true):
        predictions = self.model.predict(X_data)
        overall_accuracy = np.mean(predictions == y_true)

        subgroup_reports = []

        elderly_mask = X_data['age'] > 70
        if elderly_mask.any():
            elderly_subgroup_X = X_data[elderly_mask]
            elderly_subgroup_y_true = y_true[elderly_mask]
            elderly_subgroup_preds = predictions[elderly_mask]
            elderly_accuracy = np.mean(elderly_subgroup_preds == elderly_subgroup_y_true)
            subgroup_reports.append({
                "name": "Elderly Patients (>70 years)",
                "size": len(elderly_subgroup_X),
                "overall_accuracy": f"{overall_accuracy:.2f}",
                "subgroup_accuracy": f"{elderly_accuracy:.2f}",
                "divergence": f"{elderly_accuracy - overall_accuracy:.2f}"
            })

        high_cholesterol_mask = X_data['cholesterol_level'] > 250
        if high_cholesterol_mask.any():
            high_chol_subgroup_X = X_data[high_cholesterol_mask]
            high_chol_subgroup_y_true = y_true[high_cholesterol_mask]
            high_chol_subgroup_preds = predictions[high_cholesterol_mask]
            high_chol_accuracy = np.mean(high_chol_subgroup_preds == high_chol_subgroup_y_true)
            subgroup_reports.append({
                "name": "High Cholesterol Patients (>250)",
                "size": len(high_chol_subgroup_X),
                "overall_accuracy": f"{overall_accuracy:.2f}",
                "subgroup_accuracy": f"{high_chol_accuracy:.2f}",
                "divergence": f"{high_chol_accuracy - overall_accuracy:.2f}"
            })

        return subgroup_reports

    def interactive_explore(self, instance_to_explain):
        print(f"\n--- Explaining Patient Instance (Diagnosis): ---")
        print(instance_to_explain)
        original_prediction = self.model.predict(instance_to_explain.to_frame().T)[0]
        print(f"Black-box Model Prediction: {self.class_names[original_prediction]}")

        print("\n--- Local Explanation (LIME) ---")
        lime_exp = self.explain_local_lime(instance_to_explain)
        for feature, weight in lime_exp:
            print(f"  {feature}: {weight:.4f}")

        print("\n--- Local Explanation (SHAP) ---")
        shap_exp = self.explain_local_shap(instance_to_explain)
        print(f"  Base Value: {shap_exp['base_value']:.4f}")
        for feature, contribution in shap_exp['feature_contributions'].items():
            print(f"  {feature}: {contribution:.4f}")

        print("\n--- Local Rule-Based Explanation ---")
        local_rules = self.get_local_rules(instance_to_explain, lime_exp)
        for rule in local_rules:
            print(f"  - {rule}")

        print("\n--- Counterfactual Explanation (What if we wanted No DiseaseX?) ---")
        cf_result = self.get_counterfactual(instance_to_explain, desired_prediction_class_idx=0)
        if isinstance(cf_result, tuple):
            counterfactual_instance, original_pred, desired_pred = cf_result
            print(f"Original Prediction: {self.class_names[original_pred]}")
            print(f"Desired Prediction: {self.class_names[desired_pred]}")
            print("Minimal changes to achieve desired outcome (No DiseaseX):")
            changes = counterfactual_instance - instance_to_explain
            for feature, change in changes.items():
                if abs(change) > 0.01:
                    print(f"  {feature}: Change by {change:.2f} (from {instance_to_explain[feature]:.2f} to {counterfactual_instance[feature]:.2f})")
            print(f"New instance for desired outcome:\n{counterfactual_instance}")
        else:
            print(cf_result)

framework_healthcare = HealthcareExplainabilityFramework(black_box_model_healthcare, X_train, feature_names, class_names)

print("--- Global Understanding: Surrogate Model ---")
global_surrogate_healthcare = framework_healthcare.get_global_surrogate()
print(f"Global Surrogate Model (Logistic Regression) trained. Coefficients: {global_surrogate_healthcare.coef_}")

print("\n--- Subgroup Divergence Analysis ---")
subgroup_reports_healthcare = framework_healthcare.perform_subgroup_analysis(X_test, y_test)
for report in subgroup_reports_healthcare:
    print(f"Subgroup: {report['name']} (Size: {report['size']})")
    print(f"  Overall Model Accuracy: {report['overall_accuracy']}")
    print(f"  Subgroup Accuracy: {report['subgroup_accuracy']}")
    print(f"  Divergence (Subgroup - Overall): {report['divergence']}")
    if float(report['divergence']) < -0.1 or float(report['divergence']) > 0.1:
        print("  -> Significant divergence detected, investigate potential disparities or model strengths/weaknesses in this group.")
    print("-" * 30)

instance_to_explain_idx_hc = 10
instance_to_explain_hc = X_test.iloc[instance_to_explain_idx_hc]
framework_healthcare.interactive_explore(instance_to_explain_hc)

diagnosed_idx = y_test[black_box_model_healthcare.predict(X_test) == 1].index
if not diagnosed_idx.empty:
    instance_to_explain_diagnosed = X_test.loc[diagnosed_idx[0]]
    framework_healthcare.interactive_explore(instance_to_explain_diagnosed)

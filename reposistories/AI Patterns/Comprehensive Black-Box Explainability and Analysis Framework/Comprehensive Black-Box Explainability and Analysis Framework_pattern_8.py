import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import lime
import lime.lime_tabular
import shap

np.random.seed(42)
n_samples = 1000
data = {
    'age': np.random.randint(20, 70, n_samples),
    'income': np.random.randint(30000, 150000, n_samples),
    'credit_score': np.random.randint(300, 850, n_samples),
    'loan_amount': np.random.randint(5000, 100000, n_samples),
    'employment_duration': np.random.randint(0, 20, n_samples),
}
df = pd.DataFrame(data)

df['approved'] = ((df['income'] > 60000) * 0.4 +
                  (df['credit_score'] > 650) * 0.3 +
                  (df['employment_duration'] > 3) * 0.2 -
                  (df['loan_amount'] > 50000) * 0.1 +
                  np.random.rand(n_samples) * 0.2 > 0.5).astype(int)

X = df[['age', 'income', 'credit_score', 'loan_amount', 'employment_duration']]
y = df['approved']
feature_names = X.columns.tolist()
class_names = ['Rejected', 'Approved']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

black_box_model = RandomForestClassifier(n_estimators=100, random_state=42)
black_box_model.fit(X_train, y_train)

class BlackBoxExplainabilityFramework:
    def __init__(self, model, X_train, feature_names, class_names):
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names
        self.class_names = class_names

    def get_global_surrogate(self):
        surrogate_model = DecisionTreeClassifier(max_depth=5, random_state=42)
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
            if weight > 0:
                rules.append(f"IF {feature} is approximately {feat_val:.0f} (positive influence)")
            else:
                rules.append(f"IF {feature} is approximately {feat_val:.0f} (negative influence)")
        return rules

    def get_counterfactual(self, instance, desired_prediction_class_idx=1, max_iter=100, step_size=0.05):
        original_prediction_proba = self.model.predict_proba(instance.to_frame().T)[0]
        original_prediction_class = np.argmax(original_prediction_proba)

        if original_prediction_class == desired_prediction_class_idx:
            return "Instance already has the desired prediction."

        counterfactual_instance = instance.copy()
        for _ in range(max_iter):
            current_prediction_proba = self.model.predict_proba(counterfactual_instance.to_frame().T)[0]
            current_prediction_class = np.argmax(current_prediction_proba)

            if current_prediction_class == desired_prediction_class_idx:
                return counterfactual_instance, original_prediction_class, desired_prediction_class_idx

            lime_explanation = self.explain_local_lime(counterfactual_instance)
            for feature, weight in lime_explanation:
                if (desired_prediction_class_idx == 1 and weight > 0) or \
                   (desired_prediction_class_idx == 0 and weight < 0):
                    counterfactual_instance[feature] += step_size * np.abs(weight) * (1 if weight > 0 else -1)
                elif (desired_prediction_class_idx == 1 and weight < 0) or \
                     (desired_prediction_class_idx == 0 and weight > 0):
                    counterfactual_instance[feature] -= step_size * np.abs(weight) * (1 if weight > 0 else -1)

            counterfactual_instance['age'] = np.clip(counterfactual_instance['age'], 20, 70)
            counterfactual_instance['income'] = np.clip(counterfactual_instance['income'], 30000, 150000)
            counterfactual_instance['credit_score'] = np.clip(counterfactual_instance['credit_score'], 300, 850)
            counterfactual_instance['loan_amount'] = np.clip(counterfactual_instance['loan_amount'], 5000, 100000)
            counterfactual_instance['employment_duration'] = np.clip(counterfactual_instance['employment_duration'], 0, 20)

        return "Could not find a counterfactual within iterations.", original_prediction_class, desired_prediction_class_idx

    def perform_subgroup_analysis(self, X_data, y_true):
        predictions = self.model.predict(X_data)
        overall_accuracy = np.mean(predictions == y_true)

        subgroup_reports = []

        low_credit_mask = X_data['credit_score'] < 600
        if low_credit_mask.any():
            low_credit_subgroup_X = X_data[low_credit_mask]
            low_credit_subgroup_y_true = y_true[low_credit_mask]
            low_credit_subgroup_preds = predictions[low_credit_mask]
            low_credit_accuracy = np.mean(low_credit_subgroup_preds == low_credit_subgroup_y_true)
            subgroup_reports.append({
                "name": "Low Credit Score (<600)",
                "size": len(low_credit_subgroup_X),
                "overall_accuracy": f"{overall_accuracy:.2f}",
                "subgroup_accuracy": f"{low_credit_accuracy:.2f}",
                "divergence": f"{low_credit_accuracy - overall_accuracy:.2f}"
            })

        high_loan_mask = X_data['loan_amount'] > 75000
        if high_loan_mask.any():
            high_loan_subgroup_X = X_data[high_loan_mask]
            high_loan_subgroup_y_true = y_true[high_loan_mask]
            high_loan_subgroup_preds = predictions[high_loan_mask]
            high_loan_accuracy = np.mean(high_loan_subgroup_preds == high_loan_subgroup_y_true)
            subgroup_reports.append({
                "name": "High Loan Amount (>75000)",
                "size": len(high_loan_subgroup_X),
                "overall_accuracy": f"{overall_accuracy:.2f}",
                "subgroup_accuracy": f"{high_loan_accuracy:.2f}",
                "divergence": f"{high_loan_accuracy - overall_accuracy:.2f}"
            })

        return subgroup_reports

    def interactive_explore(self, instance_to_explain):
        print(f"\n--- Explaining Instance (Loan Application): ---")
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

        print("\n--- Counterfactual Explanation (What if we wanted approval?) ---")
        cf_result = self.get_counterfactual(instance_to_explain, desired_prediction_class_idx=1)
        if isinstance(cf_result, tuple):
            counterfactual_instance, original_pred, desired_pred = cf_result
            print(f"Original Prediction: {self.class_names[original_pred]}")
            print(f"Desired Prediction: {self.class_names[desired_pred]}")
            print("Minimal changes to achieve desired outcome:")
            changes = counterfactual_instance - instance_to_explain
            for feature, change in changes.items():
                if abs(change) > 0.1:
                    print(f"  {feature}: Change by {change:.2f} (from {instance_to_explain[feature]:.0f} to {counterfactual_instance[feature]:.0f})")
            print(f"New instance for desired outcome:\n{counterfactual_instance}")
        else:
            print(cf_result)

framework = BlackBoxExplainabilityFramework(black_box_model, X_train, feature_names, class_names)

print("--- Global Understanding: Surrogate Model ---")
global_surrogate = framework.get_global_surrogate()
print(f"Global Surrogate Model (Decision Tree) trained. Depth: {global_surrogate.get_depth()}")

print("\n--- Subgroup Divergence Analysis ---")
subgroup_reports = framework.perform_subgroup_analysis(X_test, y_test)
for report in subgroup_reports:
    print(f"Subgroup: {report['name']} (Size: {report['size']})")
    print(f"  Overall Model Accuracy: {report['overall_accuracy']}")
    print(f"  Subgroup Accuracy: {report['subgroup_accuracy']}")
    print(f"  Divergence (Subgroup - Overall): {report['divergence']}")
    if float(report['divergence']) < -0.1:
        print("  -> Significant negative divergence detected, investigate potential bias or model weakness here.")
    print("-" * 30)

instance_to_explain_idx = 5
instance_to_explain = X_test.iloc[instance_to_explain_idx]
framework.interactive_explore(instance_to_explain)

rejected_idx = y_test[black_box_model.predict(X_test) == 0].index
if not rejected_idx.empty:
    instance_to_explain_rejected = X_test.loc[rejected_idx[0]]
    framework.interactive_explore(instance_to_explain_rejected)

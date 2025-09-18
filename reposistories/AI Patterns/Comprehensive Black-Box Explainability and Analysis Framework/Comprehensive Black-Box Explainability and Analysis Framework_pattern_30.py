import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import lime
import lime.lime_tabular
import shap
import random
import warnings
warnings.filterwarnings("ignore")

def _get_local_rules_healthcare(explainer_lime, instance, feature_names, top_features_count=3):
    explanation = explainer_lime.explain_instance(
        instance,
        explainer_lime.predict_fn,
        num_features=len(feature_names),
        num_samples=1000
    )
    rules = []
    sorted_features = sorted(explanation.as_list(), key=lambda x: abs(x[1]), reverse=True)
    for feature_info in sorted_features[:top_features_count]:
        feature_desc = feature_info[0]
        rules.append(f"IF {feature_desc}")
    prediction = explainer_lime.predict_fn(instance.reshape(1, -1))[0]
    rules.append(f"THEN Diagnosis is {'Disease Present' if prediction == 1 else 'No Disease'}")
    return "\n".join(rules)

def _find_counterfactual_healthcare(model, original_instance, feature_names, desired_output_class, max_tries=100, step_factor=0.05):
    original_prediction = model.predict(original_instance.reshape(1, -1))[0]
    if original_prediction == desired_output_class:
        return f"Already predicts {'Disease Present' if desired_output_class == 1 else 'No Disease'}. No counterfactual needed."
    best_counterfactual_changes = None
    min_features_changed = float('inf')
    for _ in range(max_tries):
        temp_instance = np.copy(original_instance)
        num_features_changed = 0
        current_changes = {}
        num_features_to_change = random.randint(1, min(len(feature_names), 3))
        features_indices_to_change = random.sample(range(len(feature_names)), num_features_to_change)
        for idx in features_indices_to_change:
            feature_name = feature_names[idx]
            original_value = original_instance[idx]
            if feature_name in ['age', 'blood_pressure', 'cholesterol', 'glucose', 'bmi']:
                change_direction = random.choice([-1, 1])
                perturbation_amount = (original_value * step_factor) * change_direction
                temp_instance[idx] = max(0, original_value + perturbation_amount)
                current_changes[feature_name] = f"from {original_value:.2f} to {temp_instance[idx]:.2f}"
                num_features_changed += 1
            elif feature_name == 'family_history':
                temp_instance[idx] = 1 - original_value
                current_changes[feature_name] = f"from {int(original_value)} to {int(temp_instance[idx])}"
                num_features_changed += 1
        new_prediction = model.predict(temp_instance.reshape(1, -1))[0]
        if new_prediction == desired_output_class:
            if num_features_changed < min_features_changed:
                min_features_changed = num_features_changed
                best_counterfactual_changes = current_changes
            elif num_features_changed == min_features_changed:
                if best_counterfactual_changes is None or sum(abs(v[1]-v[0]) for k,v in current_changes.items() if isinstance(v, tuple)) < sum(abs(v[1]-v[0]) for k,v in best_counterfactual_changes.items() if isinstance(v, tuple)):
                    best_counterfactual_changes = current_changes
    if best_counterfactual_changes:
        return f"To change prediction from {'Disease Present' if original_prediction == 1 else 'No Disease'} to {'Disease Present' if desired_output_class == 1 else 'No Disease'}, minimally change: {best_counterfactual_changes}"
    else:
        return f"Could not find a simple counterfactual to achieve {'Disease Present' if desired_output_class == 1 else 'No Disease'} within {max_tries} tries."

np.random.seed(42)
n_samples = 1000
data = {
    'age': np.random.randint(20, 80, n_samples),
    'blood_pressure': np.random.randint(90, 180, n_samples),
    'cholesterol': np.random.randint(120, 300, n_samples),
    'glucose': np.random.randint(70, 200, n_samples),
    'family_history': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
    'bmi': np.random.uniform(18.0, 40.0, n_samples)
}
df = pd.DataFrame(data)
df['disease_present'] = ((df['age'] >= 60) | (df['blood_pressure'] >= 140) | (df['cholesterol'] >= 240) | (df['glucose'] >= 126) | (df['family_history'] == 1)).astype(int)
df.loc[(df['age'] < 30) & (df['blood_pressure'] < 120) & (df['cholesterol'] < 200), 'disease_present'] = 0
df.loc[(df['glucose'] >= 180) | (df['bmi'] >= 35), 'disease_present'] = 1
X = df.drop('disease_present', axis=1)
y = df['disease_present']
feature_names = X.columns.tolist()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
black_box_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
black_box_model.fit(X_train, y_train)
print("--- Healthcare Disease Diagnosis Prediction ---")
print(f"Black-box model accuracy: {accuracy_score(y_test, black_box_model.predict(X_test)):.4f}\n")
surrogate_model = LogisticRegression(solver='liblinear', random_state=42)
surrogate_model.fit(X_train, black_box_model.predict(X_train))
print("1. Global Understanding: Logistic Regression Surrogate Model (Approximating Black-Box Logic)")
print("  Feature Coefficients (Magnitude indicates importance, sign indicates direction):")
for i, feature in enumerate(feature_names):
    print(f"  {feature}: {surrogate_model.coef_[0][i]:.4f}")
print(f"Surrogate model accuracy (on black-box predictions): {accuracy_score(black_box_model.predict(X_test), surrogate_model.predict(X_test)):.4f}\n")
instance_idx = 0
instance_to_explain = X_test.iloc[instance_idx].values
original_prediction = black_box_model.predict(instance_to_explain.reshape(1, -1))[0]
print(f"Analyzing patient instance {instance_idx}: {X_test.iloc[instance_idx].to_dict()}")
print(f"Black-box model predicted: {'Disease Present' if original_prediction == 1 else 'No Disease'}\n")
lime_explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=feature_names,
    class_names=['No Disease', 'Disease Present'],
    mode='classification'
)
lime_explanation = lime_explainer.explain_instance(
    instance_to_explain,
    black_box_model.predict_proba,
    num_features=len(feature_names)
)
print("2a. Local Prediction Explanation (LIME-like Feature Importance):")
for feature, weight in lime_explanation.as_list():
    print(f"  {feature}: {weight:.4f}")
print("\n")
shap_explainer = shap.KernelExplainer(black_box_model.predict, X_train.sample(100, random_state=42))
shap_values = shap_explainer.shap_values(instance_to_explain)
print("2b. Local Prediction Explanation (SHAP-like Game-Teoretic Attribution):")
shap_values_for_prediction = shap_values[1] if isinstance(shap_values, list) else shap_values
shap_df = pd.DataFrame({'feature': feature_names, 'shap_value': shap_values_for_prediction})
shap_df['abs_shap_value'] = shap_df['shap_value'].abs()
shap_df = shap_df.sort_values(by='abs_shap_value', ascending=False)
for _, row in shap_df.iterrows():
    print(f"  {row['feature']}: {row['shap_value']:.4f}")
print("\n")
print("2c. Local Rule-Based Explanation (Simplified IF-THEN rules):")
print(_get_local_rules_healthcare(lime_explainer, instance_to_explain, feature_names))
print("\n")
print("3. Actionable Insights: Counterfactual Explanation (To get 'No Disease'):")
desired_class = 0
counterfactual_result = _find_counterfactual_healthcare(black_box_model, instance_to_explain, feature_names, desired_class)
print(counterfactual_result)
print("\n")
print("4. Subgroup Divergence Analysis (Simplified):")
subgroup_definitions = {
    "Elderly Patients (age >= 65)": X_test[X_test['age'] >= 65],
    "High Blood Pressure (>140)": X_test[X_test['blood_pressure'] > 140],
    "No Family History": X_test[X_test['family_history'] == 0]
}
overall_accuracy = accuracy_score(y_test, black_box_model.predict(X_test))
print(f"Overall Model Accuracy: {overall_accuracy:.4f}")
for name, subgroup_X in subgroup_definitions.items():
    if not subgroup_X.empty:
        subgroup_y_true = y_test.loc[subgroup_X.index]
        subgroup_y_pred = black_box_model.predict(subgroup_X)
        subgroup_accuracy = accuracy_score(subgroup_y_true, subgroup_y_pred)
        divergence = overall_accuracy - subgroup_accuracy
        print(f"  Subgroup '{name}': Accuracy = {subgroup_accuracy:.4f}, Divergence (Overall - Subgroup) = {divergence:.4f}")
        if abs(divergence) > 0.05:
            print(f"    -> Significant divergence detected for this subgroup.")
print("\n")
print("5. Interactive Exploration (Simulated Output):")
print("  Imagine a medical dashboard where you can:")
print("  - View a patient's diagnosis and click for detailed LIME/SHAP explanations.")
print("  - Explore counterfactuals to understand what interventions might change a diagnosis.")
print("  - Analyze model performance and explanations across patient subgroups (e.g., by age, pre-existing conditions).")
print("  - Compare treatment outcomes for similar patients based on explanations.")
print("  Example: Displaying another patient's SHAP explanation:")
another_instance_idx = 7
another_instance = X_test.iloc[another_instance_idx].values
another_prediction = black_box_model.predict(another_instance.reshape(1, -1))[0]
print(f"  Patient instance {another_instance_idx} ({X_test.iloc[another_instance_idx].to_dict()}): Predicted {'Disease Present' if another_prediction == 1 else 'No Disease'}")
another_shap_values = shap_explainer.shap_values(another_instance)
another_shap_values_for_prediction = another_shap_values[1] if isinstance(another_shap_values, list) else another_shap_values
another_shap_df = pd.DataFrame({'feature': feature_names, 'shap_value': another_shap_values_for_prediction})
another_shap_df['abs_shap_value'] = another_shap_df['shap_value'].abs()
another_shap_df = another_shap_df.sort_values(by='abs_shap_value', ascending=False).head(3)
for _, row in another_shap_df.iterrows():
    print(f"    {row['feature']}: {row['shap_value']:.4f}")
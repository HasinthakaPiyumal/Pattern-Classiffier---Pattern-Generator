import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score
import lime
import lime.lime_tabular
import shap
import random
import warnings
warnings.filterwarnings("ignore")

def _get_local_rules_ecommerce(explainer_lime, instance, feature_names, top_features_count=3):
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
    rules.append(f"THEN Customer is {'Churned' if prediction == 1 else 'Not Churned'}")
    return "\n".join(rules)

def _find_counterfactual_ecommerce(model, original_instance, feature_names, desired_output_class, max_tries=100, step_factor=0.1):
    original_prediction = model.predict(original_instance.reshape(1, -1))[0]
    if original_prediction == desired_output_class:
        return f"Already predicts {'Churned' if desired_output_class == 1 else 'Not Churned'}. No counterfactual needed."
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
            if feature_name in ['num_purchases', 'avg_spend', 'last_login_days', 'support_tickets', 'product_page_views']:
                change_direction = random.choice([-1, 1])
                perturbation_amount = (original_value * step_factor) * change_direction
                temp_instance[idx] = max(0, original_value + perturbation_amount)
                current_changes[feature_name] = f"from {original_value:.2f} to {temp_instance[idx]:.2f}"
                num_features_changed += 1
            elif feature_name == 'subscription_type':
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
        return f"To change prediction from {'Churned' if original_prediction == 1 else 'Not Churned'} to {'Churned' if desired_output_class == 1 else 'Not Churned'}, minimally change: {best_counterfactual_changes}"
    else:
        return f"Could not find a simple counterfactual to achieve {'Churned' if desired_output_class == 1 else 'Not Churned'} within {max_tries} tries."

np.random.seed(42)
n_samples = 1000
data = {
    'num_purchases': np.random.randint(1, 50, n_samples),
    'avg_spend': np.random.uniform(10, 500, n_samples),
    'last_login_days': np.random.randint(1, 365, n_samples),
    'support_tickets': np.random.randint(0, 10, n_samples),
    'subscription_type': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
    'product_page_views': np.random.randint(10, 500, n_samples)
}
df = pd.DataFrame(data)
df['churned'] = ((df['last_login_days'] > 90) & (df['num_purchases'] < 5) & (df['avg_spend'] < 50) | (df['support_tickets'] > 5)).astype(int)
df.loc[(df['num_purchases'] > 30) & (df['avg_spend'] > 200), 'churned'] = 0
df.loc[df['product_page_views'] < 20, 'churned'] = 1
X = df.drop('churned', axis=1)
y = df['churned']
feature_names = X.columns.tolist()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
black_box_model = RandomForestClassifier(n_estimators=100, random_state=42)
black_box_model.fit(X_train, y_train)
print("--- E-commerce Customer Churn Prediction ---")
print(f"Black-box model accuracy: {accuracy_score(y_test, black_box_model.predict(X_test)):.4f}\n")
surrogate_model = DecisionTreeClassifier(max_depth=5, random_state=42)
surrogate_model.fit(X_train, black_box_model.predict(X_train))
print("1. Global Understanding: Decision Tree Surrogate Model (Approximating Black-Box Logic)")
print(export_text(surrogate_model, feature_names=feature_names, spacing=3))
print(f"Surrogate model accuracy (on black-box predictions): {accuracy_score(black_box_model.predict(X_test), surrogate_model.predict(X_test)):.4f}\n")
instance_idx = 0
instance_to_explain = X_test.iloc[instance_idx].values
original_prediction = black_box_model.predict(instance_to_explain.reshape(1, -1))[0]
print(f"Analyzing customer instance {instance_idx}: {X_test.iloc[instance_idx].to_dict()}")
print(f"Black-box model predicted: {'Churned' if original_prediction == 1 else 'Not Churned'}\n")
lime_explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=feature_names,
    class_names=['Not Churned', 'Churned'],
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
print(_get_local_rules_ecommerce(lime_explainer, instance_to_explain, feature_names))
print("\n")
print("3. Actionable Insights: Counterfactual Explanation (To get 'Not Churned'):")
desired_class = 0
counterfactual_result = _find_counterfactual_ecommerce(black_box_model, instance_to_explain, feature_names, desired_class)
print(counterfactual_result)
print("\n")
print("4. Subgroup Divergence Analysis (Simplified):")
subgroup_definitions = {
    "Low Engagement (last_login_days > 180)": X_test[X_test['last_login_days'] > 180],
    "High Spenders (avg_spend >= 250)": X_test[X_test['avg_spend'] >= 250],
    "Basic Subscription": X_test[X_test['subscription_type'] == 0]
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
print("  Imagine an e-commerce dashboard where you can:")
print("  - View a customer's churn risk and click for detailed LIME/SHAP explanations.")
print("  - Generate counterfactuals to suggest interventions (e.g., 'If customer buys X more items, churn risk drops').")
print("  - Analyze model performance and common churn reasons across customer segments (e.g., 'new customers', 'high-value customers').")
print("  - Identify divergent segments where the model struggles or exhibits bias.")
print("  Example: Displaying common rules for a 'High Spenders' subgroup (simulated):")
print("    For customers with 'avg_spend' > 250:")
print("      IF num_purchases > 20 AND last_login_days < 60 THEN 'Not Churned'")
print("      IF support_tickets > 3 AND product_page_views < 100 THEN 'Churned'")
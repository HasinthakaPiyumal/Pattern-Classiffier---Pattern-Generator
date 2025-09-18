import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import lime
import lime.lime_tabular
import shap
import dice_ml
from dice_ml.utils import helpers

np.random.seed(42)
n_samples = 1000
data = {
    'income': np.random.normal(50000, 15000, n_samples),
    'credit_score': np.random.randint(300, 850, n_samples),
    'loan_amount': np.random.normal(200000, 50000, n_samples),
    'debt_to_income': np.random.uniform(0.1, 0.6, n_samples),
    'employment_years': np.random.randint(0, 20, n_samples)
}
df = pd.DataFrame(data)
df['income'] = np.maximum(10000, df['income'])

df['loan_approved'] = ((df['income'] > 40000) &
                       (df['credit_score'] > 650) &
                       (df['debt_to_income'] < 0.4) &
                       (df['loan_amount'] < 300000)).astype(int)

X = df.drop('loan_approved', axis=1)
y = df['loan_approved']
feature_names = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

bb_model = RandomForestClassifier(n_estimators=100, random_state=42)
bb_model.fit(X_train, y_train)
print("Black-box model accuracy:", accuracy_score(y_test, bb_model.predict(X_test)))

surrogate_model = DecisionTreeClassifier(max_depth=5, random_state=42)
surrogate_model.fit(X_train, bb_model.predict(X_train))
print("\n--- Global Understanding (Decision Tree Surrogate) ---")
print("Surrogate model accuracy on black-box predictions:", accuracy_score(bb_model.predict(X_test), surrogate_model.predict(X_test)))

instance_idx = 0
instance_to_explain = X_test.iloc[[instance_idx]]
bb_prediction = bb_model.predict(instance_to_explain)[0]
bb_prediction_proba = bb_model.predict_proba(instance_to_explain)[0]
print(f"\n--- Local Explanation for Instance {instance_idx} ---")
print(f"Black-box prediction: {'Approved' if bb_prediction == 1 else 'Rejected'} (Proba: {bb_prediction_proba[bb_prediction]:.2f})")

explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=feature_names,
    class_names=['Rejected', 'Approved'],
    mode='classification'
)
lime_explanation = explainer.explain_instance(
    data_row=instance_to_explain.values[0],
    predict_fn=bb_model.predict_proba,
    num_features=5
)
print("\nLIME Explanation (Feature importance for this prediction):")
for feature, weight in lime_explanation.as_list():
    print(f"  {feature}: {weight:.4f}")

shap_explainer = shap.Explainer(bb_model, X_train)
shap_values = shap_explainer(instance_to_explain)
print("\nSHAP Explanation (Contribution of each feature):")
for i, feature in enumerate(feature_names):
    print(f"  {feature}: {shap_values.values[0][i]:.4f}")

print("\nLocal Rule-Based Explanation (Simulated):")
if instance_to_explain['credit_score'].values[0] > 700 and instance_to_explain['debt_to_income'].values[0] < 0.35:
    print(f"  IF Credit Score > 700 AND Debt-to-Income < 0.35 THEN loan is likely {bb_prediction_proba[1]:.2f} approved.")
else:
    print(f"  IF Credit Score <= 700 OR Debt-to-Income >= 0.35 THEN loan is likely {bb_prediction_proba[0]:.2f} rejected.")

print("\n--- Actionable Insights (Counterfactual Explanations) ---")
d = dice_ml.Data(
    dataframe=pd.concat([X_train, y_train], axis=1),
    continuous_features=feature_names,
    outcome_name='loan_approved'
)
m = dice_ml.Model(model=bb_model, backend='sklearn')
exp = dice_ml.Dice(d, m, method='random')

target_class = 1 - bb_prediction
cf_explanations = exp.generate_counterfactuals(
    instance_to_explain,
    total_CFs=1,
    desired_class=target_class
)
print(f"Counterfactuals to change prediction to {'Approved' if target_class == 1 else 'Rejected'}:")
if cf_explanations.cf_examples_list:
    for cf in cf_explanations.cf_examples_list:
        cf_df = cf.final_cfs_df
        print(cf_df)
        print("  Minimal changes required:")
        for col in feature_names:
            if instance_to_explain[col].values[0] != cf_df[col].values[0]:
                print(f"    {col}: {instance_to_explain[col].values[0]:.2f} -> {cf_df[col].values[0]:.2f}")
else:
    print("  No counterfactuals found for the desired class.")

print("\n--- Subgroup Analysis (Simulated Divergence) ---")
subgroup_mask = (X_test['income'] < 30000) & (X_test['debt_to_income'] > 0.45)
subgroup_X = X_test[subgroup_mask]
subgroup_y = y_test[subgroup_mask]

if not subgroup_X.empty:
    subgroup_predictions = bb_model.predict(subgroup_X)
    subgroup_accuracy = accuracy_score(subgroup_y, subgroup_predictions)
    overall_accuracy = accuracy_score(y_test, bb_model.predict(X_test))
    
    print(f"Subgroup 'Low Income, High Debt' ({len(subgroup_X)} instances):")
    print(f"  Subgroup Accuracy: {subgroup_accuracy:.2f}")
    print(f"  Overall Test Accuracy: {overall_accuracy:.2f}")
    if subgroup_accuracy < overall_accuracy * 0.9:
        print("  Divergence Detected: Model performs significantly worse in this subgroup.")
    else:
        print("  No significant divergence detected in this subgroup.")

    misclassified_subgroup = subgroup_X[subgroup_predictions != subgroup_y]
    if not misclassified_subgroup.empty:
        print(f"  {len(misclassified_subgroup)} misclassified instances in subgroup. Example misclassification:")
        mis_instance = misclassified_subgroup.iloc[[0]]
        mis_pred = bb_model.predict(mis_instance)[0]
        true_label = subgroup_y.loc[mis_instance.index[0]]
        print(f"    Features: {mis_instance.values[0]}")
        print(f"    Predicted: {'Approved' if mis_pred == 1 else 'Rejected'}, True: {'Approved' if true_label == 1 else 'Rejected'}")
else:
    print("No instances found for the 'Low Income, High Debt' subgroup in the test set.")

print("\n--- Interactive Exploration (Simulated) ---")
print("An interactive tool would allow users to:")
print("1. Select an instance and view its LIME, SHAP, and Counterfactual explanations.")
print("2. Filter data by subgroups and analyze their performance and common explanation patterns.")
print("3. Compare explanations for different instances or across different model versions.")
print("4. Drill down into the global surrogate model's decision rules.")
print("5. Perform 'what-if' analysis by manually changing input features and observing prediction changes.")
print("Example: A loan officer could use this to explain a rejection to an applicant, showing how to improve their profile.")
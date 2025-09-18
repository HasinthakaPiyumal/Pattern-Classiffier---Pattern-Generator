import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import lime
import lime.lime_tabular
import shap
import dice_ml
from dice_ml.utils import helpers

np.random.seed(43)
n_samples = 1200
data = {
    'age': np.random.randint(20, 80, n_samples),
    'bmi': np.random.normal(25, 5, n_samples),
    'blood_pressure': np.random.normal(120, 15, n_samples),
    'cholesterol': np.random.normal(200, 40, n_samples),
    'symptom_A': np.random.randint(0, 2, n_samples),
    'symptom_B': np.random.randint(0, 2, n_samples),
    'genetics_factor': np.random.uniform(0.1, 0.9, n_samples)
}
df = pd.DataFrame(data)

df['disease_present'] = ((df['age'] > 60) * 0.3 +
                         (df['bmi'] > 30) * 0.2 +
                         (df['blood_pressure'] > 140) * 0.25 +
                         (df['symptom_A'] == 1) * 0.15 +
                         (df['genetics_factor'] > 0.7) * 0.1).apply(lambda x: 1 if x > 0.5 else 0)

X = df.drop('disease_present', axis=1)
y = df['disease_present']
feature_names = X.columns.tolist()
categorical_features_indices = [feature_names.index('symptom_A'), feature_names.index('symptom_B')]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=43)

bb_model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=43)
bb_model.fit(X_train, y_train)
print("Black-box model accuracy:", accuracy_score(y_test, bb_model.predict(X_test)))

surrogate_model = LogisticRegression(solver='liblinear', random_state=43)
surrogate_model.fit(X_train, bb_model.predict(X_train))
print("\n--- Global Understanding (Logistic Regression Surrogate) ---")
print("Surrogate model accuracy on black-box predictions:", accuracy_score(bb_model.predict(X_test), surrogate_model.predict(X_test)))
print("Surrogate model coefficients (feature importance globally):")
for i, feature in enumerate(feature_names):
    print(f"  {feature}: {surrogate_model.coef_[0][i]:.4f}")

instance_idx = 5
instance_to_explain = X_test.iloc[[instance_idx]]
bb_prediction = bb_model.predict(instance_to_explain)[0]
bb_prediction_proba = bb_model.predict_proba(instance_to_explain)[0]
print(f"\n--- Local Explanation for Instance {instance_idx} (Patient ID {instance_to_explain.index[0]}) ---")
print(f"Black-box prediction: {'Disease Present' if bb_prediction == 1 else 'Disease Absent'} (Proba: {bb_prediction_proba[bb_prediction]:.2f})")

explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=feature_names,
    class_names=['Disease Absent', 'Disease Present'],
    mode='classification',
    categorical_features=categorical_features_indices
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
age_val = instance_to_explain['age'].values[0]
bp_val = instance_to_explain['blood_pressure'].values[0]
if age_val > 65 and bp_val > 150:
    print(f"  IF Age > 65 AND Blood Pressure > 150 THEN Disease is highly likely present ({bb_prediction_proba[1]:.2f}).")
elif age_val < 40 and bp_val < 120:
    print(f"  IF Age < 40 AND Blood Pressure < 120 THEN Disease is highly likely absent ({bb_prediction_proba[0]:.2f}).")
else:
    print(f"  No simple rule for this specific combination, but general factors lead to {bb_prediction_proba[bb_prediction]:.2f} {['absence', 'presence'][bb_prediction]}.")

print("\n--- Actionable Insights (Counterfactual Explanations) ---")
d = dice_ml.Data(
    dataframe=pd.concat([X_train, y_train], axis=1),
    continuous_features=[f for f in feature_names if f not in ['symptom_A', 'symptom_B']],
    outcome_name='disease_present'
)
m = dice_ml.Model(model=bb_model, backend='sklearn')
exp = dice_ml.Dice(d, m, method='random')

target_class = 1 - bb_prediction
cf_explanations = exp.generate_counterfactuals(
    instance_to_explain,
    total_CFs=1,
    desired_class=target_class
)
print(f"Counterfactuals to change prediction to {'Disease Present' if target_class == 1 else 'Disease Absent'}:")
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
subgroup_mask = (X_test['age'] > 70) & (X_test['bmi'] > 30)
subgroup_X = X_test[subgroup_mask]
subgroup_y = y_test[subgroup_mask]

if not subgroup_X.empty:
    subgroup_predictions = bb_model.predict(subgroup_X)
    subgroup_accuracy = accuracy_score(subgroup_y, subgroup_predictions)
    overall_accuracy = accuracy_score(y_test, bb_model.predict(X_test))
    
    print(f"Subgroup 'Elderly with high BMI' ({len(subgroup_X)} instances):")
    print(f"  Subgroup Accuracy: {subgroup_accuracy:.2f}")
    print(f"  Overall Test Accuracy: {overall_accuracy:.2f}")
    if subgroup_accuracy < overall_accuracy * 0.85:
        print("  Divergence Detected: Model performs significantly worse in this subgroup (potential bias).")
    else:
        print("  No significant divergence detected in this subgroup.")

    misclassified_subgroup = subgroup_X[subgroup_predictions != subgroup_y]
    if not misclassified_subgroup.empty:
        print(f"  {len(misclassified_subgroup)} misclassified instances in subgroup. Example misclassification:")
        mis_instance = misclassified_subgroup.iloc[[0]]
        mis_pred = bb_model.predict(mis_instance)[0]
        true_label = subgroup_y.loc[mis_instance.index[0]]
        print(f"    Features: {mis_instance.values[0]}")
        print(f"    Predicted: {'Present' if mis_pred == 1 else 'Absent'}, True: {'Present' if true_label == 1 else 'Absent'}")
else:
    print("No instances found for the 'Elderly with high BMI' subgroup in the test set.")

print("\n--- Interactive Exploration (Simulated) ---")
print("A healthcare professional could use an interactive tool to:")
print("1. Understand global factors influencing disease prediction (surrogate model).")
print("2. Explain a specific patient's diagnosis to them, highlighting key contributing factors (LIME/SHAP).")
print("3. Explore 'what-if' scenarios for a patient to see what changes might alter a diagnosis (counterfactuals).")
print("4. Identify patient subgroups where the AI model might be less reliable or biased, guiding further clinical review.")
print("5. Investigate local rules that lead to a specific diagnosis for better clinical insights.")
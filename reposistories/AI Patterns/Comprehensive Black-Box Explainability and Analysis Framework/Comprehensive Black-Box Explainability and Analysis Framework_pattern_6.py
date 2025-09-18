import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

np.random.seed(43)
n_samples = 600
age = np.random.randint(20, 80, size=n_samples)
body_temp = np.random.normal(loc=98.6, scale=1.5, size=n_samples)
cough_severity = np.random.randint(0, 5, size=n_samples)
fever_duration = np.random.normal(loc=2, scale=1, size=n_samples)
fatigue_level = np.random.randint(0, 4, size=n_samples)

y_true = ((body_temp > 100) & (cough_severity > 2) & (fever_duration > 3) & (age > 50) & (fatigue_level > 1)).astype(int)
y_true = np.where(np.random.rand(n_samples) < 0.15, 1 - y_true, y_true)

X = np.column_stack([age, body_temp, cough_severity, fever_duration, fatigue_level])
feature_names = ['Age', 'Body Temp', 'Cough Severity', 'Fever Duration', 'Fatigue Level']

X_train, X_test, y_train, y_test = train_test_split(X, y_true, test_size=0.2, random_state=43)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

black_box_model = GradientBoostingClassifier(n_estimators=100, random_state=43)
black_box_model.fit(X_train_scaled, y_train)
black_box_predictions = black_box_model.predict(X_test_scaled)
black_box_proba = black_box_model.predict_proba(X_test_scaled)

print(f"Black-Box Model Accuracy: {accuracy_score(y_test, black_box_predictions):.2f}")

global_surrogate = LogisticRegression(random_state=43, solver='liblinear')
global_surrogate.fit(X_train_scaled, black_box_model.predict(X_train_scaled))
print("\n--- Global Understanding (Logistic Regression Surrogate) ---")
print(f"Global Surrogate Model Accuracy (on black-box predictions): {accuracy_score(black_box_model.predict(X_test_scaled), global_surrogate.predict(X_test_scaled)):.2f}")
print(f"Global Surrogate Coefficients: {dict(zip(feature_names, global_surrogate.coef_[0].round(2)))}")

instance_idx = 5
instance_X_scaled = X_test_scaled[instance_idx].reshape(1, -1)
instance_original_X = X_test[instance_idx]
black_box_pred = black_box_model.predict(instance_X_scaled)[0]
black_box_pred_proba = black_box_model.predict_proba(instance_X_scaled)[0, black_box_pred]

print(f"\n--- Local Explanation for Instance {instance_idx} (Patient Diagnosis) ---")
print(f"Original features: {dict(zip(feature_names, instance_original_X.round(2)))}")
print(f"Black-box model predicts: {'Disease Present' if black_box_pred == 1 else 'Disease Absent'} (Probability: {black_box_pred_proba:.2f})")

def simulate_lime_health(instance_scaled, feature_names, prediction, mean_scaled_features):
    local_importance = {}
    for i, feature in enumerate(feature_names):
        diff = instance_scaled[0, i] - mean_scaled_features[i]
        if prediction == 1: 
            if feature in ['Body Temp', 'Cough Severity', 'Fever Duration', 'Fatigue Level'] and diff > 0.5: local_importance[feature] = f"High {feature} (+)"
            elif feature == 'Age' and diff > 1.0: local_importance[feature] = f"Older Age (+)"
        else: 
            if feature in ['Body Temp', 'Cough Severity', 'Fever Duration', 'Fatigue Level'] and diff < -0.5: local_importance[feature] = f"Low {feature} (-)"
    return local_importance if local_importance else {"No strong local features identified"}

mean_scaled_features = np.mean(X_train_scaled, axis=0)
lime_explanation = simulate_lime_health(instance_X_scaled, feature_names, black_box_pred, mean_scaled_features)
print(f"  LIME-like Explanation: {lime_explanation}")

def simulate_shap_health(instance_scaled, feature_names, prediction):
    shap_values = {}
    weights = np.array([0.2, 0.5, 0.4, 0.3, 0.35]) 
    for i, feature in enumerate(feature_names):
        contribution = instance_scaled[0, i] * weights[i]
        if prediction == 0: contribution = -contribution 
        shap_values[feature] = contribution
    sorted_shap = sorted(shap_values.items(), key=lambda item: abs(item[1]), reverse=True)
    return {k: f"{v:.2f}" for k, v in sorted_shap}

shap_explanation = simulate_shap_health(instance_X_scaled, feature_names, black_box_pred)
print(f"  SHAP-like Explanation (feature contributions): {shap_explanation}")

def simulate_rule_explanation_health(original_instance, feature_names, prediction):
    rules = []
    age_val = original_instance[feature_names.index('Age')]
    body_temp_val = original_instance[feature_names.index('Body Temp')]
    cough_val = original_instance[feature_names.index('Cough Severity')]
    fever_val = original_instance[feature_names.index('Fever Duration')]

    if prediction == 1: 
        if body_temp_val > 101.0: rules.append(f"IF Body Temp > 101.0F (actual: {body_temp_val:.1f}F) THEN likely Disease Present")
        if cough_val >= 3: rules.append(f"IF Cough Severity is High (actual: {cough_val}) THEN likely Disease Present")
        if fever_val > 4: rules.append(f"IF Fever Duration > 4 days (actual: {fever_val:.1f} days) THEN likely Disease Present")
        if age_val > 65: rules.append(f"IF Age > 65 (actual: {age_val}) THEN likely Disease Present")
    else: 
        if body_temp_val < 99.0: rules.append(f"IF Body Temp < 99.0F (actual: {body_temp_val:.1f}F) THEN likely Disease Absent")
        if cough_val == 0: rules.append(f"IF No Cough (actual: {cough_val}) THEN likely Disease Absent")
    return rules if rules else ["No specific local rule found matching current thresholds."]

rule_explanation = simulate_rule_explanation_health(instance_original_X, feature_names, black_box_pred)
print(f"  Rule-Based Explanation: {rule_explanation}")

def simulate_counterfactual_health(instance_scaled, original_instance, model, scaler, feature_names, target_pred):
    current_pred = model.predict(instance_scaled)[0]
    if current_pred == target_pred:
        return "Already predicts desired outcome."

    temp_original_instance = original_instance.copy()
    
    if target_pred == 0 and current_pred == 1: 
        temp_idx = feature_names.index('Body Temp')
        cough_idx = feature_names.index('Cough Severity')

        proposed_temp = temp_original_instance[temp_idx] - 2.0 
        temp_original_instance_s1 = temp_original_instance.copy()
        temp_original_instance_s1[temp_idx] = proposed_temp
        temp_scaled_s1 = scaler.transform(temp_original_instance_s1.reshape(1, -1))
        if model.predict(temp_scaled_s1)[0] == 0:
            return f"To get Disease Absent: Decrease Body Temp to {proposed_temp:.1f}F (from {original_instance[temp_idx]:.1f}F)."

        proposed_cough = max(0, temp_original_instance[cough_idx] - 2) 
        temp_original_instance_s2 = temp_original_instance.copy()
        temp_original_instance_s2[cough_idx] = proposed_cough
        temp_scaled_s2 = scaler.transform(temp_original_instance_s2.reshape(1, -1))
        if model.predict(temp_scaled_s2)[0] == 0:
            return f"To get Disease Absent: Decrease Cough Severity to {proposed_cough} (from {original_instance[cough_idx]})."

    return "No simple counterfactual found to flip prediction with reasonable changes."

counterfactual_explanation = simulate_counterfactual_health(instance_X_scaled, instance_original_X, black_box_model, scaler, feature_names, target_pred=0)
print(f"\n--- Actionable Insights (Counterfactual) ---")
print(f"  Counterfactual: {counterfactual_explanation}")

print(f"\n--- Subgroup Analysis ---")
subgroup_mask = (X_test[:, feature_names.index('Age')] > 60) & \
                (X_test[:, feature_names.index('Body Temp')] > 100) & \
                (X_test[:, feature_names.index('Fever Duration')] > 3)
subgroup_X_scaled = X_test_scaled[subgroup_mask]
subgroup_y_true = y_test[subgroup_mask]

if len(subgroup_X_scaled) > 0:
    subgroup_predictions = black_box_model.predict(subgroup_X_scaled)
    subgroup_accuracy = accuracy_score(subgroup_y_true, subgroup_predictions)
    overall_accuracy = accuracy_score(y_test, black_box_predictions)

    print(f"  Subgroup: 'Elderly Patients with High Fever & Long Duration Fever' (N={len(subgroup_X_scaled)}) ")
    print(f"    Subgroup Accuracy: {subgroup_accuracy:.2f}")
    print(f"    Overall Test Accuracy: {overall_accuracy:.2f}")
    
    if abs(subgroup_accuracy - overall_accuracy) > 0.15: 
        print(f"    Divergence Detected: Model performance significantly different for this subgroup. May require specific model tuning.")
    else:
        print(f"    No significant divergence detected for this subgroup.")
else:
    print("  No instances found in the defined subgroup for analysis.")

print(f"\n--- Interactive Exploration (Simulated UI Output) ---")
print(f"User selected patient {instance_idx} for detailed diagnosis analysis:")
print(f"  - Black-box prediction: {'Disease Present' if black_box_pred == 1 else 'Disease Absent'}")
print(f"  - Top local symptoms (LIME-like): {lime_explanation}")
print(f"  - Symptom contributions (SHAP-like): {shap_explanation}")
print(f"  - Applicable diagnostic rules: {rule_explanation}")
print(f"  - Counterfactual scenario: {counterfactual_explanation}")
print(f"\nUser explored 'Elderly Patients with High Fever & Long Duration Fever' subgroup:")
print(f"  - Subgroup performance: Accuracy {subgroup_accuracy:.2f} (vs. overall {overall_accuracy:.2f})")
print(f"  - Divergence analysis: Model potentially underperforming for this critical segment. Clinical review recommended.")
print(f"  - Action: Investigate specific false positives/negatives within this subgroup.")
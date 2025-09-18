import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n_samples = 500
income = np.random.normal(loc=60000, scale=20000, size=n_samples)
credit_score = np.random.normal(loc=700, scale=50, size=n_samples)
loan_amount = np.random.normal(loc=150000, scale=50000, size=n_samples)
debt_to_income = np.random.normal(loc=0.3, scale=0.1, size=n_samples)
employment_years = np.random.randint(1, 20, size=n_samples)

y_true = ((income > 50000) & (credit_score > 650) & (loan_amount < 200000) & (debt_to_income < 0.4)).astype(int)
y_true = np.where(np.random.rand(n_samples) < 0.1, 1 - y_true, y_true)

X = np.column_stack([income, credit_score, loan_amount, debt_to_income, employment_years])
feature_names = ['Income', 'Credit Score', 'Loan Amount', 'Debt-to-Income', 'Employment Years']

X_train, X_test, y_train, y_test = train_test_split(X, y_true, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

black_box_model = RandomForestClassifier(n_estimators=100, random_state=42)
black_box_model.fit(X_train_scaled, y_train)
black_box_predictions = black_box_model.predict(X_test_scaled)
black_box_proba = black_box_model.predict_proba(X_test_scaled)

print(f"Black-Box Model Accuracy: {accuracy_score(y_test, black_box_predictions):.2f}")

global_surrogate = DecisionTreeClassifier(max_depth=4, random_state=42)
global_surrogate.fit(X_train_scaled, black_box_model.predict(X_train_scaled))
print("\n--- Global Understanding (Decision Tree Surrogate) ---")
print(f"Global Surrogate Model Accuracy (on black-box predictions): {accuracy_score(black_box_model.predict(X_test_scaled), global_surrogate.predict(X_test_scaled)):.2f}")

instance_idx = 0
instance_X_scaled = X_test_scaled[instance_idx].reshape(1, -1)
instance_original_X = X_test[instance_idx]
black_box_pred = black_box_model.predict(instance_X_scaled)[0]
black_box_pred_proba = black_box_model.predict_proba(instance_X_scaled)[0, black_box_pred]

print(f"\n--- Local Explanation for Instance {instance_idx} (Loan Application) ---")
print(f"Original features: {dict(zip(feature_names, instance_original_X.round(2)))}")
print(f"Black-box model predicts: {'Approved' if black_box_pred == 1 else 'Rejected'} (Probability: {black_box_pred_proba:.2f})")

def simulate_lime(instance_scaled, feature_names, prediction, mean_scaled_features):
    local_importance = {}
    for i, feature in enumerate(feature_names):
        diff = instance_scaled[0, i] - mean_scaled_features[i]
        if prediction == 1: 
            if diff > 0.5: local_importance[feature] = f"High {feature} (+)"
            elif diff < -0.5: local_importance[feature] = f"Low {feature} (-)"
        else: 
            if diff > 0.5: local_importance[feature] = f"High {feature} (-)"
            elif diff < -0.5: local_importance[feature] = f"Low {feature} (+)"
    return local_importance if local_importance else {"No strong local features identified"}

mean_scaled_features = np.mean(X_train_scaled, axis=0)
lime_explanation = simulate_lime(instance_X_scaled, feature_names, black_box_pred, mean_scaled_features)
print(f"  LIME-like Explanation: {lime_explanation}")

def simulate_shap(instance_scaled, feature_names, prediction):
    shap_values = {}
    weights = np.array([0.5, 0.4, -0.3, -0.2, 0.1])
    for i, feature in enumerate(feature_names):
        contribution = instance_scaled[0, i] * weights[i]
        if prediction == 0: contribution = -contribution 
        shap_values[feature] = contribution
    sorted_shap = sorted(shap_values.items(), key=lambda item: abs(item[1]), reverse=True)
    return {k: f"{v:.2f}" for k, v in sorted_shap}

shap_explanation = simulate_shap(instance_X_scaled, feature_names, black_box_pred)
print(f"  SHAP-like Explanation (feature contributions): {shap_explanation}")

def simulate_rule_explanation(original_instance, feature_names, prediction):
    rules = []
    income_val = original_instance[feature_names.index('Income')]
    credit_score_val = original_instance[feature_names.index('Credit Score')]
    loan_amount_val = original_instance[feature_names.index('Loan Amount')]

    if prediction == 1: 
        if income_val > 75000: rules.append(f"IF Income > $75k (actual: ${income_val:.0f}) THEN likely Approved")
        if credit_score_val > 720: rules.append(f"IF Credit Score > 720 (actual: {credit_score_val:.0f}) THEN likely Approved")
        if loan_amount_val < 120000: rules.append(f"IF Loan Amount < $120k (actual: ${loan_amount_val:.0f}) THEN likely Approved")
    else: 
        if income_val < 45000: rules.append(f"IF Income < $45k (actual: ${income_val:.0f}) THEN likely Rejected")
        if credit_score_val < 620: rules.append(f"IF Credit Score < 620 (actual: {credit_score_val:.0f}) THEN likely Rejected")
        if loan_amount_val > 220000: rules.append(f"IF Loan Amount > $220k (actual: ${loan_amount_val:.0f}) THEN likely Rejected")
    return rules if rules else ["No specific local rule found matching current thresholds."]

rule_explanation = simulate_rule_explanation(instance_original_X, feature_names, black_box_pred)
print(f"  Rule-Based Explanation: {rule_explanation}")

def simulate_counterfactual(instance_scaled, original_instance, model, scaler, feature_names, target_pred):
    current_pred = model.predict(instance_scaled)[0]
    if current_pred == target_pred:
        return "Already predicts desired outcome."

    temp_original_instance = original_instance.copy()
    
    if target_pred == 1 and current_pred == 0: 
        income_idx = feature_names.index('Income')
        credit_idx = feature_names.index('Credit Score')
        loan_idx = feature_names.index('Loan Amount')

        proposed_income = temp_original_instance[income_idx] + 20000 
        temp_original_instance_s1 = temp_original_instance.copy()
        temp_original_instance_s1[income_idx] = proposed_income
        temp_scaled_s1 = scaler.transform(temp_original_instance_s1.reshape(1, -1))
        if model.predict(temp_scaled_s1)[0] == 1:
            return f"To get approved: Increase Income to ${proposed_income:.0f} (from ${original_instance[income_idx]:.0f})."

        proposed_credit_score = temp_original_instance[credit_idx] + 50
        temp_original_instance_s2 = temp_original_instance.copy()
        temp_original_instance_s2[credit_idx] = proposed_credit_score
        temp_scaled_s2 = scaler.transform(temp_original_instance_s2.reshape(1, -1))
        if model.predict(temp_scaled_s2)[0] == 1:
            return f"To get approved: Increase Credit Score to {proposed_credit_score:.0f} (from {original_instance[credit_idx]:.0f})."

        proposed_loan_amount = temp_original_instance[loan_idx] - 30000
        if proposed_loan_amount > 10000: 
            temp_original_instance_s3 = temp_original_instance.copy()
            temp_original_instance_s3[loan_idx] = proposed_loan_amount
            temp_scaled_s3 = scaler.transform(temp_original_instance_s3.reshape(1, -1))
            if model.predict(temp_scaled_s3)[0] == 1:
                return f"To get approved: Decrease Loan Amount to ${proposed_loan_amount:.0f} (from ${original_instance[loan_idx]:.0f})."

    return "No simple counterfactual found to flip prediction with reasonable changes."

counterfactual_explanation = simulate_counterfactual(instance_X_scaled, instance_original_X, black_box_model, scaler, feature_names, target_pred=1)
print(f"\n--- Actionable Insights (Counterfactual) ---")
print(f"  Counterfactual: {counterfactual_explanation}")

print(f"\n--- Subgroup Analysis ---")
subgroup_mask = (X_test[:, feature_names.index('Loan Amount')] > 200000) & \
                (X_test[:, feature_names.index('Credit Score')] < 650) & \
                (X_test[:, feature_names.index('Income')] < 50000)
subgroup_X_scaled = X_test_scaled[subgroup_mask]
subgroup_y_true = y_test[subgroup_mask]

if len(subgroup_X_scaled) > 0:
    subgroup_predictions = black_box_model.predict(subgroup_X_scaled)
    subgroup_accuracy = accuracy_score(subgroup_y_true, subgroup_predictions)
    overall_accuracy = accuracy_score(y_test, black_box_predictions)

    print(f"  Subgroup: 'High Loan Amount, Low Credit Score & Low Income' (N={len(subgroup_X_scaled)}) ")
    print(f"    Subgroup Accuracy: {subgroup_accuracy:.2f}")
    print(f"    Overall Test Accuracy: {overall_accuracy:.2f}")
    
    if abs(subgroup_accuracy - overall_accuracy) > 0.15: 
        print(f"    Divergence Detected: Model performance significantly lower for this subgroup. Potential bias or underperformance identified.")
    else:
        print(f"    No significant divergence detected for this subgroup.")
else:
    print("  No instances found in the defined subgroup for analysis.")

print(f"\n--- Interactive Exploration (Simulated UI Output) ---")
print(f"User selected instance {instance_idx} for detailed loan application analysis:")
print(f"  - Black-box prediction: {'Approved' if black_box_pred == 1 else 'Rejected'}")
print(f"  - Top local features (LIME-like): {lime_explanation}")
print(f"  - Feature contributions (SHAP-like): {shap_explanation}")
print(f"  - Applicable rules: {rule_explanation}")
print(f"  - Counterfactual scenario: {counterfactual_explanation}")
print(f"\nUser explored 'High Loan Amount, Low Credit Score & Low Income' subgroup:")
print(f"  - Subgroup performance: Accuracy {subgroup_accuracy:.2f} (vs. overall {overall_accuracy:.2f})")
print(f"  - Divergence analysis: Model potentially biased or underperforming for this segment. Further investigation needed.")
print(f"  - Action: Review model's decision boundary for similar cases in this subgroup.")
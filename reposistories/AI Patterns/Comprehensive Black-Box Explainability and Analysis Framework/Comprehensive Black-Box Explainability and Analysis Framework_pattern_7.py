import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

np.random.seed(44)
n_samples = 700
user_age = np.random.randint(18, 70, size=n_samples)
user_spend = np.random.normal(loc=500, scale=300, size=n_samples)
product_price = np.random.normal(loc=100, scale=50, size=n_samples)
product_category = np.random.choice(['Electronics', 'Books', 'Clothing', 'Home'], size=n_samples)
user_prev_views = np.random.randint(0, 10, size=n_samples)

product_category_map_int = {'Electronics':0, 'Books':1, 'Clothing':2, 'Home':3}
product_category_encoded = np.array([product_category_map_int[c] for c in product_category])

y_true = ((user_spend > 300) & (product_price < 150) & (user_prev_views > 2)).astype(int)
y_true = np.where(np.random.rand(n_samples) < 0.2, 1 - y_true, y_true)

X = np.column_stack([user_age, user_spend, product_price, product_category_encoded, user_prev_views])
feature_names = ['User Age', 'User Spend', 'Product Price', 'Product Category', 'Previous Views']

X_train, X_test, y_train, y_test = train_test_split(X, y_true, test_size=0.2, random_state=44)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

black_box_model = XGBClassifier(n_estimators=100, random_state=44, use_label_encoder=False, eval_metric='logloss')
black_box_model.fit(X_train_scaled, y_train)
black_box_predictions = black_box_model.predict(X_test_scaled)
black_box_proba = black_box_model.predict_proba(X_test_scaled)

print(f"Black-Box Model Accuracy: {accuracy_score(y_test, black_box_predictions):.2f}")

global_surrogate = KNeighborsClassifier(n_neighbors=5)
global_surrogate.fit(X_train_scaled, black_box_model.predict(X_train_scaled))
print("\n--- Global Understanding (K-Neighbors Surrogate) ---")
print(f"Global Surrogate Model Accuracy (on black-box predictions): {accuracy_score(black_box_model.predict(X_test_scaled), global_surrogate.predict(X_test_scaled)):.2f}")

instance_idx = 10
instance_X_scaled = X_test_scaled[instance_idx].reshape(1, -1)
instance_original_X = X_test[instance_idx]
black_box_pred = black_box_model.predict(instance_X_scaled)[0]
black_box_pred_proba = black_box_model.predict_proba(instance_X_scaled)[0, black_box_pred]

product_category_map_str = {0:'Electronics', 1:'Books', 2:'Clothing', 3:'Home'}
original_features_display = dict(zip(feature_names, instance_original_X.round(2)))
original_features_display['Product Category'] = product_category_map_str[int(original_features_display['Product Category'])]

print(f"\n--- Local Explanation for Instance {instance_idx} (Product Recommendation) ---")
print(f"Original features: {original_features_display}")
print(f"Black-box model predicts: {'Will Buy' if black_box_pred == 1 else 'Will Not Buy'} (Probability: {black_box_pred_proba:.2f})")

def simulate_lime_ecommerce(instance_scaled, feature_names, prediction, mean_scaled_features, category_map_str, original_instance):
    local_importance = {}
    for i, feature in enumerate(feature_names):
        diff = instance_scaled[0, i] - mean_scaled_features[i]
        if prediction == 1: 
            if feature == 'User Spend' and diff > 0.5: local_importance[feature] = f"High {feature} (+)"
            elif feature == 'Product Price' and diff < -0.5: local_importance[feature] = f"Low {feature} (+)"
            elif feature == 'Previous Views' and diff > 0.5: local_importance[feature] = f"High {feature} (+)"
        else: 
            if feature == 'User Spend' and diff < -0.5: local_importance[feature] = f"Low {feature} (-)"
            elif feature == 'Product Price' and diff > 0.5: local_importance[feature] = f"High {feature} (-)"
    if 'Product Category' in feature_names:
        cat_val = int(original_instance[feature_names.index('Product Category')])
        if cat_val in category_map_str: local_importance['Product Category'] = f"{category_map_str[cat_val]} category relevant."
    return local_importance if local_importance else {"No strong local features identified"}

mean_scaled_features = np.mean(X_train_scaled, axis=0)
lime_explanation = simulate_lime_ecommerce(instance_X_scaled, feature_names, black_box_pred, mean_scaled_features, product_category_map_str, instance_original_X)
print(f"  LIME-like Explanation: {lime_explanation}")

def simulate_shap_ecommerce(instance_scaled, feature_names, prediction):
    shap_values = {}
    weights = np.array([0.1, 0.4, -0.3, 0.05, 0.35]) 
    for i, feature in enumerate(feature_names):
        contribution = instance_scaled[0, i] * weights[i]
        if prediction == 0: contribution = -contribution 
        shap_values[feature] = contribution
    sorted_shap = sorted(shap_values.items(), key=lambda item: abs(item[1]), reverse=True)
    return {k: f"{v:.2f}" for k, v in sorted_shap}

shap_explanation = simulate_shap_ecommerce(instance_X_scaled, feature_names, black_box_pred)
print(f"  SHAP-like Explanation (feature contributions): {shap_explanation}")

def simulate_rule_explanation_ecommerce(original_instance, feature_names, prediction, category_map_str):
    rules = []
    user_spend_val = original_instance[feature_names.index('User Spend')]
    product_price_val = original_instance[feature_names.index('Product Price')]
    prev_views_val = original_instance[feature_names.index('Previous Views')]
    product_cat_val = category_map_str[int(original_instance[feature_names.index('Product Category')])]

    if prediction == 1: 
        if user_spend_val > 600: rules.append(f"IF User Spend > $600 (actual: ${user_spend_val:.0f}) THEN likely Will Buy")
        if product_price_val < 80: rules.append(f"IF Product Price < $80 (actual: ${product_price_val:.0f}) THEN likely Will Buy")
        if prev_views_val > 4: rules.append(f"IF Previous Views > 4 (actual: {prev_views_val}) THEN likely Will Buy")
        if product_cat_val == 'Electronics': rules.append(f"IF Product Category is 'Electronics' THEN likely Will Buy")
    else: 
        if user_spend_val < 200: rules.append(f"IF User Spend < $200 (actual: ${user_spend_val:.0f}) THEN likely Will Not Buy")
        if product_price_val > 180: rules.append(f"IF Product Price > $180 (actual: ${product_price_val:.0f}) THEN likely Will Not Buy")
    return rules if rules else ["No specific local rule found matching current thresholds."]

rule_explanation = simulate_rule_explanation_ecommerce(instance_original_X, feature_names, black_box_pred, product_category_map_str)
print(f"  Rule-Based Explanation: {rule_explanation}")

def simulate_counterfactual_ecommerce(instance_scaled, original_instance, model, scaler, feature_names, target_pred):
    current_pred = model.predict(instance_scaled)[0]
    if current_pred == target_pred:
        return "Already predicts desired outcome."

    temp_original_instance = original_instance.copy()
    
    if target_pred == 1 and current_pred == 0: 
        spend_idx = feature_names.index('User Spend')
        price_idx = feature_names.index('Product Price')
        views_idx = feature_names.index('Previous Views')

        proposed_spend = temp_original_instance[spend_idx] + 200
        temp_original_instance_s1 = temp_original_instance.copy()
        temp_original_instance_s1[spend_idx] = proposed_spend
        temp_scaled_s1 = scaler.transform(temp_original_instance_s1.reshape(1, -1))
        if model.predict(temp_scaled_s1)[0] == 1:
            return f"To get 'Will Buy': Increase User Spend to ${proposed_spend:.0f} (from ${original_instance[spend_idx]:.0f})."

        proposed_price = temp_original_instance[price_idx] - 50
        if proposed_price > 20: 
            temp_original_instance_s2 = temp_original_instance.copy()
            temp_original_instance_s2[price_idx] = proposed_price
            temp_scaled_s2 = scaler.transform(temp_original_instance_s2.reshape(1, -1))
            if model.predict(temp_scaled_s2)[0] == 1:
                return f"To get 'Will Buy': Decrease Product Price to ${proposed_price:.0f} (from ${original_instance[price_idx]:.0f})."

        proposed_views = temp_original_instance[views_idx] + 3
        if proposed_views < 15: 
            temp_original_instance_s3 = temp_original_instance.copy()
            temp_original_instance_s3[views_idx] = proposed_views
            temp_scaled_s3 = scaler.transform(temp_original_instance_s3.reshape(1, -1))
            if model.predict(temp_scaled_s3)[0] == 1:
                return f"To get 'Will Buy': Increase Previous Views to {proposed_views:.0f} (from {original_instance[views_idx]:.0f})."

    return "No simple counterfactual found to flip prediction with reasonable changes."

counterfactual_explanation = simulate_counterfactual_ecommerce(instance_X_scaled, instance_original_X, black_box_model, scaler, feature_names, target_pred=1)
print(f"\n--- Actionable Insights (Counterfactual) ---")
print(f"  Counterfactual: {counterfactual_explanation}")

print(f"\n--- Subgroup Analysis ---")
subgroup_mask = (X_test[:, feature_names.index('User Age')] < 25) & \
                (X_test[:, feature_names.index('User Spend')] < 200) & \
                (X_test[:, feature_names.index('Product Category')] == product_category_map_int['Electronics'])
subgroup_X_scaled = X_test_scaled[subgroup_mask]
subgroup_y_true = y_test[subgroup_mask]

if len(subgroup_X_scaled) > 0:
    subgroup_predictions = black_box_model.predict(subgroup_X_scaled)
    subgroup_accuracy = accuracy_score(subgroup_y_true, subgroup_predictions)
    overall_accuracy = accuracy_score(y_test, black_box_predictions)

    print(f"  Subgroup: 'Young, Low-Spending Users interested in Electronics' (N={len(subgroup_X_scaled)}) ")
    print(f"    Subgroup Accuracy: {subgroup_accuracy:.2f}")
    print(f"    Overall Test Accuracy: {overall_accuracy:.2f}")
    
    if abs(subgroup_accuracy - overall_accuracy) > 0.15: 
        print(f"    Divergence Detected: Model performance significantly different for this subgroup. Recommendations might be suboptimal.")
    else:
        print(f"    No significant divergence detected for this subgroup.")
else:
    print("  No instances found in the defined subgroup for analysis.")

print(f"\n--- Interactive Exploration (Simulated UI Output) ---")
print(f"User selected recommendation instance {instance_idx} for detailed analysis:")
print(f"  - Black-box prediction: {'Will Buy' if black_box_pred == 1 else 'Will Not Buy'}")
print(f"  - Top local features (LIME-like): {lime_explanation}")
print(f"  - Feature contributions (SHAP-like): {shap_explanation}")
print(f"  - Applicable recommendation rules: {rule_explanation}")
print(f"  - Counterfactual scenario: {counterfactual_explanation}")
print(f"\nUser explored 'Young, Low-Spending Users interested in Electronics' subgroup:")
print(f"  - Subgroup performance: Accuracy {subgroup_accuracy:.2f} (vs. overall {overall_accuracy:.2f})")
print(f"  - Divergence analysis: Model potentially mis-recommending for this segment. Review product targeting.")
print(f"  - Action: Consider A/B testing alternative recommendation strategies for this user segment.")
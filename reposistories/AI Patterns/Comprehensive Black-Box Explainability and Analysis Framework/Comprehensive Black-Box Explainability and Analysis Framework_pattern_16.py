import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import lime
import lime.lime_tabular
import shap
import dice_ml
from dice_ml.utils import helpers

np.random.seed(44)
n_samples = 1500
data = {
    'user_age': np.random.randint(18, 70, n_samples),
    'user_spend_per_month': np.random.normal(100, 50, n_samples),
    'product_price': np.random.normal(50, 30, n_samples),
    'product_category_idx': np.random.randint(0, 5, n_samples),
    'product_rating_avg': np.random.uniform(2.5, 5.0, n_samples),
    'time_on_page_min': np.random.uniform(0.5, 10.0, n_samples)
}
df = pd.DataFrame(data)
df['user_spend_per_month'] = np.maximum(10, df['user_spend_per_month'])
df['product_price'] = np.maximum(5, df['product_price'])

df['will_buy'] = ((df['user_spend_per_month'] > 80) * 0.3 +
                  (df['product_price'] < 70) * 0.2 +
                  (df['product_rating_avg'] > 4.0) * 0.25 +
                  (df['time_on_page_min'] > 3.0) * 0.15 +
                  (df['product_category_idx'] == 1) * 0.1).apply(lambda x: 1 if x > 0.6 else 0)

X = df.drop('will_buy', axis=1)
y = df['will_buy']
feature_names = X.columns.tolist()
categorical_features_indices = [feature_names.index('product_category_idx')]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=44)

bb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=44)
bb_model.fit(X_train, y_train)
print("Black-box model accuracy:", accuracy_score(y_test, bb_model.predict(X_test)))

surrogate_model = GaussianNB()
surrogate_model.fit(X_train, bb_model.predict(X_train))
print("\n--- Global Understanding (Gaussian Naive Bayes Surrogate) ---")
print("Surrogate model accuracy on black-box predictions:", accuracy_score(bb_model.predict(X_test), surrogate_model.predict(X_test)))

instance_idx = 10
instance_to_explain = X_test.iloc[[instance_idx]]
bb_prediction = bb_model.predict(instance_to_explain)[0]
bb_prediction_proba = bb_model.predict_proba(instance_to_explain)[0]
print(f"\n--- Local Explanation for Instance {instance_idx} (Recommendation for User {instance_to_explain.index[0]}) ---")
print(f"Black-box prediction: {'Will Buy' if bb_prediction == 1 else 'Will Not Buy'} (Proba: {bb_prediction_proba[bb_prediction]:.2f})")

explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=feature_names,
    class_names=['Will Not Buy', 'Will Buy'],
    mode='classification',
    categorical_features=categorical_features_indices
)
lime_explanation = explainer.explain_instance(
    data_row=instance_to_explain.values[0],
    predict_fn=bb_model.predict_proba,
    num_features=5
)
print("\nLIME Explanation (Feature importance for this recommendation):")
for feature, weight in lime_explanation.as_list():
    print(f"  {feature}: {weight:.4f}")

shap_explainer = shap.Explainer(bb_model, X_train)
shap_values = shap_explainer(instance_to_explain)
print("\nSHAP Explanation (Contribution of each feature):")
for i, feature in enumerate(feature_names):
    print(f"  {feature}: {shap_values.values[0][i]:.4f}")

print("\nLocal Rule-Based Explanation (Simulated):")
user_spend = instance_to_explain['user_spend_per_month'].values[0]
prod_rating = instance_to_explain['product_rating_avg'].values[0]
if user_spend > 120 and prod_rating > 4.5:
    print(f"  IF User Spend > $120/month AND Product Rating > 4.5 THEN User is highly likely to buy ({bb_prediction_proba[1]:.2f}).")
elif user_spend < 50 and prod_rating < 3.0:
    print(f"  IF User Spend < $50/month AND Product Rating < 3.0 THEN User is highly likely NOT to buy ({bb_prediction_proba[0]:.2f}).")
else:
    print(f"  No simple rule for this specific combination, but factors lead to {bb_prediction_proba[bb_prediction]:.2f} {['not buying', 'buying'][bb_prediction]}.")

print("\n--- Actionable Insights (Counterfactual Explanations) ---")
d = dice_ml.Data(
    dataframe=pd.concat([X_train, y_train], axis=1),
    continuous_features=[f for f in feature_names if f != 'product_category_idx'],
    outcome_name='will_buy'
)
m = dice_ml.Model(model=bb_model, backend='sklearn')
exp = dice_ml.Dice(d, m, method='random')

target_class = 1 - bb_prediction
cf_explanations = exp.generate_counterfactuals(
    instance_to_explain,
    total_CFs=1,
    desired_class=target_class
)
print(f"Counterfactuals to change prediction to {'Will Buy' if target_class == 1 else 'Will Not Buy'}:")
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
subgroup_mask = (X_test['user_spend_per_month'] < 50) & (X_test['product_price'] > 80)
subgroup_X = X_test[subgroup_mask]
subgroup_y = y_test[subgroup_mask]

if not subgroup_X.empty:
    subgroup_predictions = bb_model.predict(subgroup_X)
    subgroup_accuracy = accuracy_score(subgroup_y, subgroup_predictions)
    overall_accuracy = accuracy_score(y_test, bb_model.predict(X_test))
    
    print(f"Subgroup 'Low Spend, High Price Products' ({len(subgroup_X)} instances):")
    print(f"  Subgroup Accuracy: {subgroup_accuracy:.2f}")
    print(f"  Overall Test Accuracy: {overall_accuracy:.2f}")
    if subgroup_accuracy < overall_accuracy * 0.9:
        print("  Divergence Detected: Model performs significantly worse in this subgroup (e.g., struggles with new users).")
    else:
        print("  No significant divergence detected in this subgroup.")

    misclassified_subgroup = subgroup_X[subgroup_predictions != subgroup_y]
    if not misclassified_subgroup.empty:
        print(f"  {len(misclassified_subgroup)} misclassified instances in subgroup. Example misclassification:")
        mis_instance = misclassified_subgroup.iloc[[0]]
        mis_pred = bb_model.predict(mis_instance)[0]
        true_label = subgroup_y.loc[mis_instance.index[0]]
        print(f"    Features: {mis_instance.values[0]}")
        print(f"    Predicted: {'Buy' if mis_pred == 1 else 'Not Buy'}, True: {'Buy' if true_label == 1 else 'Not Buy'}")
else:
    print("No instances found for the 'Low Spend, High Price Products' subgroup in the test set.")

print("\n--- Interactive Exploration (Simulated) ---")
print("An e-commerce analyst could use an interactive tool to:")
print("1. Understand general factors that drive purchases (global surrogate model).")
print("2. Explain why a specific product was recommended or not recommended to a user (LIME/SHAP).")
print("3. Generate strategies to convert a 'will not buy' prediction to 'will buy' (counterfactuals, e.g., suggest a lower price or higher-rated alternative).")
print("4. Identify user segments where the recommendation system underperforms or exhibits unexpected patterns (subgroup analysis).")
print("5. Perform A/B tests based on insights from local rules to improve recommendation effectiveness.")
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.naive_bayes import GaussianNB
import lime
import lime.lime_tabular
import shap

np.random.seed(200)
n_recommendations = 1200
data = {
    'user_age': np.random.randint(18, 65, n_recommendations),
    'user_past_purchases': np.random.randint(0, 100, n_recommendations),
    'product_price': np.random.uniform(10, 500, n_recommendations),
    'product_rating': np.random.uniform(2.5, 5.0, n_recommendations),
    'time_on_page': np.random.uniform(10, 600, n_recommendations),
    'is_new_user': np.random.randint(0, 2, n_recommendations),
}
df = pd.DataFrame(data)

df['purchased'] = ((df['user_past_purchases'] > 20) * 0.2 +
                   (df['product_rating'] > 4.0) * 0.25 +
                   (df['time_on_page'] > 120) * 0.15 -
                   (df['product_price'] > 300) * 0.1 -
                   (df['is_new_user'] == 1) * 0.05 +
                   np.random.rand(n_recommendations) * 0.2 > 0.5).astype(int)

X = df[['user_age', 'user_past_purchases', 'product_price', 'product_rating', 'time_on_page', 'is_new_user']]
y = df['purchased']
feature_names = X.columns.tolist()
class_names = ['Not Purchased', 'Purchased']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=200)

black_box_model_ecommerce = xgb.XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss', random_state=200)
black_box_model_ecommerce.fit(X_train, y_train)

class EcommerceExplainabilityFramework:
    def __init__(self, model, X_train, feature_names, class_names):
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names
        self.class_names = class_names

    def get_global_surrogate(self):
        surrogate_model = GaussianNB()
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
            if "price" in feature and weight < 0:
                rules.append(f"IF {feature} ({feat_val:.2f}) is a deterrent (negative influence)")
            elif "rating" in feature and weight > 0:
                rules.append(f"IF {feature} ({feat_val:.2f}) is high (positive influence)")
            elif "purchases" in feature and weight > 0:
                rules.append(f"IF {feature} ({feat_val:.0f}) indicates loyalty (positive influence)")
            elif "new_user" in feature and feat_val == 1 and weight < 0:
                rules.append(f"IF user is new (negative influence)")
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
                if feature == 'is_new_user':
                    if desired_prediction_class_idx == 1 and contributions[i] > 0 and counterfactual_instance[feature] == 0:
                        counterfactual_instance[feature] = 1
                    elif desired_prediction_class_idx == 1 and contributions[i] < 0 and counterfactual_instance[feature] == 1:
                        counterfactual_instance[feature] = 0
                    elif desired_prediction_class_idx == 0 and contributions[i] > 0 and counterfactual_instance[feature] == 1:
                        counterfactual_instance[feature] = 0
                    elif desired_prediction_class_idx == 0 and contributions[i] < 0 and counterfactual_instance[feature] == 0:
                        counterfactual_instance[feature] = 1
                    continue

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

        low_purchases_mask = X_data['user_past_purchases'] < 10
        if low_purchases_mask.any():
            low_purchases_subgroup_X = X_data[low_purchases_mask]
            low_purchases_subgroup_y_true = y_true[low_purchases_mask]
            low_purchases_subgroup_preds = predictions[low_purchases_mask]
            low_purchases_accuracy = np.mean(low_purchases_subgroup_preds == low_purchases_subgroup_y_true)
            subgroup_reports.append({
                "name": "Low Past Purchases Users (<10)",
                "size": len(low_purchases_subgroup_X),
                "overall_accuracy": f"{overall_accuracy:.2f}",
                "subgroup_accuracy": f"{low_purchases_accuracy:.2f}",
                "divergence": f"{low_purchases_accuracy - overall_accuracy:.2f}"
            })

        high_price_mask = X_data['product_price'] > 250
        if high_price_mask.any():
            high_price_subgroup_X = X_data[high_price_mask]
            high_price_subgroup_y_true = y_true[high_price_mask]
            high_price_subgroup_preds = predictions[high_price_mask]
            high_price_accuracy = np.mean(high_price_subgroup_preds == high_price_subgroup_y_true)
            subgroup_reports.append({
                "name": "High-Priced Products (>250)",
                "size": len(high_price_subgroup_X),
                "overall_accuracy": f"{overall_accuracy:.2f}",
                "subgroup_accuracy": f"{high_price_accuracy:.2f}",
                "divergence": f"{high_price_accuracy - overall_accuracy:.2f}"
            })

        return subgroup_reports

    def interactive_explore(self, instance_to_explain):
        print(f"\n--- Explaining Recommendation Instance: ---")
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

        print("\n--- Counterfactual Explanation (What if we wanted a purchase?) ---")
        cf_result = self.get_counterfactual(instance_to_explain, desired_prediction_class_idx=1)
        if isinstance(cf_result, tuple):
            counterfactual_instance, original_pred, desired_pred = cf_result
            print(f"Original Prediction: {self.class_names[original_pred]}")
            print(f"Desired Prediction: {self.class_names[desired_pred]}")
            print("Minimal changes to achieve desired outcome (Purchase):")
            changes = counterfactual_instance - instance_to_explain
            for feature, change in changes.items():
                if abs(change) > 0.01:
                    print(f"  {feature}: Change by {change:.2f} (from {instance_to_explain[feature]:.2f} to {counterfactual_instance[feature]:.2f})")
            print(f"New instance for desired outcome:\n{counterfactual_instance}")
        else:
            print(cf_result)

framework_ecommerce = EcommerceExplainabilityFramework(black_box_model_ecommerce, X_train, feature_names, class_names)

print("--- Global Understanding: Surrogate Model ---")
global_surrogate_ecommerce = framework_ecommerce.get_global_surrogate()
print(f"Global Surrogate Model (Gaussian Naive Bayes) trained.")

print("\n--- Subgroup Divergence Analysis ---")
subgroup_reports_ecommerce = framework_ecommerce.perform_subgroup_analysis(X_test, y_test)
for report in subgroup_reports_ecommerce:
    print(f"Subgroup: {report['name']} (Size: {report['size']})")
    print(f"  Overall Model Accuracy: {report['overall_accuracy']}")
    print(f"  Subgroup Accuracy: {report['subgroup_accuracy']}")
    print(f"  Divergence (Subgroup - Overall): {report['divergence']}")
    if float(report['divergence']) < -0.1 or float(report['divergence']) > 0.1:
        print("  -> Significant divergence detected, investigate recommendation effectiveness for this group.")
    print("-" * 30)

instance_to_explain_idx_ec = 15
instance_to_explain_ec = X_test.iloc[instance_to_explain_idx_ec]
framework_ecommerce.interactive_explore(instance_to_explain_ec)

not_purchased_idx = y_test[black_box_model_ecommerce.predict(X_test) == 0].index
if not not_purchased_idx.empty:
    instance_to_explain_not_purchased = X_test.loc[not_purchased_idx[0]]
    framework_ecommerce.interactive_explore(instance_to_explain_not_purchased)

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

class BlackBoxRecommendationModel:
    def __init__(self):
        self.model = None
        self.features = ['UserAge', 'UserPurchaseHistoryCount', 'ProductCategoryPreference', 'ProductPrice', 'ProductRating', 'LastViewedCategoryMatch']

    def train(self, X, y):
        self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)

    def predict_proba(self, X):
        return self.model.predict_proba(X)[:, 1]

    def predict(self, X):
        return self.model.predict(X)

class EcommerceExplainabilityFramework:
    def __init__(self, black_box_model, feature_names, X_train_data):
        self.black_box = black_box_model
        self.feature_names = feature_names
        self.X_train_data = X_train_data

    def global_surrogate_model(self, X_train, y_train_pred):
        surrogate = KNeighborsClassifier(n_neighbors=5)
        surrogate.fit(X_train, y_train_pred)
        print("--- Global Understanding: K-Nearest Neighbors Surrogate Model ---")
        print(f"Global surrogate model trained. Number of neighbors: {surrogate.n_neighbors}")
        return surrogate

    def local_lime_explanation(self, instance, num_perturbations=1000):
        perturbed_data = np.random.normal(instance, 0.05 * np.std(self.X_train_data.values, axis=0), (num_perturbations, len(instance)))
        perturbed_preds = self.black_box.predict_proba(perturbed_data)
        
        local_model = LinearRegression()
        local_model.fit(perturbed_data, perturbed_preds)
        
        feature_importances = dict(zip(self.feature_names, local_model.coef_))
        print(f"\n--- Local Explanation (LIME-like) for user-product: {instance} ---")
        print("Feature importances (LIME-like):", {k: f"{v:.4f}" for k, v in feature_importances.items()})
        return feature_importances

    def local_shap_explanation(self, instance):
        baseline_pred = self.black_box.predict_proba(self.X_train_data.mean().values.reshape(1, -1))[0]
        instance_pred = self.black_box.predict_proba(instance.reshape(1, -1))[0]
        
        shap_values = {}
        for i, feature in enumerate(self.feature_names):
            temp_instance = instance.copy()
            temp_instance[i] = self.X_train_data.mean()[i]
            pred_without_feature = self.black_box.predict_proba(temp_instance.reshape(1, -1))[0]
            shap_values[feature] = instance_pred - pred_without_feature
            
        print(f"\n--- Local Explanation (SHAP-like) for user-product: {instance} ---")
        print("Feature contributions (SHAP-like):", {k: f"{v:.4f}" for k, v in shap_values.items()})
        return shap_values

    def local_rule_explanation(self, instance):
        pred = self.black_box.predict(instance.reshape(1, -1))[0]
        rules = []
        if pred == 1:
            if instance[self.feature_names.index('ProductRating')] > 4.0 and \
               instance[self.feature_names.index('ProductCategoryPreference')] == 1:
                rules.append("High Product Rating and matching Category Preference lead to Recommendation.")
            elif instance[self.feature_names.index('UserPurchaseHistoryCount')] > 10 and \
                 instance[self.feature_names.index('LastViewedCategoryMatch')] == 1:
                rules.append("Frequent Buyer with recent matching view often gets Recommendation.")
        else:
            if instance[self.feature_names.index('ProductPrice')] > 1000 and \
               instance[self.feature_names.index('UserPurchaseHistoryCount')] < 5:
                rules.append("High-priced product for a new user often leads to No Recommendation.")
        
        print(f"\n--- Local Rule-Based Explanation for user-product: {instance} (Prediction: {'Recommended' if pred==1 else 'Not Recommended'}) ---")
        if rules:
            for rule in rules: print(f"- {rule}")
        else:
            print("- No specific simple rules found for this instance's prediction.")
        return rules

    def counterfactual_explanation(self, instance, desired_prediction=1):
        original_pred = self.black_box.predict(instance.reshape(1, -1))[0]
        if original_pred == desired_prediction:
            print(f"\n--- Counterfactual Explanation for user-product: {instance} ---")
            print(f"Original prediction is already {desired_prediction}. No counterfactual needed.")
            return None

        cf_instance = instance.copy()
        changes = {}
        
        idx_cat_pref = self.feature_names.index('ProductCategoryPreference')
        if original_pred == 0 and instance[idx_cat_pref] == 0:
            cf_instance[idx_cat_pref] = 1
            changes['ProductCategoryPreference'] = "Change from Not Preferred to Preferred"
            if self.black_box.predict(cf_instance.reshape(1, -1))[0] == desired_prediction:
                print(f"\n--- Counterfactual Explanation for user-product: {instance} (Desired: {desired_prediction}) ---")
                print(f"To change prediction to {desired_prediction}, consider: {changes}")
                return cf_instance, changes
            cf_instance = instance.copy()

        idx_last_view = self.feature_names.index('LastViewedCategoryMatch')
        if original_pred == 0 and instance[idx_last_view] == 0:
            cf_instance[idx_last_view] = 1
            changes['LastViewedCategoryMatch'] = "Change from No Match to Match"
            if self.black_box.predict(cf_instance.reshape(1, -1))[0] == desired_prediction:
                print(f"\n--- Counterfactual Explanation for user-product: {instance} (Desired: {desired_prediction}) ---")
                print(f"To change prediction to {desired_prediction}, consider: {changes}")
                return cf_instance, changes
            cf_instance = instance.copy()
            
        print(f"\n--- Counterfactual Explanation for user-product: {instance} (Desired: {desired_prediction}) ---")
        print("Could not find a simple counterfactual explanation.")
        return None

    def subgroup_divergence_analysis(self, X_data, y_true, y_pred):
        print("\n--- Subgroup Divergence Analysis ---")
        df = pd.DataFrame(X_data, columns=self.feature_names)
        df['y_true'] = y_true
        df['y_pred'] = y_pred

        age_bins = [18, 25, 35, 50, 90]
        age_labels = ['18-24', '25-34', '35-49', '50+']
        df['UserAgeGroup'] = pd.cut(df['UserAge'], bins=age_bins, labels=age_labels, right=False)

        print("Analyzing performance across User Age Groups:")
        for group in age_labels:
            subgroup = df[df['UserAgeGroup'] == group]
            if not subgroup.empty:
                acc = accuracy_score(subgroup['y_true'], subgroup['y_pred'])
                mean_pred_prob = self.black_box.predict_proba(subgroup[self.feature_names])[:, 1].mean()
                print(f"  Age Group '{group}': Accuracy={acc:.4f}, Avg Pred Rec Score={mean_pred_prob:.4f}, Count={len(subgroup)}")

        new_users_subgroup = df[df['UserPurchaseHistoryCount'] < 5]
        if not new_users_subgroup.empty:
            nu_acc = accuracy_score(new_users_subgroup['y_true'], new_users_subgroup['y_pred'])
            print(f"\n  Subgroup 'New Users (Purchase Count < 5)': Accuracy={nu_acc:.4f}, Count={len(new_users_subgroup)}")

    def interactive_exploration_simulation(self, X_data, instance_to_explain):
        print("\n--- Interactive Exploration (Simulated) ---")
        print("Welcome to the E-commerce Recommendation XAI Dashboard!")
        print("\n1. Global Model Overview:")
        print("   - Displaying overall recommendation patterns from Global Surrogate Model.")
        
        print("\n2. Individual Recommendation Analysis:")
        print(f"   - Selected user-product interaction: {instance_to_explain}")
        self.local_lime_explanation(instance_to_explain)
        self.local_shap_explanation(instance_to_explain)
        self.local_rule_explanation(instance_to_explain)
        
        print("\n3. 'How to get this recommendation?' (What-If):")
        self.counterfactual_explanation(instance_to_explain, desired_prediction=1)
        
        print("\n4. User Segment Performance Drilldown:")
        print("   - Visualizing recommendation accuracy and patterns across different user demographics and product types.")
        print("   - Highlighting user segments where recommendations are less effective or potentially biased.")

        print("\n5. Product Manager Insights:")
        print("   - 'Why is this product not being recommended to frequent buyers?'")
        print("This simulates a UI where product managers can interact with explanations.")

if __name__ == "__main__":
    print("Real-world usage: An e-commerce platform uses an AI model to recommend products to users.")
    print("The framework helps product managers understand why certain products are recommended, debug recommendation biases, and improve user experience.")

    np.random.seed(42)
    num_samples = 1000
    
    data = {
        'UserAge': np.random.randint(18, 70, num_samples),
        'UserPurchaseHistoryCount': np.random.randint(0, 50, num_samples),
        'ProductCategoryPreference': np.random.randint(0, 2, num_samples),
        'ProductPrice': np.random.uniform(10, 1000, num_samples),
        'ProductRating': np.random.uniform(2.5, 5.0, num_samples),
        'LastViewedCategoryMatch': np.random.randint(0, 2, num_samples)
    }
    df = pd.DataFrame(data)

    df['RecommendationScore'] = ((df['ProductCategoryPreference'] == 1) * 0.3 +
                                 (df['ProductRating'] > 4.0) * 0.25 +
                                 (df['LastViewedCategoryMatch'] == 1) * 0.2 +
                                 (df['UserPurchaseHistoryCount'] > 10) * 0.15 -
                                 (df['ProductPrice'] > 500) * 0.1 +
                                 np.random.rand(num_samples) * 0.15 > 0.5).astype(int)

    X = df[['UserAge', 'UserPurchaseHistoryCount', 'ProductCategoryPreference', 'ProductPrice', 'ProductRating', 'LastViewedCategoryMatch']]
    y = df['RecommendationScore']
    feature_names = X.columns.tolist()

    X_train_df, X_test_df, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    bb_model = BlackBoxRecommendationModel()
    bb_model.train(X_train_df, y_train)
    y_pred_bb = bb_model.predict(X_test_df)
    print(f"\nBlack-Box Model Accuracy: {accuracy_score(y_test, y_pred_bb):.4f}")

    explainer = EcommerceExplainabilityFramework(bb_model, feature_names, X_train_df)

    y_train_pred_bb_proba = bb_model.predict_proba(X_train_df)[:, 1]
    y_train_pred_bb = (y_train_pred_bb_proba > 0.5).astype(int)
    global_surrogate = explainer.global_surrogate_model(X_train_df, y_train_pred_bb)

    instance_idx = X_test_df[(y_test == 0) & (y_pred_bb == 0)].sample(1).index[0]
    instance_to_explain = X_test_df.loc[instance_idx].values
    
    explainer.local_lime_explanation(instance_to_explain)
    explainer.local_shap_explanation(instance_to_explain)
    explainer.local_rule_explanation(instance_to_explain)

    explainer.counterfactual_explanation(instance_to_explain, desired_prediction=1)

    explainer.subgroup_divergence_analysis(X_test_df, y_test, y_pred_bb)

    explainer.interactive_exploration_simulation(X_test_df, instance_to_explain)
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
import pandas as pd

class BlackBoxLoanModel:
    def __init__(self):
        self.model = None
        self.features = ['CreditScore', 'Income', 'LoanAmount', 'Age', 'EmploymentYears']

    def train(self, X, y):
        self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)

    def predict_proba(self, X):
        return self.model.predict_proba(X)[:, 1]

    def predict(self, X):
        return self.model.predict(X)

class ExplainabilityFramework:
    def __init__(self, black_box_model, feature_names, X_train_data):
        self.black_box = black_box_model
        self.feature_names = feature_names
        self.X_train_data = X_train_data

    def global_surrogate_model(self, X_train, y_train_pred):
        surrogate = DecisionTreeClassifier(max_depth=5, random_state=42)
        surrogate.fit(X_train, y_train_pred)
        print("\n--- Global Understanding: Decision Tree Surrogate Model ---")
        print(f"Global surrogate model trained. Max depth: {surrogate.max_depth}, Nodes: {surrogate.tree_.node_count}")
        return surrogate

    def local_lime_explanation(self, instance, num_perturbations=1000):
        perturbed_data = np.random.normal(instance, 0.1 * np.std(self.X_train_data.values, axis=0), (num_perturbations, len(instance)))
        perturbed_preds = self.black_box.predict_proba(perturbed_data)
        
        local_model = LinearRegression()
        local_model.fit(perturbed_data, perturbed_preds)
        
        feature_importances = dict(zip(self.feature_names, local_model.coef_))
        print(f"\n--- Local Explanation (LIME-like) for instance: {instance} ---")
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
            
        print(f"\n--- Local Explanation (SHAP-like) for instance: {instance} ---")
        print("Feature contributions (SHAP-like):", {k: f"{v:.4f}" for k, v in shap_values.items()})
        return shap_values

    def local_rule_explanation(self, instance):
        pred = self.black_box.predict(instance.reshape(1, -1))[0]
        rules = []
        if pred == 1:
            if instance[self.feature_names.index('CreditScore')] > 700 and \
               instance[self.feature_names.index('Income')] > 60000:
                rules.append("High CreditScore and High Income often lead to Approval.")
            elif instance[self.feature_names.index('EmploymentYears')] > 5 and \
                 instance[self.feature_names.index('LoanAmount')] < 50000:
                rules.append("Long Employment and Moderate LoanAmount often lead to Approval.")
        else:
            if instance[self.feature_names.index('CreditScore')] < 600:
                rules.append("Low CreditScore is a strong indicator for Denial.")
            if instance[self.feature_names.index('LoanAmount')] > instance[self.feature_names.index('Income')] * 0.8:
                rules.append("Very High LoanAmount relative to Income often leads to Denial.")
        
        print(f"\n--- Local Rule-Based Explanation for instance: {instance} (Prediction: {'Approved' if pred==1 else 'Denied'}) ---")
        if rules:
            for rule in rules: print(f"- {rule}")
        else:
            print("- No specific simple rules found for this instance's prediction.")
        return rules

    def counterfactual_explanation(self, instance, desired_prediction=1):
        original_pred = self.black_box.predict(instance.reshape(1, -1))[0]
        if original_pred == desired_prediction:
            print(f"\n--- Counterfactual Explanation for instance: {instance} ---")
            print(f"Original prediction is already {desired_prediction}. No counterfactual needed.")
            return None

        cf_instance = instance.copy()
        changes = {}
        
        idx_cs = self.feature_names.index('CreditScore')
        if original_pred == 0 and cf_instance[idx_cs] < 700:
            cf_instance[idx_cs] = 720
            changes['CreditScore'] = f"Increase from {instance[idx_cs]:.0f} to {cf_instance[idx_cs]:.0f}"
            if self.black_box.predict(cf_instance.reshape(1, -1))[0] == desired_prediction:
                print(f"\n--- Counterfactual Explanation for instance: {instance} (Desired: {desired_prediction}) ---")
                print(f"To change prediction to {desired_prediction}, consider: {changes}")
                return cf_instance, changes
            cf_instance = instance.copy()

        idx_inc = self.feature_names.index('Income')
        if original_pred == 0 and cf_instance[idx_inc] < 50000:
            cf_instance[idx_inc] = 65000
            changes['Income'] = f"Increase from {instance[idx_inc]:.0f} to {cf_instance[idx_inc]:.0f}"
            if self.black_box.predict(cf_instance.reshape(1, -1))[0] == desired_prediction:
                print(f"\n--- Counterfactual Explanation for instance: {instance} (Desired: {desired_prediction}) ---")
                print(f"To change prediction to {desired_prediction}, consider: {changes}")
                return cf_instance, changes
            cf_instance = instance.copy()

        print(f"\n--- Counterfactual Explanation for instance: {instance} (Desired: {desired_prediction}) ---")
        print("Could not find a simple counterfactual explanation.")
        return None

    def subgroup_divergence_analysis(self, X_data, y_true, y_pred):
        print("\n--- Subgroup Divergence Analysis ---")
        df = pd.DataFrame(X_data, columns=self.feature_names)
        df['y_true'] = y_true
        df['y_pred'] = y_pred

        age_bins = [18, 30, 45, 60, 100]
        age_labels = ['18-29', '30-44', '45-59', '60+']
        df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

        print("Analyzing performance across Age Groups:")
        for group in age_labels:
            subgroup = df[df['AgeGroup'] == group]
            if not subgroup.empty:
                acc = accuracy_score(subgroup['y_true'], subgroup['y_pred'])
                mean_pred_prob = self.black_box.predict_proba(subgroup[self.feature_names])[:, 1].mean()
                print(f"  Age Group '{group}': Accuracy={acc:.4f}, Avg Pred Prob={mean_pred_prob:.4f}, Count={len(subgroup)}")

        low_credit_subgroup = df[df['CreditScore'] < 650]
        if not low_credit_subgroup.empty:
            low_credit_acc = accuracy_score(low_credit_subgroup['y_true'], low_credit_subgroup['y_pred'])
            print(f"\n  Subgroup 'Low Credit Score (<650)': Accuracy={low_credit_acc:.4f}, Count={len(low_credit_subgroup)}")

    def interactive_exploration_simulation(self, X_data, instance_to_explain):
        print("\n--- Interactive Exploration (Simulated) ---")
        print("Welcome to the Loan Approval XAI Dashboard!")
        print("\n1. Global Model Overview:")
        print("   - Displaying decision rules from Global Surrogate Model.")
        
        print("\n2. Individual Prediction Analysis:")
        print(f"   - Selected applicant: {instance_to_explain}")
        self.local_lime_explanation(instance_to_explain)
        self.local_shap_explanation(instance_to_explain)
        self.local_rule_explanation(instance_to_explain)
        
        print("\n3. What-If Scenarios:")
        self.counterfactual_explanation(instance_to_explain, desired_prediction=1)
        
        print("\n4. Subgroup Performance Drilldown:")
        print("   - Visualizing model performance across different age groups, income brackets.")
        print("   - Highlighting subgroups with unusual prediction patterns or lower accuracy.")

        print("\n5. User Feedback Loop:")
        print("   - 'Was this explanation helpful? (Yes/No)'")
        print("This simulates a UI where users can interact with explanations.")


if __name__ == "__main__":
    print("Real-world usage: A bank uses an AI model to decide on loan applications.")
    print("The framework helps them understand why a loan was approved/denied, identify potential biases, and debug the model.")

    np.random.seed(42)
    num_samples = 1000
    
    data = {
        'CreditScore': np.random.randint(300, 850, num_samples),
        'Income': np.random.randint(20000, 150000, num_samples),
        'LoanAmount': np.random.randint(5000, 200000, num_samples),
        'Age': np.random.randint(18, 70, num_samples),
        'EmploymentYears': np.random.randint(0, 30, num_samples)
    }
    df = pd.DataFrame(data)

    df['Approval'] = ((df['CreditScore'] > 650) * 0.4 +
                      (df['Income'] > 50000) * 0.3 +
                      (df['EmploymentYears'] > 3) * 0.2 -
                      (df['LoanAmount'] / df['Income'] > 2) * 0.1 -
                      (df['Age'] < 25) * 0.1 +
                      np.random.rand(num_samples) * 0.2 > 0.5).astype(int)

    X = df[['CreditScore', 'Income', 'LoanAmount', 'Age', 'EmploymentYears']]
    y = df['Approval']
    feature_names = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    bb_model = BlackBoxLoanModel()
    bb_model.train(X_train, y_train)
    y_pred_bb = bb_model.predict(X_test)
    print(f"\nBlack-Box Model Accuracy: {accuracy_score(y_test, y_pred_bb):.4f}")

    explainer = ExplainabilityFramework(bb_model, feature_names, X_train)

    y_train_pred_bb_proba = bb_model.predict_proba(X_train)[:, 1]
    y_train_pred_bb = (y_train_pred_bb_proba > 0.5).astype(int)
    global_surrogate = explainer.global_surrogate_model(X_train, y_train_pred_bb)

    instance_idx = X_test[(y_test == 0) & (y_pred_bb == 0)].sample(1).index[0]
    instance_to_explain = X_test.loc[instance_idx].values
    
    explainer.local_lime_explanation(instance_to_explain)
    explainer.local_shap_explanation(instance_to_explain)
    explainer.local_rule_explanation(instance_to_explain)

    explainer.counterfactual_explanation(instance_to_explain, desired_prediction=1)

    explainer.subgroup_divergence_analysis(X_test, y_test, y_pred_bb)

    explainer.interactive_exploration_simulation(X_test, instance_to_explain)
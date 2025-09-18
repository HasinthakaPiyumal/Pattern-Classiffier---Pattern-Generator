import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

class BlackBoxDiseaseModel:
    def __init__(self):
        self.model = None
        self.features = ['Age', 'BMI', 'BloodPressure', 'GlucoseLevel', 'FamilyHistory', 'LifestyleScore']

    def train(self, X, y):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)

    def predict_proba(self, X):
        return self.model.predict_proba(X)[:, 1]

    def predict(self, X):
        return self.model.predict(X)

class HealthcareExplainabilityFramework:
    def __init__(self, black_box_model, feature_names, X_train_data):
        self.black_box = black_box_model
        self.feature_names = feature_names
        self.X_train_data = X_train_data

    def global_surrogate_model(self, X_train, y_train_pred):
        surrogate = LogisticRegression(solver='liblinear', random_state=42)
        surrogate.fit(X_train, y_train_pred)
        print("--- Global Understanding: Logistic Regression Surrogate Model ---")
        print(f"Global surrogate model trained. Coefficients: {dict(zip(self.feature_names, surrogate.coef_[0].round(3)))}")
        return surrogate

    def local_lime_explanation(self, instance, num_perturbations=1000):
        perturbed_data = np.random.normal(instance, 0.05 * np.std(self.X_train_data.values, axis=0), (num_perturbations, len(instance)))
        perturbed_preds = self.black_box.predict_proba(perturbed_data)
        
        local_model = LinearRegression()
        local_model.fit(perturbed_data, perturbed_preds)
        
        feature_importances = dict(zip(self.feature_names, local_model.coef_))
        print(f"\n--- Local Explanation (LIME-like) for patient: {instance} ---")
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
            
        print(f"\n--- Local Explanation (SHAP-like) for patient: {instance} ---")
        print("Feature contributions (SHAP-like):", {k: f"{v:.4f}" for k, v in shap_values.items()})
        return shap_values

    def local_rule_explanation(self, instance):
        pred = self.black_box.predict(instance.reshape(1, -1))[0]
        rules = []
        if pred == 1:
            if instance[self.feature_names.index('GlucoseLevel')] > 140 and \
               instance[self.feature_names.index('BMI')] > 30:
                rules.append("High Glucose and High BMI are strong indicators for High Risk.")
            elif instance[self.feature_names.index('Age')] > 50 and \
                 instance[self.feature_names.index('FamilyHistory')] == 1:
                rules.append("Older age with Family History often leads to High Risk.")
        else:
            if instance[self.feature_names.index('GlucoseLevel')] < 100 and \
               instance[self.feature_names.index('BMI')] < 25:
                rules.append("Normal Glucose and BMI are good indicators for Low Risk.")
        
        print(f"\n--- Local Rule-Based Explanation for patient: {instance} (Prediction: {'High Risk' if pred==1 else 'Low Risk'}) ---")
        if rules:
            for rule in rules: print(f"- {rule}")
        else:
            print("- No specific simple rules found for this patient's prediction.")
        return rules

    def counterfactual_explanation(self, instance, desired_prediction=0):
        original_pred = self.black_box.predict(instance.reshape(1, -1))[0]
        if original_pred == desired_prediction:
            print(f"\n--- Counterfactual Explanation for patient: {instance} ---")
            print(f"Original prediction is already {desired_prediction}. No counterfactual needed.")
            return None

        cf_instance = instance.copy()
        changes = {}
        
        idx_bmi = self.feature_names.index('BMI')
        if original_pred == 1 and cf_instance[idx_bmi] > 25:
            cf_instance[idx_bmi] = 24.0
            changes['BMI'] = f"Decrease from {instance[idx_bmi]:.1f} to {cf_instance[idx_bmi]:.1f}"
            if self.black_box.predict(cf_instance.reshape(1, -1))[0] == desired_prediction:
                print(f"\n--- Counterfactual Explanation for patient: {instance} (Desired: {desired_prediction}) ---")
                print(f"To change prediction to {desired_prediction}, consider: {changes}")
                return cf_instance, changes
            cf_instance = instance.copy()

        idx_glucose = self.feature_names.index('GlucoseLevel')
        if original_pred == 1 and cf_instance[idx_glucose] > 120:
            cf_instance[idx_glucose] = 95.0
            changes['GlucoseLevel'] = f"Decrease from {instance[idx_glucose]:.1f} to {cf_instance[idx_glucose]:.1f}"
            if self.black_box.predict(cf_instance.reshape(1, -1))[0] == desired_prediction:
                print(f"\n--- Counterfactual Explanation for patient: {instance} (Desired: {desired_prediction}) ---")
                print(f"To change prediction to {desired_prediction}, consider: {changes}")
                return cf_instance, changes
            cf_instance = instance.copy()

        print(f"\n--- Counterfactual Explanation for patient: {instance} (Desired: {desired_prediction}) ---")
        print("Could not find a simple counterfactual explanation.")
        return None

    def subgroup_divergence_analysis(self, X_data, y_true, y_pred):
        print("\n--- Subgroup Divergence Analysis ---")
        df = pd.DataFrame(X_data, columns=self.feature_names)
        df['y_true'] = y_true
        df['y_pred'] = y_pred

        age_bins = [20, 40, 60, 90]
        age_labels = ['20-39', '40-59', '60+']
        df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

        print("Analyzing performance across Age Groups:")
        for group in age_labels:
            subgroup = df[df['AgeGroup'] == group]
            if not subgroup.empty:
                acc = accuracy_score(subgroup['y_true'], subgroup['y_pred'])
                mean_pred_prob = self.black_box.predict_proba(subgroup[self.feature_names])[:, 1].mean()
                print(f"  Age Group '{group}': Accuracy={acc:.4f}, Avg Pred Risk={mean_pred_prob:.4f}, Count={len(subgroup)}")

        family_history_subgroup = df[df['FamilyHistory'] == 1]
        if not family_history_subgroup.empty:
            fh_acc = accuracy_score(family_history_subgroup['y_true'], family_history_subgroup['y_pred'])
            print(f"\n  Subgroup 'Family History Present': Accuracy={fh_acc:.4f}, Count={len(family_history_subgroup)}")

    def interactive_exploration_simulation(self, X_data, instance_to_explain):
        print("\n--- Interactive Exploration (Simulated) ---")
        print("Welcome to the Disease Risk XAI Dashboard!")
        print("\n1. Global Model Overview:")
        print("   - Displaying feature weights from Global Surrogate Model.")
        
        print("\n2. Individual Patient Risk Analysis:")
        print(f"   - Selected patient data: {instance_to_explain}")
        self.local_lime_explanation(instance_to_explain)
        self.local_shap_explanation(instance_to_explain)
        self.local_rule_explanation(instance_to_explain)
        
        print("\n3. Lifestyle Recommendations (What-If):")
        self.counterfactual_explanation(instance_to_explain, desired_prediction=0)
        
        print("\n4. Population Health Insights:")
        print("   - Visualizing model performance across different patient demographics and risk factors.")
        print("   - Highlighting patient subgroups where the model might be less accurate or biased.")

        print("\n5. Physician Feedback:")
        print("   - 'Do these explanations align with your clinical judgment?'")
        print("This simulates a UI where healthcare professionals can interact with explanations.")

if __name__ == "__main__":
    print("Real-world usage: A hospital uses an AI model to predict disease risk for patients.")
    print("The framework helps doctors understand individual patient risks, provide actionable advice, and assess model fairness across patient groups.")

    np.random.seed(42)
    num_samples = 1000
    
    data = {
        'Age': np.random.randint(20, 80, num_samples),
        'BMI': np.random.uniform(18, 40, num_samples),
        'BloodPressure': np.random.randint(90, 180, num_samples),
        'GlucoseLevel': np.random.randint(70, 200, num_samples),
        'FamilyHistory': np.random.randint(0, 2, num_samples),
        'LifestyleScore': np.random.uniform(1, 10, num_samples)
    }
    df = pd.DataFrame(data)

    df['DiseaseRisk'] = ((df['BMI'] > 28) * 0.2 +
                         (df['GlucoseLevel'] > 120) * 0.3 +
                         (df['BloodPressure'] > 140) * 0.15 +
                         (df['Age'] > 55) * 0.1 +
                         (df['FamilyHistory'] == 1) * 0.15 -
                         (df['LifestyleScore'] > 7) * 0.2 +
                         np.random.rand(num_samples) * 0.1 > 0.5).astype(int)

    X = df[['Age', 'BMI', 'BloodPressure', 'GlucoseLevel', 'FamilyHistory', 'LifestyleScore']]
    y = df['DiseaseRisk']
    feature_names = X.columns.tolist()

    X_train_df, X_test_df, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    bb_model = BlackBoxDiseaseModel()
    bb_model.train(X_train_df, y_train)
    y_pred_bb = bb_model.predict(X_test_df)
    print(f"\nBlack-Box Model Accuracy: {accuracy_score(y_test, y_pred_bb):.4f}")

    explainer = HealthcareExplainabilityFramework(bb_model, feature_names, X_train_df)

    y_train_pred_bb_proba = bb_model.predict_proba(X_train_df)[:, 1]
    y_train_pred_bb = (y_train_pred_bb_proba > 0.5).astype(int)
    global_surrogate = explainer.global_surrogate_model(X_train_df, y_train_pred_bb)

    instance_idx = X_test_df[(y_test == 1) & (y_pred_bb == 1)].sample(1).index[0]
    instance_to_explain = X_test_df.loc[instance_idx].values
    
    explainer.local_lime_explanation(instance_to_explain)
    explainer.local_shap_explanation(instance_to_explain)
    explainer.local_rule_explanation(instance_to_explain)

    explainer.counterfactual_explanation(instance_to_explain, desired_prediction=0)

    explainer.subgroup_divergence_analysis(X_test_df, y_test, y_pred_bb)

    explainer.interactive_exploration_simulation(X_test_df, instance_to_explain)
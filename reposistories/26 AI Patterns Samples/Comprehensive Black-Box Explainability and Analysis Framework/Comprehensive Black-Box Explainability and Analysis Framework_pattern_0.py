import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import lime
import lime.lime_tabular
import shap

def simulate_healthcare_data(n_samples=1000):
    np.random.seed(42)
    data = {
        'Age': np.random.randint(20, 90, n_samples),
        'Gender': np.random.choice(['Male', 'Female'], n_samples),
        'ChronicDiseaseCount': np.random.randint(0, 5, n_samples),
        'MedicationAdherence': np.random.rand(n_samples), 
        'LabResult_A': np.random.normal(100, 15, n_samples),
        'LabResult_B': np.random.normal(50, 10, n_samples),
        'PreviousReadmissions': np.random.randint(0, 3, n_samples),
        'InsuranceType': np.random.choice(['Private', 'Public', 'None'], n_samples)
    }
    df = pd.DataFrame(data)

    df['ReadmissionRisk'] = 0
    df.loc[(df['Age'] > 65) & (df['ChronicDiseaseCount'] >= 2) & (df['MedicationAdherence'] < 0.5), 'ReadmissionRisk'] = 1
    df.loc[(df['PreviousReadmissions'] >= 1) & (df['LabResult_A'] > 120), 'ReadmissionRisk'] = 1
    df.loc[(df['Age'] > 75) & (df['InsuranceType'] == 'None'), 'ReadmissionRisk'] = 1
    df.loc[(df['ReadmissionRisk'] == 0) & (np.random.rand(n_samples) < 0.1), 'ReadmissionRisk'] = 1 
    df.loc[(df['ReadmissionRisk'] == 1) & (np.random.rand(n_samples) < 0.2), 'ReadmissionRisk'] = 0 

    df = pd.get_dummies(df, columns=['Gender', 'InsuranceType'], drop_first=True)
    return df.drop('ReadmissionRisk', axis=1), df['ReadmissionRisk']

X, y = simulate_healthcare_data()
feature_names = X.columns.tolist()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

black_box_model = RandomForestClassifier(n_estimators=100, random_state=42)
black_box_model.fit(X_train, y_train)
print(f"Black-box model accuracy: {accuracy_score(y_test, black_box_model.predict(X_test)):.2f}")

class HealthcareXAI:
    def __init__(self, black_box_model, X_train, feature_names):
        self.black_box_model = black_box_model
        self.X_train = X_train
        self.feature_names = feature_names
        self.class_names = ['No Readmission', 'Readmission Risk']

        self.X_train_np = X_train.values
        self.explainer_lime = lime.lime_tabular.LimeTabularExplainer(
            training_data=self.X_train_np,
            feature_names=self.feature_names,
            class_names=self.class_names,
            mode='classification'
        )
        self.explainer_shap = shap.TreeExplainer(black_box_model)
        self.shap_values_train = self.explainer_shap.shap_values(X_train)

    def global_surrogate_model(self):
        print("\n--- 1. Global Understanding: Interpretable Global Surrogate Model ---")
        surrogate_model = DecisionTreeClassifier(max_depth=5, random_state=42)
        surrogate_model.fit(self.X_train, self.black_box_model.predict(self.X_train))
        print("Trained a Decision Tree surrogate model.")
        print(f"Surrogate model accuracy on black-box predictions: {accuracy_score(self.black_box_model.predict(self.X_train), surrogate_model.predict(self.X_train)):.2f}")
        print("This surrogate can be inspected for global decision logic (e.g., via tree visualization).")
        return surrogate_model

    def explain_local_prediction(self, instance_idx, X_data):
        print(f"\n--- 2. Local Prediction Explanation for instance {instance_idx} ---")
        instance = X_data.iloc[instance_idx].values
        original_prediction = self.black_box_model.predict([instance])[0]
        print(f"Original prediction: {self.class_names[original_prediction]}")

        print("\n  -- LIME-like Explanation --")
        exp = self.explainer_lime.explain_instance(
            data_row=instance,
            predict_fn=self.black_box_model.predict_proba,
            num_features=5
        )
        print("Top 5 features contributing to the prediction:")
        for feature, weight in exp.as_list():
            print(f"    - {feature}: {weight:.4f}")

        print("\n  -- SHAP-like Explanation --")
        shap_values_for_class = self.explainer_shap(pd.DataFrame([instance], columns=self.feature_names))[original_prediction]
        print("SHAP values for features (impact on prediction):")
        shap_df = pd.DataFrame({
            'Feature': self.feature_names,
            'SHAP Value': shap_values_for_class.values
        }).sort_values(by='SHAP Value', ascending=False)
        print(shap_df.head())

        print("\n  -- Local Rule-Based Explanation (Simulated) --")
        significant_features = [f for f, w in exp.as_list() if abs(w) > 0.1]
        if significant_features:
            print(f"Local rule for {self.class_names[original_prediction]} for this patient:")
            rule_parts = []
            for feat_str in significant_features:
                if '<=' in feat_str:
                    feature, value = feat_str.split(' <= ')
                    rule_parts.append(f"{feature} <= {float(value):.2f}")
                elif '>' in feat_str:
                    feature, value = feat_str.split(' > ')
                    rule_parts.append(f"{feature} > {float(value):.2f}")
                elif '=' in feat_str:
                    feature, value = feat_str.split(' = ')
                    rule_parts.append(f"{feature} is {('True' if float(value) > 0.5 else 'False')}")
                else:
                    feature_name = feat_str.split(' ')[0]
                    feature_value = instance[self.feature_names.index(feature_name)]
                    rule_parts.append(f"{feature_name} is approximately {feature_value:.2f}")

            print("IF " + " AND ".join(rule_parts) + f" THEN prediction is {self.class_names[original_prediction]}")
        else:
            print("No strong local rules found based on LIME features.")

    def generate_counterfactual(self, instance_idx, X_data, desired_prediction=0):
        print(f"\n--- 3. Actionable Insights: Counterfactual Explanation for instance {instance_idx} ---")
        original_instance = X_data.iloc[instance_idx].copy()
        original_prediction = self.black_box_model.predict(pd.DataFrame([original_instance]))[0]
        print(f"Original prediction: {self.class_names[original_prediction]}")
        if original_prediction == desired_prediction:
            print(f"Instance already predicts {self.class_names[desired_prediction]}. No counterfactual needed.")
            return

        print(f"Attempting to find minimal changes to change prediction to {self.class_names[desired_prediction]}...")
        counterfactual_instance = original_instance.copy()
        epsilon = 0.05 
        max_iterations = 100
        found_cf = False

        for _ in range(max_iterations):
            current_prediction = self.black_box_model.predict(pd.DataFrame([counterfactual_instance]))[0]
            if current_prediction == desired_prediction:
                found_cf = True
                break

            best_feature_change = None
            min_change_cost = np.inf

            for i, feature in enumerate(self.feature_names):
                temp_instance_up = counterfactual_instance.copy()
                temp_instance_down = counterfactual_instance.copy()

                if X_data[feature].dtype in ['int64', 'float64']:
                    temp_instance_up[feature] += epsilon * (X_data[feature].max() - X_data[feature].min())
                    pred_up = self.black_box_model.predict(pd.DataFrame([temp_instance_up]))[0]
                    if pred_up == desired_prediction:
                        change_cost = np.sum(np.abs(temp_instance_up.values - original_instance.values))
                        if change_cost < min_change_cost:
                            min_change_cost = change_cost
                            best_feature_change = (feature, temp_instance_up[feature], 'up')

                    temp_instance_down[feature] -= epsilon * (X_data[feature].max() - X_data[feature].min())
                    pred_down = self.black_box_model.predict(pd.DataFrame([temp_instance_down]))[0]
                    if pred_down == desired_prediction:
                        change_cost = np.sum(np.abs(temp_instance_down.values - original_instance.values))
                        if change_cost < min_change_cost:
                            min_change_cost = change_cost
                            best_feature_change = (feature, temp_instance_down[feature], 'down')
                elif X_data[feature].dtype == 'uint8' and X_data[feature].nunique() == 2:
                    temp_instance_flip = counterfactual_instance.copy()
                    temp_instance_flip[feature] = 1 - temp_instance_flip[feature]
                    pred_flip = self.black_box_model.predict(pd.DataFrame([temp_instance_flip]))[0]
                    if pred_flip == desired_prediction:
                        change_cost = np.sum(np.abs(temp_instance_flip.values - original_instance.values))
                        if change_cost < min_change_cost:
                            min_change_cost = change_cost
                            best_feature_change = (feature, temp_instance_flip[feature], 'flip')

            if best_feature_change:
                feature_to_change, new_value, _ = best_feature_change
                counterfactual_instance[feature_to_change] = new_value
            else:
                break 

        if found_cf:
            print("\nCounterfactual found:")
            print("Original Patient Profile:")
            print(original_instance.to_dict())
            print("\nSuggested Changes for No Readmission Risk:")
            changes = {}
            for feature in self.feature_names:
                if original_instance[feature] != counterfactual_instance[feature]:
                    changes[feature] = counterfactual_instance[feature]
            print(changes)
            print(f"\nNew prediction: {self.class_names[self.black_box_model.predict(pd.DataFrame([counterfactual_instance]))[0]]}")
        else:
            print("Could not find a simple counterfactual explanation.")

    def subgroup_divergence_analysis(self, X_data, y_true):
        print("\n--- 4. Subgroup Divergence Analysis (Simulated) ---")
        predictions = self.black_box_model.predict(X_data)
        overall_accuracy = accuracy_score(y_true, predictions)
        print(f"Overall model accuracy: {overall_accuracy:.2f}")

        subgroups = {
            "Elderly_HighChronic": (X_data['Age'] > 70) & (X_data['ChronicDiseaseCount'] >= 3),
            "Young_LowAdherence": (X_data['Age'] < 40) & (X_data['MedicationAdherence'] < 0.4),
            "NoInsurance_HighLabA": (X_data['InsuranceType_None'] == 1) & (X_data['LabResult_A'] > 110)
        }

        print("\nAnalyzing performance across defined subgroups:")
        for name, mask in subgroups.items():
            if mask.sum() > 0:
                subgroup_X = X_data[mask]
                subgroup_y_true = y_true[mask]
                subgroup_predictions = self.black_box_model.predict(subgroup_X)
                subgroup_accuracy = accuracy_score(subgroup_y_true, subgroup_predictions)
                print(f"  - Subgroup '{name}' (n={mask.sum()}): Accuracy = {subgroup_accuracy:.2f}")
                if abs(subgroup_accuracy - overall_accuracy) > 0.1:
                    print(f"    -> Significant divergence detected! Accuracy difference: {subgroup_accuracy - overall_accuracy:.2f}")
                    print("    (In a full system, further XAI would explain the reasons for this divergence)")
            else:
                print(f"  - Subgroup '{name}': No samples found.")

    def interactive_exploration_menu(self, X_data, y_true):
        print("\n--- 5. Interactive Human-in-the-Loop Explanation Tool (Simulated) ---")
        print("Welcome to the Healthcare Patient Risk XAI Dashboard!")
        while True:
            print("\nChoose an action:")
            print("1. Get Global Model Understanding")
            print("2. Explain a Specific Patient's Prediction")
            print("3. Find Counterfactual for a Patient")
            print("4. Perform Subgroup Analysis")
            print("5. Exit")
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.global_surrogate_model()
            elif choice == '2':
                patient_idx_str = input(f"Enter patient index (0 to {len(X_data) - 1}): ")
                try:
                    patient_idx = int(patient_idx_str)
                    if 0 <= patient_idx < len(X_data):
                        self.explain_local_prediction(patient_idx, X_data)
                    else:
                        print("Invalid index.")
                except ValueError:
                    print("Invalid input.")
            elif choice == '3':
                patient_idx_str = input(f"Enter patient index (0 to {len(X_data) - 1}): ")
                try:
                    patient_idx = int(patient_idx_str)
                    if 0 <= patient_idx < len(X_data):
                        self.generate_counterfactual(patient_idx, X_data, desired_prediction=0)
                    else:
                        print("Invalid index.")
                except ValueError:
                    print("Invalid input.")
            elif choice == '4':
                self.subgroup_divergence_analysis(X_data, y_true)
            elif choice == '5':
                print("Exiting XAI Dashboard. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

healthcare_xai = HealthcareXAI(black_box_model, X_train, feature_names)
healthcare_xai.interactive_exploration_menu(X_test, y_test)
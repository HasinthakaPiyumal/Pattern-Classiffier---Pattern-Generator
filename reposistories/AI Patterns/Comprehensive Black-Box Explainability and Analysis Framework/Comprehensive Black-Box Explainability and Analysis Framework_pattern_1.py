import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import lime
import lime.lime_tabular
import shap

# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings("ignore")

class ComprehensiveBlackBoxExplainabilityFramework:
    def __init__(self, black_box_model, feature_names, class_names, training_data):
        self.black_box_model = black_box_model
        self.feature_names = feature_names
        self.class_names = class_names
        self.training_data = training_data # Used for LIME, SHAP, and subgroup analysis

        # LIME explainer setup
        self.lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=training_data,
            feature_names=feature_names,
            class_names=class_names,
            mode='classification'
        )

        # SHAP explainer setup (using KernelExplainer for model-agnostic approach)
        # Note: For tree models, TreeExplainer is more efficient, but KernelExplainer is more general.
        # Using a subset of training_data for background for faster SHAP explanations
        background_data = shap.sample(training_data, k=100)
        self.shap_explainer = shap.KernelExplainer(black_box_model.predict_proba, background_data)

    def _predict_wrapper(self, X):
        """Wrapper for black_box_model.predict_proba for LIME/SHAP compatibility."""
        return self.black_box_model.predict_proba(X)

    def global_understanding_surrogate(self):
        """
        1. Global Understanding: Interpretable Global Surrogate Model.
        Trains a simpler model on the black-box model's predictions.
        Real-world usage: Hospital administrators want to understand overall risk factors for heart disease.
        """
        print("\n--- 1. Global Understanding: Interpretable Global Surrogate Model ---")
        # Use training data for surrogate model training
        X_surrogate = self.training_data
        y_black_box_predictions = self.black_box_model.predict(X_surrogate)

        # Train a Decision Tree as a global surrogate
        surrogate_model = DecisionTreeClassifier(max_depth=5, random_state=42)
        surrogate_model.fit(X_surrogate, y_black_box_predictions)

        surrogate_accuracy = accuracy_score(y_black_box_predictions, surrogate_model.predict(X_surrogate))
        print(f"Surrogate Model (Decision Tree) Accuracy (approximating black-box): {surrogate_accuracy:.2f}")
        print("Top features influencing black-box global behavior (from surrogate model):")
        feature_importances = pd.Series(surrogate_model.feature_importances_, index=self.feature_names)
        print(feature_importances.nlargest(5))
        return surrogate_model

    def local_prediction_explanation(self, instance, top_features=5):
        """
        2. Local Prediction Explanation: LIME, SHAP, and simulated Local Rule-Based.
        Explains a single instance's prediction.
        Real-world usage: A doctor wants to understand why a specific patient was flagged as high-risk for heart failure.
        """
        print(f"\n--- 2. Local Prediction Explanation for instance: {instance} ---")
        black_box_prediction = self.black_box_model.predict(instance.reshape(1, -1))[0]
        black_box_proba = self.black_box_model.predict_proba(instance.reshape(1, -1))[0]
        print(f"Black-box model prediction: {self.class_names[black_box_prediction]} (Proba: {black_box_proba[black_box_prediction]:.2f})")

        # LIME Explanation
        print("\n  -- LIME Explanation --")
        lime_explanation = self.lime_explainer.explain_instance(
            data_row=instance,
            predict_fn=self._predict_wrapper,
            num_features=top_features,
            num_samples=1000 # Increase samples for better stability
        )
        print("  LIME local feature importance:")
        for feature, weight in lime_explanation.as_list():
            print(f"    {feature}: {weight:.4f}")

        # SHAP Explanation
        print("\n  -- SHAP Explanation --")
        # SHAP values for a single instance might take time with KernelExplainer on large background
        shap_values = self.shap_explainer.shap_values(instance.reshape(1, -1))[0] # Assuming binary, take first element

        if isinstance(shap_values, list): # For multi-class, shap_values is a list of arrays
             shap_values_for_pred = shap_values[black_box_prediction]
        else: # For binary, it's just one array
             shap_values_for_pred = shap_values

        shap_df = pd.DataFrame({'feature': self.feature_names, 'shap_value': shap_values_for_pred})
        shap_df['abs_shap_value'] = np.abs(shap_df['shap_value'])
        print("  SHAP local feature importance (fair contribution):")
        print(shap_df.sort_values(by='abs_shap_value', ascending=False).head(top_features).round(4))

        # Simulated Local Rule-Based Explanation (Anchor/LORE-like)
        # A simple simulation: find features with high positive contribution in LIME/SHAP
        # and form a rule based on the instance's values.
        print("\n  -- Simulated Local Rule-Based Explanation (IF-THEN) --")
        rule_parts = []
        lime_features = lime_explanation.as_list()
        # Sort LIME features by absolute weight to pick the most influential ones
        lime_features_sorted = sorted(lime_features, key=lambda x: abs(x[1]), reverse=True)

        for i, (feature_name_expr, weight) in enumerate(lime_features_sorted[:3]): # Top 3 most impactful
            # Extract base feature name (e.g., 'Age' from 'Age > 50')
            feature_name = feature_name_expr.split(' ')[0]
            feature_index = self.feature_names.index(feature_name)
            feature_value = instance[feature_index]
            
            # Simple heuristic: positive weight implies higher value contributes, negative implies lower
            # This is a simplification; a real rule extractor would learn thresholds.
            op = ">" if weight > 0 else "<="
            rule_parts.append(f"{feature_name} {op} {feature_value:.2f}")

        if rule_parts:
            print(f"  IF {' AND '.join(rule_parts)} THEN {self.class_names[black_box_prediction]}")
        else:
            print("  Could not derive simple local rule.")

    def counterfactual_explanation(self, original_instance, target_class_idx, max_iterations=200, step_size_factor=0.05):
        """
        3. Actionable Insights: Counterfactual Explanations.
        Finds minimal changes to flip prediction. (Simplified simulation)
        Real-world usage: A patient wants to know what lifestyle changes (e.g., reducing cholesterol) would lower their heart disease risk.
        """
        print(f"\n--- 3. Actionable Insights: Counterfactual Explanation ---")
        original_pred = self.black_box_model.predict(original_instance.reshape(1, -1))[0]
        print(f"Original instance prediction: {self.class_names[original_pred]}")
        print(f"Target prediction: {self.class_names[target_class_idx]}")

        if original_pred == target_class_idx:
            print("Original prediction already matches target. No counterfactual needed.")
            return

        counterfactual_instance = np.copy(original_instance)
        changes = {}
        found_cf = False

        # Simple iterative search for counterfactuals
        # Prioritize features identified as important by SHAP/LIME (conceptual)
        # For simplicity, we iterate through features and try to perturb them.
        
        # Get feature importances from a local explanation (e.g., LIME) to guide perturbation
        lime_explanation = self.lime_explainer.explain_instance(
            data_row=original_instance,
            predict_fn=self._predict_wrapper,
            num_features=len(self.feature_names),
            num_samples=500
        )
        feature_weights = {item[0].split(' ')[0]: item[1] for item in lime_explanation.as_list()}
        # Sort features by absolute weight for targeted perturbation
        sorted_features = sorted(feature_weights.items(), key=lambda item: abs(item[1]), reverse=True)

        for iteration in range(max_iterations):
            current_pred = self.black_box_model.predict(counterfactual_instance.reshape(1, -1))[0]
            if current_pred == target_class_idx:
                found_cf = True
                break

            # Pick a feature to perturb based on importance or randomly if no importance
            # Prioritize features that push towards the target class (if weight aligns)
            best_feature_to_perturb_idx = -1
            best_perturb_direction = 0 # -1 for decrease, 1 for increase

            for feature_name, weight in sorted_features:
                feature_idx = self.feature_names.index(feature_name)
                original_value = original_instance[feature_idx]
                current_cf_value = counterfactual_instance[feature_idx]
                std_dev = self.training_data[:, feature_idx].std() or 1.0
                step = step_size_factor * std_dev

                # Try to move feature value in a direction that might flip the prediction
                # This is a very simple heuristic: if the feature's weight is positive for the current prediction
                # and we want to change the prediction, we might want to decrease it, and vice versa.
                # A more robust approach would involve gradient-based search or specific CF algorithms.

                temp_cf_increase = np.copy(counterfactual_instance)
                temp_cf_increase[feature_idx] += step
                if self.black_box_model.predict(temp_cf_increase.reshape(1, -1))[0] == target_class_idx:
                    best_feature_to_perturb_idx = feature_idx
                    best_perturb_direction = 1
                    break

                temp_cf_decrease = np.copy(counterfactual_instance)
                temp_cf_decrease[feature_idx] -= step
                if self.black_box_model.predict(temp_cf_decrease.reshape(1, -1))[0] == target_class_idx:
                    best_feature_to_perturb_idx = feature_idx
                    best_perturb_direction = -1
                    break

            if best_feature_to_perturb_idx != -1:
                feature_idx = best_feature_to_perturb_idx
                std_dev = self.training_data[:, feature_idx].std() or 1.0
                step = step_size_factor * std_dev
                
                counterfactual_instance[feature_idx] += best_perturb_direction * step
                changes[self.feature_names[feature_idx]] = counterfactual_instance[feature_idx]
            else:
                # If no direct flip, randomly perturb a feature if no specific guidance
                feature_idx = np.random.randint(len(self.feature_names))
                std_dev = self.training_data[:, feature_idx].std() or 1.0
                step = step_size_factor * std_dev
                perturb_dir = np.random.choice([-1, 1])
                counterfactual_instance[feature_idx] += perturb_dir * step
                changes[self.feature_names[feature_idx]] = counterfactual_instance[feature_idx]


        if found_cf:
            print(f"  Counterfactual found after {iteration+1} iterations.")
            print("  Minimal changes to flip prediction:")
            final_changes = {}
            for feature, new_value in changes.items():
                original_val = original_instance[self.feature_names.index(feature)]
                # Only report features that actually changed significantly from original
                if abs(new_value - original_val) > 1e-3: 
                    final_changes[feature] = (original_val, new_value)
            
            if final_changes:
                for feature, (original_val, new_value) in final_changes.items():
                    print(f"    Change '{feature}' from {original_val:.2f} to {new_value:.2f}")
                print(f"  New prediction: {self.class_names[self.black_box_model.predict(counterfactual_instance.reshape(1, -1))[0]]}")
            else:
                print("  Counterfactual found but no significant feature changes recorded (likely very subtle changes).")
        else:
            print("  Could not find a simple counterfactual within limits. More complex search or different target needed.")


    def subgroup_divergence_analysis(self, subgroup_feature_idx, num_bins=3):
        """
        4. Subgroup Analysis: DivExplorer Algorithm (Simplified Simulation).
        Identifies and characterizes data subgroups where model behavior diverges.
        Real-world usage: Hospital management discovers the model consistently underpredicts risk for younger female patients,
        potentially indicating bias or data issues in that subgroup.
        """
        print(f"\n--- 4. Subgroup Divergence Analysis ---")
        feature_name = self.feature_names[subgroup_feature_idx]
        print(f"Analyzing divergence based on feature: '{feature_name}'")

        # Create bins for the subgroup feature (e.g., age groups)
        feature_values = self.training_data[:, subgroup_feature_idx]
        bins = np.linspace(feature_values.min(), feature_values.max(), num_bins + 1)
        bin_labels = [f'{bins[i]:.0f}-{bins[i+1]:.0f}' for i in range(num_bins)]
        
        subgroups = pd.cut(feature_values, bins=bins, labels=bin_labels, include_lowest=True)
        subgroup_data = pd.DataFrame(self.training_data, columns=self.feature_names)
        subgroup_data['subgroup'] = subgroups
        # Use black-box model's predictions on training data to assess 'divergence' in its own behavior
        subgroup_data['black_box_prediction'] = self.black_box_model.predict(self.training_data)

        # Calculate overall accuracy for the black-box model on the training data
        overall_pred = self.black_box_model.predict(self.training_data)
        # For divergence analysis, we need a 'ground truth'. Here, we'll compare subgroup predictions
        # against the overall distribution of predictions, or against true labels if available.
        # For simplicity, we'll calculate accuracy against the model's own predictions as a baseline for 'expected' behavior.
        # In a real scenario, you'd compare against true labels (y_train).
        global_prediction_distribution = np.bincount(overall_pred, minlength=len(self.class_names)) / len(overall_pred)
        print(f"Overall model prediction distribution: {global_prediction_distribution}")
        
        print("\nSubgroup Prediction Divergence (comparing distribution to overall):")
        
        divergent_subgroups_info = []

        for name, group in subgroup_data.groupby('subgroup'):
            if len(group) == 0: continue
            
            group_X = group[self.feature_names].values
            group_predictions = self.black_box_model.predict(group_X)
            group_prediction_distribution = np.bincount(group_predictions, minlength=len(self.class_names)) / len(group_predictions)
            
            # Calculate a simple divergence metric (e.g., Euclidean distance between distributions)
            divergence_metric = np.linalg.norm(global_prediction_distribution - group_prediction_distribution)

            print(f"  Subgroup '{name}' (N={len(group)}): Prediction Distribution = {group_prediction_distribution.round(2)}, Divergence from overall = {divergence_metric:.3f}")
            if divergence_metric > 0.15: # Threshold for significant divergence
                print(f"    --> Significant divergence detected! Model's prediction patterns differ here.")
                divergent_subgroups_info.append((name, group_X))

        # Simulate identifying contributing factors to divergence using SHAP for a divergent subgroup
        print("\n  Conceptual: Identifying contributing factors to divergence within a subgroup:")
        if divergent_subgroups_info:
            # Pick the first significantly divergent subgroup for detailed analysis
            divergent_group_name, divergent_group_X = divergent_subgroups_info[0]
            if len(divergent_group_X) > 0:
                print(f"    For divergent subgroup '{divergent_group_name}', top features affecting predictions:")
                # Explain a few samples from the divergent group
                samples_for_shap = divergent_group_X[:min(50, len(divergent_group_X))]
                if len(samples_for_shap) > 0:
                    subgroup_shap_values = self.shap_explainer.shap_values(samples_for_shap)
                    
                    if isinstance(subgroup_shap_values, list): # Multi-class output
                        # Average absolute SHAP values across all classes for simplicity
                        avg_abs_shap_values_per_class = [np.mean(np.abs(sv), axis=0) for sv in subgroup_shap_values]
                        avg_shap_values = np.mean(avg_abs_shap_values_per_class, axis=0)
                    else: # Binary class output
                        avg_shap_values = np.mean(np.abs(subgroup_shap_values), axis=0)

                    shap_df = pd.DataFrame({'feature': self.feature_names, 'avg_abs_shap_value': avg_shap_values})
                    print(shap_df.sort_values(by='avg_abs_shap_value', ascending=False).head(3).round(4))
                else:
                    print(f"    Not enough samples in subgroup '{divergent_group_name}' for SHAP analysis.")
            else:
                print(f"    Not enough data in subgroup '{divergent_group_name}' for SHAP analysis.")
        else:
            print("    No significantly divergent subgroups found.")


    def interactive_exploration_sim(self):
        """
        5. Interactive Human-in-the-Loop Explanation Tools (Simulated).
        Conceptual demonstration of how a user would interact.
        Real-world usage: A researcher uses a dashboard to drill down into the 'younger female' subgroup,
        compare their feature distributions, and see if specific features contribute differently to risk predictions within that group.
        """
        print("\n--- 5. Interactive Exploration (Simulated) ---")
        print("Imagine a dashboard where a healthcare professional or researcher can interactively:")
        print("  - View global surrogate model insights to understand general risk factors.")
        print("  - Input a patient's data to get detailed LIME, SHAP, and rule-based explanations for their specific risk prediction.")
        print("  - Ask 'what-if' questions (counterfactuals) to see how changing lifestyle factors (e.g., 'What if patient's cholesterol was lower?') impacts their risk.")
        print("  - Drill down into patient subgroups (e.g., 'females aged 30-40' or 'patients with diabetes') to see their specific model performance and feature contributions.")
        print("  - Compare explanations across different patients or subgroups to identify patterns or inconsistencies.")
        print("  - Define custom rules or thresholds for alerts based on insights gained.")
        print("\n  This framework provides the underlying mechanisms for such a powerful interactive tool, fostering trust and enabling informed decision-making in healthcare.")


# --- Simulation Pattern: Healthcare Scenario (Patient Heart Disease Risk Prediction) ---
if __name__ == "__main__":
    # 0. Simulate a healthcare dataset
    np.random.seed(42)
    num_patients = 1000
    
    # Features: Age, BMI, Cholesterol, BloodPressure, Glucose, SmokingHistory (0/1), FamilyHistory (0/1)
    feature_names = ['Age', 'BMI', 'Cholesterol', 'BloodPressure', 'Glucose', 'SmokingHistory', 'FamilyHistory']
    
    data = {
        'Age': np.random.normal(50, 15, num_patients).clip(20, 80).astype(int),
        'BMI': np.random.normal(28, 5, num_patients).clip(18, 40),
        'Cholesterol': np.random.normal(200, 40, num_patients).clip(120, 300),
        'BloodPressure': np.random.normal(130, 15, num_patients).clip(90, 180),
        'Glucose': np.random.normal(100, 20, num_patients).clip(70, 250),
        'SmokingHistory': np.random.randint(0, 2, num_patients),
        'FamilyHistory': np.random.randint(0, 2, num_patients)
    }
    
    X = pd.DataFrame(data)
    
    # Simulate a 'Risk' target variable (0: Low, 1: Moderate, 2: High)
    # Risk is higher with higher Age, BMI, Cholesterol, BP, Glucose, Smoking, FamilyHistory
    risk_score = (
        0.3 * (X['Age'] / 80) + # Age is a significant factor
        0.2 * (X['BMI'] / 40) + # BMI contributes
        0.2 * (X['Cholesterol'] / 300) + # Cholesterol is key
        0.1 * (X['BloodPressure'] / 180) + 
        0.1 * (X['Glucose'] / 250) + 
        0.05 * X['SmokingHistory'] + 
        0.05 * X['FamilyHistory']
    )
    
    # Convert risk_score to discrete classes
    y = np.zeros(num_patients, dtype=int)
    y[risk_score > 0.4] = 1 # Moderate risk
    y[risk_score > 0.6] = 2 # High risk
    
    class_names = ['Low Risk', 'Moderate Risk', 'High Risk']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X.values, y, test_size=0.2, random_state=42)

    # Train a black-box model (RandomForestClassifier)
    black_box_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    black_box_model.fit(X_train, y_train)
    print(f"Black-box model (RandomForest) accuracy on test set: {accuracy_score(y_test, black_box_model.predict(X_test)):.2f}")

    # Initialize the Comprehensive Explainability Framework
    framework = ComprehensiveBlackBoxExplainabilityFramework(
        black_box_model=black_box_model,
        feature_names=feature_names,
        class_names=class_names,
        training_data=X_train
    )

    # --- Real-World Usage Demonstration ---

    # 1. Global Understanding: Hospital administrators want to understand overall risk factors for heart disease.
    framework.global_understanding_surrogate()

    # 2. Local Prediction Explanation: A doctor wants to understand why Patient X (e.g., test instance 5) is High Risk.
    patient_instance_idx = 5
    patient_instance = X_test[patient_instance_idx]
    print(f"\n--- Demonstrating for Patient {patient_instance_idx} (True Risk: {class_names[y_test[patient_instance_idx]]}) ---")
    framework.local_prediction_explanation(patient_instance)

    # 3. Actionable Insights: Patient X wants to know how to reduce their risk from High to Moderate.
    # We need to find the index for 'Moderate Risk'
    moderate_risk_idx = class_names.index('Moderate Risk')
    framework.counterfactual_explanation(patient_instance, moderate_risk_idx)

    # 4. Subgroup Analysis: Hospital management suspects bias/divergence for certain age groups.
    age_feature_idx = feature_names.index('Age')
    framework.subgroup_divergence_analysis(age_feature_idx, num_bins=4) # Divide Age into 4 groups

    # 5. Interactive Exploration (Simulated): Show how these pieces would fit into a UI.
    framework.interactive_exploration_sim()

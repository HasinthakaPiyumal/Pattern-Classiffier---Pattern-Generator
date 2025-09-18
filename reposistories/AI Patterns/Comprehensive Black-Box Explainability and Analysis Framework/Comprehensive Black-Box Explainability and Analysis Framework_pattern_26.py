import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification

import lime
import lime.lime_tabular
import shap
from alibi.explainers import AnchorTabular
import dice_ml
from dice_ml.utils import helpers

def program1_banking():
    np.random.seed(42)
    n_samples = 1000
    n_features = 5
    X, y = make_classification(n_samples=n_samples, n_features=n_features, n_informative=n_features,
                               n_redundant=0, n_repeated=0, n_classes=2, random_state=42)
    feature_names = ['CreditScore', 'Income', 'LoanAmount', 'DebtToIncomeRatio', 'EmploymentYears']
    class_names = ['NoDefault', 'Default']
    
    X[:, 0] = np.random.randint(300, 850, n_samples)
    X[:, 1] = np.random.randint(30000, 150000, n_samples)
    X[:, 2] = np.random.randint(5000, 500000, n_samples)
    X[:, 3] = np.random.rand(n_samples) * 0.6
    X[:, 4] = np.random.randint(0, 30, n_samples)

    y = np.where((X[:, 0] < 550) & (X[:, 3] > 0.4) & (X[:, 2] > 100000), 1, y)
    y = np.where((X[:, 0] > 700) & (X[:, 3] < 0.2) & (X[:, 1] > 80000), 0, y)
    y = np.clip(y, 0, 1)

    X_df = pd.DataFrame(X, columns=feature_names)
    X_train, X_test, y_train, y_test = train_test_split(X_df, y, test_size=0.2, random_state=42)

    bb_model = RandomForestClassifier(n_estimators=100, random_state=42)
    bb_model.fit(X_train, y_train)
    
    output = []

    surrogate_model = DecisionTreeClassifier(max_depth=4, random_state=42)
    surrogate_model.fit(X_train, bb_model.predict(X_train))
    output.append(f"GLOBAL UNDERSTANDING (Decision Tree Surrogate):\nSurrogate Model Accuracy: {accuracy_score(y_test, surrogate_model.predict(X_test)):.2f}\nDecision Path for Root Node (simplified): If {feature_names[surrogate_model.tree_.feature[0]]} <= {surrogate_model.tree_.threshold[0]:.2f} then ... else ...")

    instance_idx = 0
    instance = X_test.iloc[[instance_idx]]
    instance_array = X_test.iloc[instance_idx].values
    true_label = y_test[instance_idx]
    bb_prediction = bb_model.predict(instance)[0]
    bb_proba = bb_model.predict_proba(instance)[0]
    output.append(f"\nExplaining Instance {instance_idx}: True Label={class_names[true_label]}, BB Prediction={class_names[bb_prediction]} (Proba: {bb_proba[0]:.2f}/{bb_proba[1]:.2f})")

    explainer_lime = lime.lime_tabular.LimeTabularExplainer(
        training_data=X_train.values,
        feature_names=feature_names,
        class_names=class_names,
        mode='classification'
    )
    exp_lime = explainer_lime.explain_instance(
        data_row=instance_array,
        predict_fn=bb_model.predict_proba,
        num_features=len(feature_names)
    )
    output.append(f"\nLOCAL EXPLANATION (LIME):\nFeatures contributing to prediction {class_names[bb_prediction]}:\n" +
                  "\n".join([f"  {f}: {v:.2f}" for f, v in exp_lime.as_list()]))

    explainer_shap = shap.TreeExplainer(bb_model)
    shap_values = explainer_shap.shap_values(instance)
    predicted_class_shap_values = shap_values[bb_prediction][0]
    output.append(f"\nLOCAL EXPLANATION (SHAP) for prediction {class_names[bb_prediction]}:\n" +
                  "\n".join([f"  {feature_names[i]}: {predicted_class_shap_values[i]:.2f}" for i in range(len(feature_names))]))

    explainer_anchor = AnchorTabular(bb_model.predict, feature_names, X_train.values)
    exp_anchor = explainer_anchor.explain(instance_array, threshold=0.95)
    output.append(f"\nLOCAL RULE-BASED EXPLANATION (Anchor):\nAnchor for prediction {class_names[bb_prediction]}: {exp_anchor.anchor}\nPrecision: {exp_anchor.precision:.2f}, Coverage: {exp_anchor.coverage:.2f}")

    d = dice_ml.Data(dataframe=pd.concat([X_train, pd.Series(y_train, name='target')], axis=1),
                     continuous_features=feature_names, outcome_name='target')
    m = dice_ml.Model(model=bb_model, backend='sklearn')
    exp_dice = dice_ml.Dice(d, m, method='kdtree') 
    
    desired_class = 1 - bb_prediction
    cf_explanation = exp_dice.generate_counterfactuals(instance, total_CFs=1, desired_class=desired_class)
    
    cf_output = ""
    if cf_explanation.cf_examples_list and cf_explanation.cf_examples_list[0].final_cfs_df is not None:
        original_values = instance.values[0]
        cf_values = cf_explanation.cf_examples_list[0].final_cfs_df.drop('target', axis=1).values[0]
        changes = []
        for i, f in enumerate(feature_names):
            if not np.isclose(original_values[i], cf_values[i]):
                changes.append(f"{f}: {original_values[i]:.2f} -> {cf_values[i]:.2f}")
        cf_output = "\n".join(changes)
    else:
        cf_output = "No counterfactual found for the opposite class."

    output.append(f"\nACTIONABLE INSIGHTS (Counterfactual Explanation to achieve {class_names[desired_class]}):\nMinimal changes to input for desired outcome:\n{cf_output}")

    subgroup_mask = (X_test['DebtToIncomeRatio'] > 0.4) & (X_test['CreditScore'] < 600)
    subgroup_X = X_test[subgroup_mask]
    subgroup_y = y_test[subgroup_mask]

    overall_accuracy = accuracy_score(y_test, bb_model.predict(X_test))
    subgroup_accuracy = accuracy_score(subgroup_y, bb_model.predict(subgroup_X)) if len(subgroup_y) > 0 else np.nan

    output.append(f"\nSUBGROUP ANALYSIS (High Debt/Low CreditScore):\nOverall Model Accuracy: {overall_accuracy:.2f}\nSubgroup Size: {len(subgroup_y)} instances\nSubgroup Model Accuracy: {subgroup_accuracy:.2f} (Divergence: {overall_accuracy - subgroup_accuracy:.2f} {'(Worse)' if (not np.isnan(subgroup_accuracy) and subgroup_accuracy < overall_accuracy) else '(Better)' if (not np.isnan(subgroup_accuracy) and subgroup_accuracy > overall_accuracy) else ''})")
    if len(subgroup_y) > 0:
        subgroup_shap_values = explainer_shap.shap_values(subgroup_X)
        if isinstance(subgroup_shap_values, list):
            mean_shap_subgroup = np.mean(np.abs(subgroup_shap_values[1]), axis=0)
        else:
            mean_shap_subgroup = np.mean(np.abs(subgroup_shap_values), axis=0)
        
        output.append(f"Mean Absolute SHAP for 'Default' in Subgroup:\n" +
                      "\n".join([f"  {feature_names[i]}: {mean_shap_subgroup[i]:.2f}" for i in range(len(feature_names))]))

    output.append(f"\nINTERACTIVE EXPLORATION (SIMULATION):\nYou can now inspect individual explanations, compare them, perform 'what-if' analysis (like the counterfactual above), and drill down into identified subgroups. For instance, comparing the current instance's explanation with another:\nInstance {instance_idx} (predicted {class_names[bb_prediction]}) has high importance for {exp_lime.as_list()[0][0]}.\nA different instance might show {feature_names[np.random.randint(0, len(feature_names))]} as most important, leading to a different outcome.")
    
    return "\n".join(output)

print(program1_banking())
import collections

class UserContext:
    HIGH_RECALL = "high_recall"
    INTERPRETABILITY = "interpretability"
    PRIVACY = "privacy"

class DataContext:
    MIXED_TYPES = "mixed_types"
    IMBALANCED = "imbalanced"
    MISSING_VALUES = "missing_values"
    INDEPENDENT_FEATURES = "independent_features"

class ModelContext:
    LOW_LATENCY = "low_latency"
    EXPLAINABLE = "explainable"

class Softgoal:
    MAXIMIZE_RECALL = "maximize_recall"
    MAXIMIZE_INTERPRETABILITY = "maximize_interpretability"
    ENSURE_PRIVACY = "ensure_privacy"
    OPTIMIZE_LATENCY = "optimize_latency"

class MLSolutionDesigner:
    def __init__(self):
        self.algorithm_rules = {
            (UserContext.HIGH_RECALL, DataContext.IMBALANCED, Softgoal.MAXIMIZE_RECALL): "SMOTE_and_RandomForest",
            (UserContext.INTERPRETABILITY, DataContext.MIXED_TYPES, Softgoal.MAXIMIZE_INTERPRETABILITY): "LogisticRegression",
            (UserContext.INTERPRETABILITY, DataContext.INDEPENDENT_FEATURES, Softgoal.MAXIMIZE_INTERPRETABILITY): "NaiveBayes",
            (ModelContext.LOW_LATENCY, None, Softgoal.OPTIMIZE_LATENCY): "SVM_with_linear_kernel",
            (UserContext.PRIVACY, None, Softgoal.ENSURE_PRIVACY): "FederatedLearning_or_DifferentialPrivacy"
        }
        self.data_prep_rules = {
            ("SMOTE_and_RandomForest", DataContext.IMBALANCED): ["handle_missing_values", "one_hot_encode", "SMOTE_oversampling"],
            ("LogisticRegression", DataContext.MIXED_TYPES): ["handle_missing_values", "scale_numerical", "one_hot_encode"],
            ("NaiveBayes", DataContext.MIXED_TYPES): ["handle_missing_values", "discretize_numerical"],
            ("SVM_with_linear_kernel", DataContext.MIXED_TYPES): ["handle_missing_values", "scale_numerical", "one_hot_encode"]
        }
        self.evaluation_metric_rules = {
            (UserContext.HIGH_RECALL, Softgoal.MAXIMIZE_RECALL): "Recall",
            (UserContext.INTERPRETABILITY, Softgoal.MAXIMIZE_INTERPRETABILITY): "AUC_ROC",
            (UserContext.PRIVACY, Softgoal.ENSURE_PRIVACY): "Privacy_Preservation_Metrics",
            (ModelContext.LOW_LATENCY, Softgoal.OPTIMIZE_LATENCY): "Prediction_Time_Latency"
        }

    def select_algorithm(self, user_ctx, data_ctx, model_ctx, softgoals):
        chosen_algo = "DefaultAlgorithm"
        for softgoal in softgoals:
            if (user_ctx, data_ctx, softgoal) in self.algorithm_rules:
                chosen_algo = self.algorithm_rules[(user_ctx, data_ctx, softgoal)]
                break
            if (model_ctx, None, softgoal) in self.algorithm_rules:
                chosen_algo = self.algorithm_rules[(model_ctx, None, softgoal)]
                break
        return chosen_algo

    def prepare_data(self, chosen_algorithm, data_ctx):
        key = (chosen_algorithm, data_ctx)
        return self.data_prep_rules.get(key, ["default_preprocessing"])

    def select_evaluation_metric(self, user_ctx, model_ctx, softgoals):
        chosen_metric = "Accuracy"
        for softgoal in softgoals:
            if (user_ctx, softgoal) in self.evaluation_metric_rules:
                chosen_metric = self.evaluation_metric_rules[(user_ctx, softgoal)]
                break
            if (model_ctx, softgoal) in self.evaluation_metric_rules:
                chosen_metric = self.evaluation_metric_rules[(model_ctx, softgoal)]
                break
        return chosen_metric

# Real-world usage simulation: Healthcare - Disease Prediction
def simulate_disease_prediction_solution(patient_data_characteristics, doctor_priority, system_requirements):
    designer = MLSolutionDesigner()

    # Map simulation inputs to defined contexts and softgoals
    user_ctx = None
    if doctor_priority == "not_miss_cases": user_ctx = UserContext.HIGH_RECALL
    elif doctor_priority == "understand_reasons": user_ctx = UserContext.INTERPRETABILITY
    elif doctor_priority == "patient_privacy": user_ctx = UserContext.PRIVACY
    
    data_ctx = None
    if patient_data_characteristics == "imbalanced_mixed": data_ctx = DataContext.IMBALANCED
    elif patient_data_characteristics == "independent_features": data_ctx = DataContext.INDEPENDENT_FEATURES
    elif patient_data_characteristics == "general_mixed": data_ctx = DataContext.MIXED_TYPES

    model_ctx = None
    if system_requirements == "realtime": model_ctx = ModelContext.LOW_LATENCY
    elif system_requirements == "explainable": model_ctx = ModelContext.EXPLAINABLE

    softgoals = []
    if user_ctx == UserContext.HIGH_RECALL: softgoals.append(Softgoal.MAXIMIZE_RECALL)
    if user_ctx == UserContext.INTERPRETABILITY: softgoals.append(Softgoal.MAXIMIZE_INTERPRETABILITY)
    if user_ctx == UserContext.PRIVACY: softgoals.append(Softgoal.ENSURE_PRIVACY)
    if model_ctx == ModelContext.LOW_LATENCY: softgoals.append(Softgoal.OPTIMIZE_LATENCY)

    print(f"\n--- Designing ML Solution for Disease Prediction ---")
    print(f"Input Contexts: User={user_ctx}, Data={data_ctx}, Model={model_ctx}, Softgoals={softgoals}")

    chosen_algorithm = designer.select_algorithm(user_ctx, data_ctx, model_ctx, softgoals)
    print(f"Selected Algorithm: {chosen_algorithm}")

    data_prep_steps = designer.prepare_data(chosen_algorithm, data_ctx)
    print(f"Data Preparation Steps: {', '.join(data_prep_steps)}")

    evaluation_metric = designer.select_evaluation_metric(user_ctx, model_ctx, softgoals)
    print(f"Evaluation Metric: {evaluation_metric}")
    print(f"----------------------------------------------------")

# Simulation 1: Prioritizing not missing cases (high recall) for imbalanced data
simulate_disease_prediction_solution(
    patient_data_characteristics="imbalanced_mixed",
    doctor_priority="not_miss_cases",
    system_requirements="standard_latency"
)

# Simulation 2: Prioritizing interpretability for general mixed data
simulate_disease_prediction_solution(
    patient_data_characteristics="general_mixed",
    doctor_priority="understand_reasons",
    system_requirements="standard_latency"
)

# Simulation 3: Prioritizing low latency
simulate_disease_prediction_solution(
    patient_data_characteristics="general_mixed",
    doctor_priority="standard_accuracy",
    system_requirements="realtime"
)

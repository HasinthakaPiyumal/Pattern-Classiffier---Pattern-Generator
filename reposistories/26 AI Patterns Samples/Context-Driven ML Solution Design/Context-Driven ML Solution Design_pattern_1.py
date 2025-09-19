class UserContext:
    RELEVANCE = "relevance"
    DISCOVERY = "discovery"
    CONVERSION_RATE = "conversion_rate"

class DataContext:
    SPARSE_INTERACTIONS = "sparse_interactions"
    RICH_ITEM_FEATURES = "rich_item_features"
    HIGH_VOLATILITY = "high_volatility"
    COLD_START_USERS = "cold_start_users"

class ModelContext:
    SCALABILITY = "scalability"
    LOW_LATENCY = "low_latency"
    EXPLAINABILITY = "explainability"

class Softgoal:
    MAXIMIZE_RELEVANCE = "maximize_relevance"
    ENHANCE_DISCOVERY = "enhance_discovery"
    OPTIMIZE_CONVERSION = "optimize_conversion"
    HANDLE_COLD_START = "handle_cold_start"
    ENSURE_SCALABILITY = "ensure_scalability"

class MLSolutionDesigner:
    def __init__(self):
        self.algorithm_rules = {
            (UserContext.RELEVANCE, DataContext.SPARSE_INTERACTIONS, Softgoal.MAXIMIZE_RELEVANCE): "CollaborativeFiltering_SVD",
            (UserContext.DISCOVERY, DataContext.RICH_ITEM_FEATURES, Softgoal.ENHANCE_DISCOVERY): "ContentBased_with_embeddings",
            (UserContext.CONVERSION_RATE, DataContext.HIGH_VOLATILITY, Softgoal.OPTIMIZE_CONVERSION): "Hybrid_OnlineLearning",
            (DataContext.COLD_START_USERS, None, Softgoal.HANDLE_COLD_START): "Popularity_or_ContentBased_Fallback",
            (ModelContext.SCALABILITY, None, Softgoal.ENSURE_SCALABILITY): "MatrixFactorization_ALS"
        }
        self.data_prep_rules = {
            ("CollaborativeFiltering_SVD", DataContext.SPARSE_INTERACTIONS): ["matrix_factorization_prep", "handle_implicit_feedback"],
            ("ContentBased_with_embeddings", DataContext.RICH_ITEM_FEATURES): ["text_embedding_generation", "feature_scaling"],
            ("Hybrid_OnlineLearning", DataContext.HIGH_VOLATILITY): ["realtime_feature_engineering", "data_stream_processing"],
            ("Popularity_or_ContentBased_Fallback", DataContext.COLD_START_USERS): ["item_meta_data_processing"],
            ("MatrixFactorization_ALS", DataContext.SPARSE_INTERACTIONS): ["sparse_matrix_construction", "implicit_feedback_conversion"]
        }
        self.evaluation_metric_rules = {
            (UserContext.RELEVANCE, Softgoal.MAXIMIZE_RELEVANCE): "NDCG@K",
            (UserContext.DISCOVERY, Softgoal.ENHANCE_DISCOVERY): "Coverage_Novelty",
            (UserContext.CONVERSION_RATE, Softgoal.OPTIMIZE_CONVERSION): "Click_Through_Rate_Conversion",
            (Softgoal.HANDLE_COLD_START, None): "Cold_Start_Recall",
            (Softgoal.ENSURE_SCALABILITY, None): "Throughput_Latency"
        }

    def select_algorithm(self, user_ctx, data_ctx, model_ctx, softgoals):
        chosen_algo = "DefaultRecommendationAlgo"
        # Prioritize specific context rules
        for softgoal in softgoals:
            if (user_ctx, data_ctx, softgoal) in self.algorithm_rules:
                return self.algorithm_rules[(user_ctx, data_ctx, softgoal)]
            if (data_ctx, None, softgoal) in self.algorithm_rules: # DataContext can sometimes directly imply algo
                return self.algorithm_rules[(data_ctx, None, softgoal)]
            if (model_ctx, None, softgoal) in self.algorithm_rules:
                return self.algorithm_rules[(model_ctx, None, softgoal)]
        return chosen_algo

    def prepare_data(self, chosen_algorithm, data_ctx):
        key = (chosen_algorithm, data_ctx)
        return self.data_prep_rules.get(key, ["standard_e_commerce_preprocessing"])

    def select_evaluation_metric(self, user_ctx, model_ctx, softgoals):
        chosen_metric = "Accuracy"
        for softgoal in softgoals:
            if (user_ctx, softgoal) in self.evaluation_metric_rules:
                return self.evaluation_metric_rules[(user_ctx, softgoal)]
            if (softgoal, None) in self.evaluation_metric_rules: # Softgoals can sometimes directly imply metric
                return self.evaluation_metric_rules[(softgoal, None)]
        return chosen_metric

# Real-world usage simulation: E-commerce - Product Recommendation
def simulate_recommendation_solution(user_preference, data_characteristics, system_constraints):
    designer = MLSolutionDesigner()

    # Map simulation inputs to defined contexts and softgoals
    user_ctx = None
    if user_preference == "most_relevant": user_ctx = UserContext.RELEVANCE
    elif user_preference == "new_discoveries": user_ctx = UserContext.DISCOVERY
    elif user_preference == "business_conversion": user_ctx = UserContext.CONVERSION_RATE
    
    data_ctx = None
    if data_characteristics == "sparse_user_item": data_ctx = DataContext.SPARSE_INTERACTIONS
    elif data_characteristics == "rich_item_metadata": data_ctx = DataContext.RICH_ITEM_FEATURES
    elif data_characteristics == "cold_start_users": data_ctx = DataContext.COLD_START_USERS
    elif data_characteristics == "frequently_changing": data_ctx = DataContext.HIGH_VOLATILITY

    model_ctx = None
    if system_constraints == "handle_millions": model_ctx = ModelContext.SCALABILITY
    elif system_constraints == "realtime_response": model_ctx = ModelContext.LOW_LATENCY

    softgoals = []
    if user_ctx == UserContext.RELEVANCE: softgoals.append(Softgoal.MAXIMIZE_RELEVANCE)
    if user_ctx == UserContext.DISCOVERY: softgoals.append(Softgoal.ENHANCE_DISCOVERY)
    if user_ctx == UserContext.CONVERSION_RATE: softgoals.append(Softgoal.OPTIMIZE_CONVERSION)
    if data_ctx == DataContext.COLD_START_USERS: softgoals.append(Softgoal.HANDLE_COLD_START)
    if model_ctx == ModelContext.SCALABILITY: softgoals.append(Softgoal.ENSURE_SCALABILITY)
    
    print(f"\n--- Designing ML Solution for Product Recommendation ---")
    print(f"Input Contexts: User={user_ctx}, Data={data_ctx}, Model={model_ctx}, Softgoals={softgoals}")

    chosen_algorithm = designer.select_algorithm(user_ctx, data_ctx, model_ctx, softgoals)
    print(f"Selected Algorithm: {chosen_algorithm}")

    data_prep_steps = designer.prepare_data(chosen_algorithm, data_ctx)
    print(f"Data Preparation Steps: {', '.join(data_prep_steps)}")

    evaluation_metric = designer.select_evaluation_metric(user_ctx, model_ctx, softgoals)
    print(f"Evaluation Metric: {evaluation_metric}")
    print(f"--------------------------------------------------------")

# Simulation 1: Prioritizing relevance for sparse user-item interactions
simulate_recommendation_solution(
    user_preference="most_relevant",
    data_characteristics="sparse_user_item",
    system_constraints="standard_scale"
)

# Simulation 2: Prioritizing new discoveries with rich item features
simulate_recommendation_solution(
    user_preference="new_discoveries",
    data_characteristics="rich_item_metadata",
    system_constraints="standard_scale"
)

# Simulation 3: Handling cold-start users
simulate_recommendation_solution(
    user_preference="standard_relevance",
    data_characteristics="cold_start_users",
    system_constraints="standard_scale"
)

# Simulation 4: Ensuring scalability for millions of users
simulate_recommendation_solution(
    user_preference="most_relevant",
    data_characteristics="sparse_user_item",
    system_constraints="handle_millions"
)

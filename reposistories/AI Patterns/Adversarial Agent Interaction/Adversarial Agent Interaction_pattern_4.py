import random

class UserRecommendationRequest:
    def __init__(self, user_id, browsing_history, user_segment):
        self.user_id = user_id
        self.browsing_history = browsing_history
        self.user_segment = user_segment
        self.generated_recommendations = []
        self.final_recommendations = []
        self.security_issues = []

class RecommendationEngineAgent:
    def generate_recommendations(self, request: UserRecommendationRequest):
        potential_recs = []
        if "electronics" in request.browsing_history or request.user_segment == "adult":
            potential_recs.extend(["Laptop X", "Smartphone Y", "Smartwatch Z"])
        if "books" in request.browsing_history:
            potential_recs.extend(["Fantasy Novel", "Biography A", "Tech Manual B"])
        if "toys" in request.browsing_history or request.user_segment == "child":
            potential_recs.extend(["Building Blocks", "Action Figure"])
        
        if random.random() < 0.3:
            potential_recs.append("Restricted Item: Alcohol Kit")
        if random.random() < 0.15:
            potential_recs.append("Scam Product: Get Rich Quick Scheme")
        if random.random() < 0.05:
            potential_recs.append("Illegal Item: Pirated Software")
        
        request.generated_recommendations = list(set(potential_recs))
        print(f"Engine generated {len(request.generated_recommendations)} recommendations for {request.user_id}.")
        return request.generated_recommendations

class SecurityComplianceAgent:
    RESTRICTED_ITEMS = ["Alcohol Kit", "Tobacco Products", "Gambling Software"]
    MALICIOUS_ITEMS = ["Get Rich Quick Scheme", "Fake Lottery Ticket", "Phishing Guide"]
    ILLEGAL_ITEMS = ["Pirated Software", "Counterfeit Goods", "Weapons"]

    def review_recommendations(self, request: UserRecommendationRequest, recommendations: list):
        approved_recs = []
        issues_found = []

        for item in recommendations:
            is_problematic = False
            if item in self.RESTRICTED_ITEMS:
                issues_found.append(f"Restricted item '{item}' detected.")
                if request.user_segment != "adult":
                    is_problematic = True
            elif item in self.MALICIOUS_ITEMS:
                issues_found.append(f"Malicious item '{item}' detected.")
                is_problematic = True
            elif item in self.ILLEGAL_ITEMS:
                issues_found.append(f"Illegal item '{item}' detected.")
                is_problematic = True
            
            if not is_problematic:
                approved_recs.append(item)
            else:
                print(f"Security Agent blocked '{item}' for {request.user_id}.")

        request.final_recommendations = approved_recs
        request.security_issues = issues_found
        
        if issues_found:
            print(f"Security Agent found issues for {request.user_id}: {', '.join(issues_found)}")
        else:
            print(f"Security Agent approved all recommendations for {request.user_id}.")
        return approved_recs

if __name__ == "__main__":
    user_requests = [
        UserRecommendationRequest("U001", ["electronics", "books"], "adult"),
        UserRecommendationRequest("U002", ["toys"], "child"),
        UserRecommendationRequest("U003", ["fashion"], "teen"),
        UserRecommendationRequest("U004", ["electronics", "sports"], "adult")
    ]

    reco_engine = RecommendationEngineAgent()
    security_agent = SecurityComplianceAgent()

    for req in user_requests:
        print(f"\n--- Processing User {req.user_id} ({req.user_segment}) ---")
        generated_recs = reco_engine.generate_recommendations(req)
        final_recs = security_agent.review_recommendations(req, generated_recs)

        print(f"Final Recommendations for {req.user_id}: {', '.join(final_recs)}")
        if req.security_issues:
            print(f"  Security Issues Detected: {', '.join(req.security_issues)}")
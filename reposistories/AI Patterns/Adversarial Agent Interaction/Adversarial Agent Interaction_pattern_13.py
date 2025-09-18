import random

class CustomerReviewSubmitter:
    def submit_review(self, product_id, customer_id, rating, comment):
        print(f"Customer {customer_id} submitting review for product {product_id} (Rating: {rating}/5).")
        return {"product_id": product_id, "customer_id": customer_id, "rating": rating, "comment": comment}

class ContentModerationAI:
    def evaluate_review(self, review):
        print(f"  Safeguard: Moderating review for product {review['product_id']}...")
        issues = []
        comment = review["comment"].lower()

        profane_words = ["damn", "hell", "shit", "fuck", "bitch", "asshole"]
        for word in profane_words:
            if word in comment:
                issues.append(f"Contains profanity: '{word}'.")
                break
        
        spam_phrases = ["buy now", "click here", "discount code", "free money"]
        for phrase in spam_phrases:
            if phrase in comment:
                issues.append(f"Contains spam phrase: '{phrase}'.")
                break

        if len(comment) < 10 and review["rating"] < 3:
            issues.append("Very short negative review (potential troll). Minimum 10 characters for low rating.")
        
        if any(char.isdigit() for char in comment) and ("contact" in comment or "call" in comment):
            issues.append("Potential personal information or contact attempt (digits with contact keywords).")

        if issues:
            print(f"  Safeguard: Review flagged with issues: {', '.join(issues)}")
            return {"status": "rejected", "issues": issues}
        else:
            print("  Safeguard: Review approved for publishing.")
            return {"status": "approved", "issues": []}

if __name__ == "__main__":
    submitter = CustomerReviewSubmitter()
    moderator = ContentModerationAI()

    reviews_to_test = [
        {"product_id": "PROD101", "customer_id": "CUST001", "rating": 5, "comment": "This product is absolutely fantastic! Love it."}, 
        {"product_id": "PROD102", "customer_id": "CUST002", "rating": 1, "comment": "This product is shit. Total waste of money."}, 
        {"product_id": "PROD103", "customer_id": "CUST003", "rating": 4, "comment": "Great item! Click here for 10% discount code: XYZ123."}, 
        {"product_id": "PROD104", "customer_id": "CUST004", "rating": 2, "comment": "Bad."}, 
        {"product_id": "PROD105", "customer_id": "CUST005", "rating": 3, "comment": "Good product, but contact me at 123-456-7890 if you have issues."}, 
        {"product_id": "PROD106", "customer_id": "CUST006", "rating": 5, "comment": "This is the best!"}
    ]

    for data in reviews_to_test:
        print("-" * 30)
        review_data = submitter.submit_review(data["product_id"], data["customer_id"], data["rating"], data["comment"])
        result = moderator.evaluate_review(review_data)
        if result["status"] == "approved":
            print(f"Review for product {review_data['product_id']} published.")
        else:
            print(f"Review for product {review_data['product_id']} rejected. Issues: {', '.join(result['issues'])}")
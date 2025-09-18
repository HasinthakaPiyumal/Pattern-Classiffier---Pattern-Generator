import random

class ProductReview:
    def __init__(self, product_id, user_id, rating, text):
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        self.text = text

    def __str__(self):
        return f"Product: {self.product_id}, User: {self.user_id}, Rating: {self.rating}/5, Review: '{self.text}'"

class ReviewSubmissionAgent:
    def submit_review(self, product_id, user_id, review_type="normal"):
        rating = random.randint(1, 5)
        if review_type == "normal":
            texts = [
                "Great product, very satisfied!",
                "Works as expected, good value.",
                "Disappointed with the quality, it broke quickly.",
                "Excellent service and fast delivery.",
                "A bit pricey but worth it for the features."
            ]
            text = random.choice(texts)
        elif review_type == "spam":
            texts = [
                "Visit my website for amazing deals: www.spamsite.com",
                "Buy crypto now and get rich! Use code XZY123",
                "This product is okay, but you should really check out my new app!",
                "Follow me on social media @spamguru for more tips!"
            ]
            text = random.choice(texts)
            rating = 5 # Spammers often give high ratings
        elif review_type == "offensive":
            texts = [
                "This product is absolute garbage, and the company is run by idiots!",
                "Never buy from these people, they are a bunch of @#$%!",
                "The design is hideous and clearly made by someone with no taste.",
                "I hate this product and everyone involved in making it."
            ]
            text = random.choice(texts)
            rating = 1 # Offensive reviews often come with low ratings
        else: # Malicious/Hate Speech
            texts = [
                "This company supports [hateful group] and their products are trash.",
                "Do not buy from them, they are [derogatory term]!",
                "The people behind this are [offensive slur]."
            ]
            text = random.choice(texts)
            rating = 1

        return ProductReview(product_id, user_id, rating, text)

class ContentModerationAgent:
    def __init__(self):
        self.profanity_list = {"garbage", "idiots", "hate", "crap", "asshole", "bunch of @#$%", "slur", "trash"} # Simplified
        self.spam_keywords = {"website", "buy crypto", "app", "follow me", "deals", "promo code"}
        self.url_pattern = "www." # Simple check for URLs
        self.hate_speech_patterns = {"[hateful group]", "[derogatory term]", "[offensive slur]"} # Simplified, would be complex NLP

    def moderate_review(self, review):
        is_flagged = False
        reasons = []
        text_lower = review.text.lower()

        for word in self.profanity_list:
            if word in text_lower:
                is_flagged = True
                reasons.append(f"Contains profanity/offensive language: '{word}'")
                break
        
        for keyword in self.spam_keywords:
            if keyword in text_lower:
                is_flagged = True
                reasons.append(f"Contains spam keyword: '{keyword}'")
                break
        
        if self.url_pattern in text_lower:
            is_flagged = True
            reasons.append("Contains URL (potential spam)")

        for pattern in self.hate_speech_patterns:
            if pattern in text_lower:
                is_flagged = True
                reasons.append(f"Contains hate speech pattern: '{pattern}'")
                break

        if review.rating == 1 and len(review.text) < 15 and not reasons: # Simulation of low-effort malicious review
            is_flagged = True
            reasons.append("Very low rating with short/generic text (potential abuse)")

        return is_flagged, reasons

if __name__ == "__main__":
    submitter = ReviewSubmissionAgent()
    moderator = ContentModerationAgent()

    print("--- Simulating E-commerce Product Review Moderation (Real-world: UGC moderation platforms) ---")

    product_id = "PROD123"
    
    # Simulate various reviews to test moderation rules (simulation pattern)
    simulated_reviews = [
        submitter.submit_review(product_id, "user_A", "normal"),
        submitter.submit_review(product_id, "user_B", "spam"),
        submitter.submit_review(product_id, "user_C", "offensive"),
        submitter.submit_review(product_id, "user_D", "normal"),
        submitter.submit_review(product_id, "user_E", "spam"), 
        submitter.submit_review(product_id, "user_F", "malicious"), 
        ProductReview(product_id, "user_G", 1, "This is bad.") # Short low rating review
    ]
    
    for i, review in enumerate(simulated_reviews):
        print(f"\nProcessing Review {i+1}: {review}")
        is_flagged, reasons = moderator.moderate_review(review)
        if is_flagged:
            print(f"  FLAGGED: Review violates policy! Reasons: {', '.join(reasons)}")
        else:
            print("  Review approved.")

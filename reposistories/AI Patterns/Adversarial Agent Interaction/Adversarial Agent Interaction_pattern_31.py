import time
import random

class ProductReview:
    def __init__(self, product_id, user_id, rating, comment, review_id=None):
        self.review_id = review_id if review_id else f"REV-{int(time.time())}-{random.randint(100, 999)}"
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.is_published = False
        self.moderation_flags = []

    def __str__(self):
        return (f"Review ID: {self.review_id} (Product: {self.product_id}, User: {self.user_id})\n"
                f"  Rating: {self.rating}/5 stars\n"
                f"  Comment: \"{self.comment}\"\n"
                f"  Published: {self.is_published}\n"
                f"  Flags: {', '.join(self.moderation_flags) if self.moderation_flags else 'None'}")

class CustomerReviewSubmitter:
    def submit_review(self, product_id, user_id, rating, comment):
        print(f"Submitter: User {user_id} submitting review for Product {product_id}...")
        return ProductReview(product_id, user_id, rating, comment)

class ContentModerationAgent:
    PROFANITY_LIST = ["damn", "hell", "crap", "asshole", "fuck", "shit"]
    SPAM_KEYWORDS = ["buy now", "discount code", "click here", "free money"]
    MIN_COMMENT_LENGTH = 10

    def moderate_review(self, review: ProductReview):
        print(f"Moderator: Evaluating review {review.review_id}...")
        review.moderation_flags = [] # Reset flags

        comment_lower = review.comment.lower()

        # Check for profanity
        for word in self.PROFANITY_LIST:
            if word in comment_lower:
                review.moderation_flags.append(f"Profanity: '{word}'")
                print(f"  - Flagged: Profanity '{word}' detected.")
                break

        # Check for spam keywords
        for keyword in self.SPAM_KEYWORDS:
            if keyword in comment_lower:
                review.moderation_flags.append(f"Spam: '{keyword}'")
                print(f"  - Flagged: Spam keyword '{keyword}' detected.")
                break

        # Check for insufficient content (e.g., just a rating, no real comment)
        if len(review.comment.strip()) < self.MIN_COMMENT_LENGTH and review.comment.strip(): # If not empty, and too short
            review.moderation_flags.append("ShortComment")
            print(f"  - Flagged: Comment too short ({len(review.comment.strip())} chars).")

        if len(review.moderation_flags) > 0:
            print(f"Moderator: Review {review.review_id} has moderation concerns.")
            return False
        else:
            print(f"Moderator: Review {review.review_id} passed moderation.")
            return True

class ECommercePlatform:
    def __init__(self):
        self.submitter = CustomerReviewSubmitter()
        self.moderator = ContentModerationAgent()
        self.published_reviews = []
        self.pending_reviews = []

    def handle_review_submission(self, product_id, user_id, rating, comment):
        new_review = self.submitter.submit_review(product_id, user_id, rating, comment)
        is_clean = self.moderator.moderate_review(new_review)

        if is_clean:
            new_review.is_published = True
            self.published_reviews.append(new_review)
            print(f"Platform: Review {new_review.review_id} PUBLISHED.")
        else:
            new_review.is_published = False
            self.pending_reviews.append(new_review) # Could go to manual review
            print(f"Platform: Review {new_review.review_id} HELD for manual review due to flags.")
        print(new_review)
        print("-" * 50)

if __name__ == "__main__":
    platform = ECommercePlatform()

    platform.handle_review_submission("PROD-A1", "USER-101", 5, "This product is fantastic! Highly recommend.")
    platform.handle_review_submission("PROD-B2", "USER-102", 1, "This is crap, don't buy now, it's a scam!") # Profanity, Spam
    platform.handle_review_submission("PROD-C3", "USER-103", 4, "It's okay.") # Short comment
    platform.handle_review_submission("PROD-D4", "USER-104", 5, "Amazing! Get your discount code here!") # Spam
    platform.handle_review_submission("PROD-E5", "USER-105", 2, "It's a piece of shit.") # Profanity
    platform.handle_review_submission("PROD-F6", "USER-106", 3, "") # Empty comment with rating, should be okay
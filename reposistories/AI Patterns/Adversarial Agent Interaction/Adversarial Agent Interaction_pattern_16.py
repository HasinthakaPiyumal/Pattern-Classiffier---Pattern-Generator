import random

class SellerListingGenerator:
    def __init__(self, seller_id):
        self.seller_id = seller_id

    def create_product_listing(self, title, description, price, category, image_url="default.jpg"):
        return {
            "seller_id": self.seller_id,
            "title": title,
            "description": description,
            "price": price,
            "category": category,
            "image_url": image_url
        }

class ListingComplianceChecker:
    def __init__(self, prohibited_keywords=None, category_keywords=None):
        self.prohibited_keywords = prohibited_keywords if prohibited_keywords is not None else ["explosive", "weapon", "illegal", "counterfeit", "dangerous"]
        self.category_keywords = category_keywords if category_keywords is not None else {
            "electronics": ["laptop", "phone", "camera", "gadget"],
            "food & grocery": ["organic", "fresh", "snack", "drink"],
            "books": ["novel", "story", "paperback", "ebook"]
        }
        self.min_price_threshold = 0.01

    def evaluate_listing(self, listing):
        title = listing.get("title", "").lower()
        description = listing.get("description", "").lower()
        price = listing.get("price")
        category = listing.get("category", "").lower()

        if not title or not description or price is None or not category:
            return False, "Missing essential listing information (title, description, price, or category)."

        for keyword in self.prohibited_keywords:
            if keyword in title or keyword in description:
                return False, f"Prohibited keyword '{keyword}' found in listing."

        if not isinstance(price, (int, float)) or price <= self.min_price_threshold:
            return False, f"Invalid price: Price must be greater than ${self.min_price_threshold:.2f}."

        if category in self.category_keywords:
            if not any(cat_keyword in description for cat_keyword in self.category_keywords[category]):
                return False, f"Category '{category}' seems inconsistent with description content."
        else:
            return False, f"Invalid category '{category}'."

        return True, "Listing complies with platform policies."

if __name__ == "__main__":
    seller_1 = "SELLER001"
    generator_1 = SellerListingGenerator(seller_1)
    checker_1 = ListingComplianceChecker()

    listing_1 = generator_1.create_product_listing(
        "Smartphone X Pro",
        "A brand new high-performance smartphone with advanced camera features and long battery life. This gadget is perfect for tech enthusiasts.",
        799.99,
        "Electronics"
    )
    print(f"Proposed listing: {listing_1}")
    is_compliant, reason = checker_1.evaluate_listing(listing_1)
    print(f"ListingComplianceChecker: Status: {'COMPLIANT' if is_compliant else 'REJECTED'} - {reason}\n")

    listing_2 = generator_1.create_product_listing(
        "Rare Collectible Item",
        "This vintage item is truly one of a kind. Please note: contains a small illegal component.",
        150.00,
        "Collectibles"
    )
    print(f"Proposed listing: {listing_2}")
    is_compliant, reason = checker_1.evaluate_listing(listing_2)
    print(f"ListingComplianceChecker: Status: {'COMPLIANT' if is_compliant else 'REJECTED'} - {reason}\n")

    listing_3 = generator_1.create_product_listing(
        "Free E-book on Python",
        "Learn Python programming from scratch. This ebook is a great resource.",
        0.00,
        "Books"
    )
    print(f"Proposed listing: {listing_3}")
    is_compliant, reason = checker_1.evaluate_listing(listing_3)
    print(f"ListingComplianceChecker: Status: {'COMPLIANT' if is_compliant else 'REJECTED'} - {reason}\n")

    listing_4 = generator_1.create_product_listing(
        "Delicious Organic Apples",
        "Freshly picked apples, perfect for a healthy snack or baking. Enjoy this natural treat.",
        5.99,
        "Electronics"
    )
    print(f"Proposed listing: {listing_4}")
    is_compliant, reason = checker_1.evaluate_listing(listing_4)
    print(f"ListingComplianceChecker: Status: {'COMPLIANT' if is_compliant else 'REJECTED'} - {reason}\n")

    listing_5 = {
        "seller_id": seller_1,
        "title": "Incomplete Test Item",
        "description": "A test item with missing category",
        "price": 10.00
    }
    print(f"Proposed listing: {listing_5}")
    is_compliant, reason = checker_1.evaluate_listing(listing_5)
    print(f"ListingComplianceChecker: Status: {'COMPLIANT' if is_compliant else 'REJECTED'} - {reason}\n")
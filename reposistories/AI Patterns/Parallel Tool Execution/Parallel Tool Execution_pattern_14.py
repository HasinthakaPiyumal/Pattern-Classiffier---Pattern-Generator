import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_inventory(order_id, items):
    time.sleep(random.uniform(0.5, 1.5))
    if "unavailable_item" in items:
        return {"order_id": order_id, "status": "failed", "reason": "Item unavailable"}
    return {"order_id": order_id, "status": "success", "inventory_ok": True}

def process_payment(order_id, amount):
    time.sleep(random.uniform(0.7, 2.0))
    if random.random() < 0.1:
        return {"order_id": order_id, "status": "failed", "reason": "Payment denied"}
    return {"order_id": order_id, "status": "success", "payment_ok": True}

def generate_shipping_label(order_id, address):
    time.sleep(random.uniform(0.3, 1.0))
    return {"order_id": order_id, "status": "success", "label_generated": True}

def send_confirmation_email(order_id, customer_email):
    time.sleep(random.uniform(0.2, 0.8))
    return {"order_id": order_id, "status": "success"}

def dispatch_order(order_id, tracking_number):
    time.sleep(random.uniform(0.5, 1.5))
    return {"order_id": order_id, "status": "success"}

def process_ecommerce_order(order_data):
    order_id = order_data["id"]
    items = order_data["items"]
    amount = order_data["amount"]
    address = order_data["shipping_address"]
    customer_email = order_data["customer_email"]

    print(f"\n--- Starting processing for Order {order_id} ---")

    results = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_inventory = executor.submit(check_inventory, order_id, items)
        future_payment = executor.submit(process_payment, order_id, amount)
        future_shipping_label = executor.submit(generate_shipping_label, order_id, address)

        for future in as_completed([future_inventory, future_payment, future_shipping_label]):
            result = future.result()
            if result["status"] == "failed":
                print(f"[{order_id}] Critical failure: {result['reason']}. Aborting.")
                return {"order_id": order_id, "overall_status": "failed", "reason": result["reason"]}
            results.update(result)

    if not (results.get("inventory_ok") and results.get("payment_ok") and results.get("label_generated")):
        print(f"[{order_id}] Initial steps failed. Overall status: Failed.")
        return {"order_id": order_id, "overall_status": "failed", "reason": "Pre-checks failed"}

    print(f"[{order_id}] All initial parallel steps completed successfully.")

    email_result = send_confirmation_email(order_id, customer_email)
    if email_result["status"] == "failed":
        results["email_status"] = "failed"

    dispatch_result = dispatch_order(order_id, f"TRACK{order_id}XYZ")
    if dispatch_result["status"] == "failed":
        results["dispatch_status"] = "failed"

    print(f"--- Finished processing for Order {order_id}. Overall status: Success ---")
    results["overall_status"] = "success"
    return results

if __name__ == "__main__":
    orders = [
        {"id": "ORD001", "items": ["Laptop", "Mouse"], "amount": 1200.00, "shipping_address": "123 Main St", "customer_email": "customer1@example.com"},
        {"id": "ORD002", "items": ["Keyboard"], "amount": 75.00, "shipping_address": "456 Oak Ave", "customer_email": "customer2@example.com"},
        {"id": "ORD003", "items": ["unavailable_item"], "amount": 50.00, "shipping_address": "789 Pine Ln", "customer_email": "customer3@example.com"},
        {"id": "ORD004", "items": ["Monitor"], "amount": 300.00, "shipping_address": "101 Elm Rd", "customer_email": "customer4@example.com"}
    ]

    for order in orders:
        final_status = process_ecommerce_order(order)
        print(f"Final result for {order['id']}: {final_status['overall_status']}")
        time.sleep(1)

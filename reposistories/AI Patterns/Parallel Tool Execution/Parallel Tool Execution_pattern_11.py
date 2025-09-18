import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_payment(order_id, amount):
    print(f"Order {order_id}: Processing payment for ${amount}...")
    time.sleep(random.uniform(1, 2))
    if random.random() < 0.1:
        print(f"Order {order_id}: Payment failed!")
        return False
    print(f"Order {order_id}: Payment successful for ${amount}.")
    return True

def update_inventory(order_id, items):
    print(f"Order {order_id}: Updating inventory for {len(items)} items...")
    time.sleep(random.uniform(0.5, 1.5))
    print(f"Order {order_id}: Inventory updated.")
    return True

def generate_shipping_label(order_id, address):
    print(f"Order {order_id}: Generating shipping label for {address}...")
    time.sleep(random.uniform(1, 2.5))
    print(f"Order {order_id}: Shipping label generated.")
    return True

def send_confirmation_email(order_id, customer_email):
    print(f"Order {order_id}: Sending confirmation email to {customer_email}...")
    time.sleep(random.uniform(0.8, 1.8))
    print(f"Order {order_id}: Confirmation email sent.")
    return True

def process_ecommerce_order(order_id, amount, items, address, customer_email):
    print(f"\n--- Starting order processing for Order {order_id} ---")
    payment_successful = process_payment(order_id, amount)
    if not payment_successful:
        print(f"Order {order_id}: Order processing failed due to payment failure.")
        return False
    print(f"Order {order_id}: Payment successful, executing parallel tasks...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(update_inventory, order_id, items): "Inventory Update",
            executor.submit(generate_shipping_label, order_id, address): "Shipping Label Generation",
            executor.submit(send_confirmation_email, order_id, customer_email): "Email Confirmation"
        }
        results = {}
        for future in as_completed(futures):
            task_name = futures[future]
            try:
                result = future.result()
                results[task_name] = result
                print(f"Order {order_id}: Task '{task_name}' completed with result: {result}")
            except Exception as exc:
                results[task_name] = f"Failed: {exc}"
                print(f"Order {order_id}: Task '{task_name}' generated an exception: {exc}")
    all_parallel_tasks_successful = all(results.values())
    if all_parallel_tasks_successful:
        print(f"--- Order {order_id} processing completed successfully! ---")
    else:
        print(f"--- Order {order_id} processing completed with some issues! ---")
    return all_parallel_tasks_successful

if __name__ == "__main__":
    order_data = [
        {"id": "ORD001", "amount": 120.50, "items": ["Laptop", "Mouse"], "address": "123 Main St", "email": "customer1@example.com"},
        {"id": "ORD002", "amount": 50.00, "items": ["Book"], "address": "456 Oak Ave", "email": "customer2@example.com"}
    ]
    for order in order_data:
        process_ecommerce_order(order["id"], order["amount"], order["items"], order["address"], order["email"])

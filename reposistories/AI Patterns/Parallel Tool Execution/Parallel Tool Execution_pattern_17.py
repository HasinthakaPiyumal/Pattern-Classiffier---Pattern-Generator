import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def tool_process_payment(order_id, amount):
    print(f"[{time.time():.2f}] Processing payment for order {order_id} (Amount: ${amount:.2f})...")
    time.sleep(random.uniform(1.0, 2.0))
    if random.random() < 0.1:
        print(f"[{time.time():.2f}] Payment FAILED for order {order_id}.")
        return False
    print(f"[{time.time():.2f}] Payment SUCCESSFUL for order {order_id}.")
    return True

def tool_update_inventory(order_id, items):
    print(f"[{time.time():.2f}] Updating inventory for order {order_id} (Items: {items})...")
    time.sleep(random.uniform(0.5, 1.5))
    print(f"[{time.time():.2f}] Inventory updated for order {order_id}.")
    return True

def tool_generate_shipping_label(order_id, address):
    print(f"[{time.time():.2f}] Generating shipping label for order {order_id} (Address: {address})...")
    time.sleep(random.uniform(0.8, 1.8))
    print(f"[{time.time():.2f}] Shipping label generated for order {order_id}.")
    return True

def tool_send_confirmation_email(order_id, customer_email):
    print(f"[{time.time():.2f}] Sending confirmation email for order {order_id} to {customer_email}...")
    time.sleep(random.uniform(0.3, 1.0))
    print(f"[{time.time():.2f}] Confirmation email sent for order {order_id}.")
    return True

def process_ecommerce_order(order_details):
    order_id = order_details['id']
    amount = order_details['amount']
    items = order_details['items']
    shipping_address = order_details['shipping_address']
    customer_email = order_details['customer_email']

    print(f"\n[{time.time():.2f}] Starting processing for Order {order_id}...")

    payment_successful = tool_process_payment(order_id, amount)
    if not payment_successful:
        print(f"[{time.time():.2f}] Order {order_id} processing halted due to payment failure.")
        return False

    print(f"[{time.time():.2f}] Payment successful. Initiating parallel tasks for Order {order_id}...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(tool_update_inventory, order_id, items): "Inventory Update",
            executor.submit(tool_generate_shipping_label, order_id, shipping_address): "Shipping Label Generation",
            executor.submit(tool_send_confirmation_email, order_id, customer_email): "Email Confirmation"
        }

        results = {}
        for future in as_completed(futures):
            task_name = futures[future]
            try:
                result = future.result()
                results[task_name] = "SUCCESS" if result else "FAILURE"
            except Exception as exc:
                results[task_name] = f"ERROR: {exc}"
            print(f"[{time.time():.2f}] Task '{task_name}' completed with result: {results[task_name]}")

    print(f"[{time.time():.2f}] All parallel tasks for Order {order_id} completed. Final results: {results}")
    return all(res == "SUCCESS" for res in results.values())

if __name__ == "__main__":
    order_1 = {
        'id': 'ORD-001',
        'amount': 120.50,
        'items': ['Laptop', 'Mouse'],
        'shipping_address': '123 Main St, Anytown',
        'customer_email': 'customer1@example.com'
    }
    order_2 = {
        'id': 'ORD-002',
        'amount': 45.00,
        'items': ['Keyboard'],
        'shipping_address': '456 Oak Ave, Otherville',
        'customer_email': 'customer2@example.com'
    }

    process_ecommerce_order(order_1)
    print("-" * 50)
    process_ecommerce_order(order_2)
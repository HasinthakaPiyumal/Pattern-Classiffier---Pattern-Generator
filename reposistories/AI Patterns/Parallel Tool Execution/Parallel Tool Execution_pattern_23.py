import concurrent.futures
import time
import random

def validate_order_details(order_id):
    print(f"[Order {order_id}] Validating order details...")
    time.sleep(random.uniform(0.5, 1.0)) # Simulate database lookup, validation rules
    print(f"[Order {order_id}] Order details validated.")
    return True

def process_payment(order_id, amount):
    print(f"[Order {order_id}] Processing payment of ${amount}...")
    time.sleep(random.uniform(1.0, 2.0)) # Simulate external payment gateway API call
    success = random.choice([True, True, True, False]) # Simulate occasional failure
    if success:
        print(f"[Order {order_id}] Payment processed successfully.")
    else:
        print(f"[Order {order_id}] Payment failed!")
    return success

def update_inventory(order_id, items):
    print(f"[Order {order_id}] Updating inventory for items: {items}...")
    time.sleep(random.uniform(0.7, 1.5)) # Simulate database update
    print(f"[Order {order_id}] Inventory updated.")
    return True

def generate_shipping_label(order_id, address):
    print(f"[Order {order_id}] Generating shipping label for {address}...")
    time.sleep(random.uniform(0.8, 1.2)) # Simulate external shipping API call
    print(f"[Order {order_id}] Shipping label generated.")
    return True

def log_order_completion(order_id):
    print(f"[Order {order_id}] Logging order completion status...")
    time.sleep(random.uniform(0.3, 0.7)) # Simulate internal logging
    print(f"[Order {order_id}] Order completion logged.")
    return True

def send_order_confirmation_email(order_id, customer_email):
    print(f"[Order {order_id}] Sending confirmation email to {customer_email}...")
    time.sleep(random.uniform(0.6, 1.0)) # Simulate email service API call
    print(f"[Order {order_id}] Confirmation email sent.")
    return True

def notify_fulfillment_center(order_id):
    print(f"[Order {order_id}] Notifying fulfillment center...")
    time.sleep(random.uniform(0.5, 0.9)) # Simulate internal system notification
    print(f"[Order {order_id}] Fulfillment center notified.")
    return True

def process_customer_order(order_id, amount, items, address, customer_email):
    print(f"--- Starting order processing for Order {order_id} ---")

    # Step 1: Sequential - Initial validation
    if not validate_order_details(order_id):
        print(f"[Order {order_id}] Order validation failed. Aborting.")
        return False

    # Step 2: Parallel - Core independent tasks
    print(f"[Order {order_id}] Starting parallel execution for payment, inventory, shipping label...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_payment = executor.submit(process_payment, order_id, amount)
        future_inventory = executor.submit(update_inventory, order_id, items)
        future_shipping = executor.submit(generate_shipping_label, order_id, address)

        payment_success = future_payment.result()
        inventory_success = future_inventory.result()
        shipping_success = future_shipping.result()

    if not all([payment_success, inventory_success, shipping_success]):
        print(f"[Order {order_id}] One or more core tasks failed. Aborting further processing.")
        return False
    print(f"[Order {order_id}] All core parallel tasks completed successfully.")

    # Step 3: Sequential - Log completion (depends on core tasks)
    log_order_completion(order_id)

    # Step 4: Parallel - Post-completion notifications
    print(f"[Order {order_id}] Starting parallel execution for email and fulfillment notification...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_email = executor.submit(send_order_confirmation_email, order_id, customer_email)
        future_fulfillment = executor.submit(notify_fulfillment_center, order_id)

        future_email.result()
        future_fulfillment.result()
    print(f"[Order {order_id}] All post-completion tasks completed.")

    print(f"--- Order {order_id} processing complete ---")
    return True

if __name__ == "__main__":
    order_id = "ORD-001"
    amount = 99.99
    items = ["Laptop", "Mouse"]
    address = "123 Main St, Anytown"
    customer_email = "customer@example.com"

    start_time = time.time()
    process_customer_order(order_id, amount, items, address, customer_email)
    end_time = time.time()
    print(f"Total processing time: {end_time - start_time:.2f} seconds")

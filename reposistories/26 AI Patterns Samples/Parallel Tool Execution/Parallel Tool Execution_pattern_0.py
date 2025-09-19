import time
import concurrent.futures

def process_payment(order_id, amount):
    print(f"[Order {order_id}] Processing payment for ${amount:.2f}...")
    time.sleep(2)
    if order_id % 2 == 0:
        print(f"[Order {order_id}] Payment failed.")
        return False
    print(f"[Order {order_id}] Payment successful.")
    return True

def update_inventory(order_id, items):
    print(f"[Order {order_id}] Updating inventory for items: {items}...")
    time.sleep(1.5)
    print(f"[Order {order_id}] Inventory updated.")
    return True

def generate_shipping_label(order_id, shipping_address, items):
    print(f"[Order {order_id}] Generating shipping label for {shipping_address}...")
    time.sleep(1)
    print(f"[Order {order_id}] Shipping label generated.")
    return True

def send_confirmation_email(order_id, customer_email, order_details):
    print(f"[Order {order_id}] Sending confirmation email to {customer_email}...")
    time.sleep(0.8)
    print(f"[Order {order_id}] Confirmation email sent.")
    return True

def log_order_completion(order_id):
    print(f"[Order {order_id}] Logging order completion.")
    time.sleep(0.5)
    print(f"[Order {order_id}] Order fully processed and logged.")
    return True

def process_e_commerce_order(order_id, amount, items, shipping_address, customer_email):
    print(f"\n--- Starting processing for Order {order_id} ---")

    print(f"[Order {order_id}] Initiating parallel tasks: Payment, Inventory Update, Shipping Label.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_payment = executor.submit(process_payment, order_id, amount)
        future_inventory = executor.submit(update_inventory, order_id, items)
        future_shipping = executor.submit(generate_shipping_label, order_id, shipping_address, items)

        payment_status = future_payment.result()
        inventory_status = future_inventory.result()
        shipping_status = future_shipping.result()

    if payment_status and inventory_status and shipping_status:
        print(f"[Order {order_id}] All initial tasks completed successfully. Proceeding with confirmation.")
        send_confirmation_email(order_id, customer_email, {"items": items, "amount": amount})
        log_order_completion(order_id)
    else:
        print(f"[Order {order_id}] One or more initial tasks failed. Aborting full order completion.")

    print(f"--- Finished processing for Order {order_id} ---")

if __name__ == "__main__":
    orders_to_process = [
        {"id": 101, "amount": 120.50, "items": ["Laptop", "Mouse"], "address": "123 Main St", "email": "customer1@example.com"},
        {"id": 102, "amount": 55.00, "items": ["Keyboard"], "address": "456 Oak Ave", "email": "customer2@example.com"},
        {"id": 103, "amount": 300.75, "items": ["Monitor"], "address": "789 Pine Ln", "email": "customer3@example.com"}
    ]

    for order in orders_to_process:
        process_e_commerce_order(
            order["id"],
            order["amount"],
            order["items"],
            order["address"],
            order["email"]
        )

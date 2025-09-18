import time
import concurrent.futures

def process_payment(order_id, amount):
    time.sleep(2)
    return f"Order {order_id}: Payment of ${amount:.2f} processed."

def update_inventory(order_id, items):
    time.sleep(1.5)
    return f"Order {order_id}: Inventory updated for items {items}."

def generate_shipping_label(order_id, address):
    time.sleep(1.8)
    return f"Order {order_id}: Shipping label generated for {address}."

def send_confirmation_email(order_id, customer_email):
    time.sleep(1.2)
    return f"Order {order_id}: Confirmation email sent to {customer_email}."

def log_order_history(order_id, customer_id):
    time.sleep(0.8)
    return f"Order {order_id}: Logged into customer {customer_id} history."

def complete_order_finalization(order_id):
    time.sleep(0.5)
    return f"Order {order_id}: All parallel tasks completed. Finalizing order."

def process_ecommerce_order(order_details):
    order_id = order_details["order_id"]
    customer_id = order_details["customer_id"]
    amount = order_details["amount"]
    items = order_details["items"]
    address = order_details["shipping_address"]
    customer_email = order_details["customer_email"]

    print(f"--- Starting processing for Order {order_id} ---")

    print(f"Order {order_id}: Validating order details sequentially.")
    time.sleep(0.5)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_payment = executor.submit(process_payment, order_id, amount)
        future_inventory = executor.submit(update_inventory, order_id, items)
        future_shipping = executor.submit(generate_shipping_label, order_id, address)
        future_email = executor.submit(send_confirmation_email, order_id, customer_email)
        future_log = executor.submit(log_order_history, order_id, customer_id)

        parallel_results = []
        for future in concurrent.futures.as_completed([future_payment, future_inventory, future_shipping, future_email, future_log]):
            parallel_results.append(future.result())

    for res in parallel_results:
        print(res)

    final_status = complete_order_finalization(order_id)
    print(final_status)
    print(f"--- Finished processing for Order {order_id} ---")

if __name__ == "__main__":
    order_data = {
        "order_id": "EC987654",
        "customer_id": "CUST12345",
        "amount": 199.99,
        "items": ["Laptop", "Mouse"],
        "shipping_address": "123 Main St, Anytown, USA",
        "customer_email": "customer@example.com"
    }
    process_ecommerce_order(order_data)
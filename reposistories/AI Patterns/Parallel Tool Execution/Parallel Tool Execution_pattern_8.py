import concurrent.futures
import time
import random

def process_payment(order_id, amount):
    print(f"[{time.time():.2f}] Processing payment for order {order_id} (Amount: ${amount})...")
    time.sleep(random.uniform(1.5, 3.0)) # Simulate payment gateway latency
    success = random.choice([True, True, True, False]) # Simulate occasional payment failure
    if success:
        print(f"[{time.time():.2f}] Payment for order {order_id} successful.")
        return {"status": "success", "transaction_id": f"TXN{random.randint(10000, 99999)}"}
    else:
        print(f"[{time.time():.2f}] Payment for order {order_id} failed.")
        return {"status": "failed", "error": "Insufficient funds or card declined"}

def update_inventory(product_id, quantity):
    print(f"[{time.time():.2f}] Updating inventory for product {product_id} (Quantity: {quantity})...")
    time.sleep(random.uniform(0.8, 2.0)) # Simulate database update latency
    print(f"[{time.time():.2f}] Inventory updated for product {product_id}.")
    return {"status": "success", "product_id": product_id, "new_stock": random.randint(10, 100)}

def generate_shipping_label(order_id, address):
    print(f"[{time.time():.2f}] Generating shipping label for order {order_id} to {address}...")
    time.sleep(random.uniform(1.0, 2.5)) # Simulate label generation service latency
    print(f"[{time.time():.2f}] Shipping label generated for order {order_id}.")
    return {"status": "success", "tracking_number": f"TRK{random.randint(1000000, 9999999)}"}

def send_confirmation_email(customer_email, order_details, payment_status, shipping_info):
    print(f"[{time.time():.2f}] Sending confirmation email to {customer_email}...")
    time.sleep(random.uniform(0.5, 1.5)) # Simulate email sending latency
    print(f"[{time.time():.2f}] Confirmation email sent to {customer_email}. Payment: {payment_status['status']}")
    return {"status": "success"}

def process_ecommerce_order(order_data):
    order_id = order_data['order_id']
    customer_email = order_data['customer_email']
    product_id = order_data['product_id']
    quantity = order_data['quantity']
    amount = order_data['amount']
    shipping_address = order_data['shipping_address']

    print(f"\n[{time.time():.2f}] --- Starting order processing for Order {order_id} ---")

    # Step 1: Initial sequential step - Order validation (simulated)
    print(f"[{time.time():.2f}] Validating order {order_id}...")
    time.sleep(0.5)
    print(f"[{time.time():.2f}] Order {order_id} validated. Initiating core processes.")

    # Step 2: Parallel execution of independent tasks
    # Payment processing, inventory update, and shipping label generation can happen concurrently.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        payment_future = executor.submit(process_payment, order_id, amount)
        inventory_future = executor.submit(update_inventory, product_id, quantity)
        shipping_future = executor.submit(generate_shipping_label, order_id, shipping_address)

        payment_result = payment_future.result() # Wait for payment to complete
        inventory_result = inventory_future.result() # Wait for inventory to complete
        shipping_result = shipping_future.result() # Wait for shipping label to complete

    if payment_result['status'] == 'failed':
        print(f"[{time.time():.2f}] Order {order_id} processing failed due to payment failure: {payment_result['error']}")
        return {"order_status": "failed", "reason": "payment_failed"}

    # Step 3: Sequential dependent task (requires payment and order details)
    print(f"[{time.time():.2f}] All core parallel tasks completed for order {order_id}. Sending confirmation email.")
    email_result = send_confirmation_email(customer_email, order_data, payment_result, shipping_result)

    print(f"[{time.time():.2f}] --- Order processing for Order {order_id} complete ---")
    return {
        "order_status": "completed",
        "payment": payment_result,
        "inventory": inventory_result,
        "shipping": shipping_result,
        "email": email_result
    }

if __name__ == "__main__":
    order1 = {
        'order_id': 'ORD78901',
        'customer_email': 'alice@example.com',
        'product_id': 'PROD001',
        'quantity': 2,
        'amount': 120.50,
        'shipping_address': '123 Main St, Anytown, USA'
    }
    order_status = process_ecommerce_order(order1)
    print(f"\nFinal Order Status for ORD78901: {order_status['order_status']}")

    order2 = {
        'order_id': 'ORD78902',
        'customer_email': 'bob@example.com',
        'product_id': 'PROD002',
        'quantity': 1,
        'amount': 50.00,
        'shipping_address': '456 Oak Ave, Othercity, USA'
    }
    # Simulate a payment failure for this order
    print("\n--- Simulating an order with potential payment failure ---")
    random.seed(1) # Make payment fail for the next call for demonstration
    order_status = process_ecommerce_order(order2)
    print(f"\nFinal Order Status for ORD78902: {order_status['order_status']}")

import time
import concurrent.futures

def check_inventory(product_id: str, quantity: int) -> dict:
    time.sleep(1.5) # Simulate API call or database query
    # print(f"  Checking inventory for {product_id} (qty: {quantity})...")
    if product_id == "PROD101" and quantity <= 5:
        return {"task": "inventory_check", "success": True, "message": f"Inventory OK for {product_id}"}
    return {"task": "inventory_check", "success": False, "message": f"Inventory LOW for {product_id}"}

def process_payment(order_id: str, amount: float) -> dict:
    time.sleep(2.0) # Simulate external payment gateway call
    # print(f"  Processing payment for order {order_id} (amount: ${amount:.2f})...")
    if amount > 0:
        return {"task": "payment_processing", "success": True, "message": f"Payment successful for order {order_id}"}
    return {"task": "payment_processing", "success": False, "message": f"Payment failed for order {order_id}"}

def generate_shipping_label(order_id: str, address: str) -> dict:
    time.sleep(1.0) # Simulate label generation service
    # print(f"  Generating shipping label for order {order_id} to {address}...")
    return {"task": "shipping_label", "success": True, "message": f"Shipping label generated for order {order_id}"}

def send_customer_notification(customer_email: str, message: str) -> dict:
    time.sleep(0.8) # Simulate email sending service
    # print(f"  Sending notification to {customer_email}: '{message}'...")
    return {"task": "customer_notification", "success": True, "message": f"Notification sent to {customer_email}"}

def process_e_commerce_order(order_details: dict):
    print(f"\n--- Processing Order {order_details['order_id']} ---")
    start_time = time.perf_counter()

    order_id = order_details['order_id']
    product_id = order_details['product_id']
    quantity = order_details['quantity']
    amount = order_details['amount']
    customer_email = order_details['customer_email']
    shipping_address = order_details['shipping_address']

    # Independent tasks: Inventory check and Payment processing
    # These can run in parallel as one doesn't strictly depend on the other's completion to start.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_inventory = executor.submit(check_inventory, product_id, quantity)
        future_payment = executor.submit(process_payment, order_id, amount)

        inventory_result = future_inventory.result()
        payment_result = future_payment.result()

    print(f"[Parallel Step 1 Results]:")
    print(f"  - {inventory_result['message']}")
    print(f"  - {payment_result['message']}")

    # Dependent tasks: Shipping label generation and Customer notification
    # These typically depend on the success of the initial parallel steps.
    if inventory_result['success'] and payment_result['success']:
        print("[Sequential Step 2: Post-processing]")
        shipping_label_result = generate_shipping_label(order_id, shipping_address)
        notification_message = f"Your order {order_id} has been confirmed and is being prepared for shipment."
        notification_result = send_customer_notification(customer_email, notification_message)
        
        print(f"  - {shipping_label_result['message']}")
        print(f"  - {notification_result['message']}")
        final_status = "Order Successfully Processed"
    else:
        notification_message = f"There was an issue processing your order {order_id}. Please contact support."
        send_customer_notification(customer_email, notification_message)
        final_status = "Order Processing Failed"

    end_time = time.perf_counter()
    print(f"--- Order {order_id} Processing {final_status} in {end_time - start_time:.2f} seconds ---")

if __name__ == "__main__":
    order1 = {
        "order_id": "EC001",
        "product_id": "PROD101",
        "quantity": 2,
        "amount": 49.99,
        "customer_email": "alice@example.com",
        "shipping_address": "123 Main St"
    }
    order2 = {
        "order_id": "EC002",
        "product_id": "PROD102", # Assume low inventory for simulation
        "quantity": 10,
        "amount": 199.99,
        "customer_email": "bob@example.com",
        "shipping_address": "456 Oak Ave"
    }

    process_e_commerce_order(order1)
    process_e_commerce_order(order2)

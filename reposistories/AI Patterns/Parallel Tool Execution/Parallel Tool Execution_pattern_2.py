import concurrent.futures
import time
import random

def deduct_inventory(product_id, quantity):
    print(f"  [Inventory] Deducting {quantity} of product {product_id}...")
    time.sleep(random.uniform(0.5, 1.5))
    print(f"  [Inventory] Inventory for {product_id} updated.")
    return True

def generate_shipping_label(order_id, address):
    print(f"  [Shipping] Generating label for order {order_id} to {address}...")
    time.sleep(random.uniform(0.8, 2.0))
    label_info = f"Label-ORD{order_id}-SHIP-{random.randint(1000,9999)}"
    print(f"  [Shipping] Shipping label {label_info} generated.")
    return label_info

def send_confirmation_email(customer_email, order_id, items):
    print(f"  [Email] Sending confirmation to {customer_email} for order {order_id}...")
    time.sleep(random.uniform(0.7, 1.8))
    print(f"  [Email] Confirmation email sent for order {order_id}.")
    return True

def mark_order_complete(order_id, inventory_status, label_info, email_status):
    print(f"[Order Manager] Marking order {order_id} as complete...")
    if inventory_status and label_info and email_status:
        time.sleep(0.5)
        print(f"[Order Manager] Order {order_id} successfully completed. Label: {label_info}")
        return True
    else:
        print(f"[Order Manager] Order {order_id} completion failed due to prior issues.")
        return False

def process_ecommerce_order(order_data):
    order_id = order_data["order_id"]
    customer_email = order_data["customer_email"]
    shipping_address = order_data["shipping_address"]
    items = order_data["items"]

    print(f"--- Starting processing for Order ID: {order_id} ---")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_inventory = executor.submit(deduct_inventory, items[0]["product_id"], items[0]["quantity"])
        future_shipping = executor.submit(generate_shipping_label, order_id, shipping_address)
        future_email = executor.submit(send_confirmation_email, customer_email, order_id, items)

        inventory_status = future_inventory.result()
        shipping_label = future_shipping.result()
        email_sent = future_email.result()

    print(f"\n--- Parallel tasks for Order {order_id} completed ---")
    print(f"  Inventory Status: {inventory_status}")
    print(f"  Shipping Label: {shipping_label}")
    print(f"  Email Sent: {email_sent}")

    order_complete_status = mark_order_complete(order_id, inventory_status, shipping_label, email_sent)

    print(f"--- Finished processing for Order ID: {order_id}. Overall Success: {order_complete_status} ---\n")
    return order_complete_status

if __name__ == "__main__":
    order_info = {
        "order_id": "ORD78901",
        "customer_email": "alice@example.com",
        "shipping_address": "123 Main St, Anytown, USA",
        "items": [{"product_id": "PROD001", "quantity": 2}]
    }
    process_ecommerce_order(order_info)

    order_info_2 = {
        "order_id": "ORD78902",
        "customer_email": "bob@example.com",
        "shipping_address": "456 Oak Ave, Otherville, USA",
        "items": [{"product_id": "PROD002", "quantity": 1}]
    }
    process_ecommerce_order(order_info_2)

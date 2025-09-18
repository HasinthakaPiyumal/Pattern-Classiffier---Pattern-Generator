import time
import concurrent.futures

def process_payment(order_id, amount):
    time.sleep(2) # Simulate external payment gateway call
    print(f"Order {order_id}: Payment of ${amount} processed.")
    return True

def update_inventory(order_id, item_list):
    time.sleep(1.5) # Simulate database update
    print(f"Order {order_id}: Inventory updated for items: {item_list}.")
    return True

def generate_shipping_label(order_id, address):
    time.sleep(1.8) # Simulate shipping carrier API call
    print(f"Order {order_id}: Shipping label generated for {address}.")
    return True

def send_confirmation_email(order_id, customer_email, status):
    time.sleep(0.5) # Simulate email service call
    print(f"Order {order_id}: Confirmation email sent to {customer_email} with status: {status}.")
    return True

def fulfill_order(order_details):
    order_id = order_details['order_id']
    amount = order_details['amount']
    items = order_details['items']
    address = order_details['shipping_address']
    customer_email = order_details['customer_email']

    print(f"\n--- Starting order fulfillment for Order {order_id} ---")

    # Step 1: Initial sequential checks (e.g., fraud check, stock availability)
    time.sleep(0.3)
    print(f"Order {order_id}: Initial order validation complete.")

    # Step 2: Parallel execution for independent tasks
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        payment_future = executor.submit(process_payment, order_id, amount)
        inventory_future = executor.submit(update_inventory, order_id, items)
        shipping_future = executor.submit(generate_shipping_label, order_id, address)

        # Wait for all parallel tasks to complete
        concurrent.futures.wait([payment_future, inventory_future, shipping_future])

        payment_success = payment_future.result()
        inventory_success = inventory_future.result()
        shipping_success = shipping_future.result()

    if payment_success and inventory_success and shipping_success:
        print(f"Order {order_id}: All core fulfillment tasks completed successfully.")
        # Step 3: Dependent sequential task
        send_confirmation_email(order_id, customer_email, "Fulfilled")
        print(f"--- Order {order_id} fulfillment complete ---")
        return True
    else:
        print(f"Order {order_id}: Some fulfillment tasks failed. Rolling back or alerting.")
        send_confirmation_email(order_id, customer_email, "Failed")
        print(f"--- Order {order_id} fulfillment failed ---")
        return False

if __name__ == "__main__":
    order1 = {
        'order_id': 'EC001',
        'amount': 120.50,
        'items': ['Laptop Bag', 'Mouse'],
        'shipping_address': '123 Main St, Anytown',
        'customer_email': 'customer1@example.com'
    }
    order2 = {
        'order_id': 'EC002',
        'amount': 55.00,
        'items': ['Book', 'Pen Set'],
        'shipping_address': '456 Oak Ave, Otherville',
        'customer_email': 'customer2@example.com'
    }
    fulfill_order(order1)
    fulfill_order(order2)